import hashlib
import hmac
import logging
import random
import time
import asyncio

import aiohttp
from aiohttp import ClientSession

from ..device_data import DeviceData
from ..devices import DiagnosticDevice, EcoflowDeviceInfo
from . import EcoflowApiClient

_LOGGER = logging.getLogger(__name__)

# from FB
# client_id limits for MQTT connections
# If you are using MQTT to connect to the API be aware that only 10 unique client IDs are allowed per day.
# As such, it is suggested that you choose a static client_id for your application or integration to use consistently.
# If your code generates a unique client_id (as mine did) for each connection,
# you can exceed this limit very quickly when testing or debugging code.


class EcoflowPublicApiClient(EcoflowApiClient):
    def __init__(self, api_domain: str, access_key: str, secret_key: str, group: str):
        super().__init__()
        self.api_domain = api_domain
        self.access_key = access_key
        self.secret_key = secret_key
        self.group = group
        self.nonce = str(random.randint(10000, 1000000))
        self.timestamp = str(int(time.time() * 1000))
        self.session: ClientSession | None = None

    async def login(self):
        self.session = ClientSession()
        _LOGGER.info("Requesting IoT MQTT credentials")
        response = await self.call_api("/certification")
        self._accept_mqqt_certification(response)
        self.mqtt_info.client_id = (
            f"Hassio-{self.mqtt_info.username}-{self.group.replace(' ', '-')}"
        )

    async def fetch_all_available_devices(self) -> list[EcoflowDeviceInfo]:
        _LOGGER.info("Requesting all devices")
        response = await self.call_api("/device/list")
        result = list()
        for device in response["data"]:
            _LOGGER.debug(str(device))
            sn = device["sn"]
            product_name = device.get("productName", "undefined")
            if product_name == "undefined":
                from ..devices.registry import device_by_product

                device_list = list(device_by_product.keys())
                for devicetype in device_list:
                    if "deviceName" in device and device[
                        "deviceName"
                    ].lower().startswith(devicetype.lower()):
                        product_name = devicetype
            device_name = device.get("deviceName", f"{product_name}-{sn}")
            status = int(device["online"])
            result.append(
                self.__create_device_info(sn, device_name, product_name, status)
            )

        return result

    def configure_device(self, device_data: DeviceData):
        if device_data.parent is not None:
            info = self.__create_device_info(
                device_data.parent.sn, device_data.name, device_data.parent.device_type
            )
        else:
            info = self.__create_device_info(
                device_data.sn, device_data.name, device_data.device_type
            )

        from custom_components.ecoflow_cloud_ai.devices.registry import device_by_product

        if device_data.device_type in device_by_product:
            device = device_by_product[device_data.device_type](info, device_data)
        elif (
            device_data.parent is not None
            and device_data.parent.device_type in device_by_product
        ):
            device = device_by_product[device_data.parent.device_type](
                info, device_data
            )
        else:
            device = DiagnosticDevice(info, device_data)

        self.add_device(device)
        return device

    async def quota_all(self, device_sn: str | None):
        if not device_sn:
            target_devices = self.devices.keys()
            # update all statuses
            devices = await self.fetch_all_available_devices()
            for device in devices:
                if device.sn in self.devices:
                    self.devices[device.sn].data.update_status(
                        {"params": {"status": device.status}}
                    )
        else:
            target_devices = [device_sn]

        tasks = [
            self.call_api("/device/quota/all", {"sn": sn}) for sn in target_devices
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for sn, result in zip(target_devices, results):
            if isinstance(result, Exception):
                _LOGGER.error(result, exc_info=True)
                _LOGGER.error("Erreur recuperation %s", sn)
            else:
                if "data" in result:
                    self.devices[sn].data.update_data({"params": result["data"]})

    async def call_api(self, endpoint: str, params: dict[str, str] = None) -> dict:
        self.nonce = str(random.randint(10000, 1000000))
        self.timestamp = str(int(time.time() * 1000))
        assert self.session is not None
        params_str = ""
        if params is not None:
            params_str = self.__sort_and_concat_params(params)

        sign = self.__gen_sign(params_str)

        headers = {
            "accessKey": self.access_key,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "sign": sign,
        }

        _LOGGER.debug("Request: %s %s.", str(endpoint), str(params_str))
        resp = await self.session.get(
            f"https://{self.api_domain}/iot-open/sign{endpoint}?{params_str}",
            headers=headers,
        )
        json_resp = await self._get_json_response(resp)
        _LOGGER.debug(
            "Request: %s %s. Response : %s",
            str(endpoint),
            str(params_str),
            str(json_resp),
        )
        return json_resp

    def __create_device_info(
        self, device_sn: str, device_name: str, device_type: str, status: int = -1
    ) -> EcoflowDeviceInfo:
        return EcoflowDeviceInfo(
            public_api=True,
            sn=device_sn,
            name=device_name,
            device_type=device_type,
            status=status,
            data_topic=f"/open/{self.mqtt_info.username}/{device_sn}/quota",
            set_topic=f"/open/{self.mqtt_info.username}/{device_sn}/set",
            set_reply_topic=f"/open/{self.mqtt_info.username}/{device_sn}/set_reply",
            get_topic=None,
            get_reply_topic=None,
            status_topic=f"/open/{self.mqtt_info.username}/{device_sn}/status",
        )

    def __gen_sign(self, query_params: str | None) -> str:
        target_str = (
            f"accessKey={self.access_key}&nonce={self.nonce}&timestamp={self.timestamp}"
        )
        if query_params:
            target_str = query_params + "&" + target_str

        return self.__encrypt_hmac_sha256(target_str, self.secret_key)

    def __sort_and_concat_params(self, params: dict[str, str]) -> str:
        # Sort the dictionary items by key
        sorted_items = sorted(params.items(), key=lambda x: x[0])

        # Create a list of "key=value" strings
        param_strings = [f"{key}={value}" for key, value in sorted_items]

        # Join the strings with '&'
        return "&".join(param_strings)

    def __encrypt_hmac_sha256(self, message: str, secret_key: str) -> str:
        # Convert the message and secret key to bytes
        message_bytes = message.encode("utf-8")
        secret_bytes = secret_key.encode("utf-8")

        # Create the HMAC
        hmac_obj = hmac.new(secret_bytes, message_bytes, hashlib.sha256)

        # Get the hexadecimal representation of the HMAC
        hmac_digest = hmac_obj.hexdigest()

        return hmac_digest
