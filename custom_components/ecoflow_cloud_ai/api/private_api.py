import base64
import hashlib
import logging
from time import time
from typing import Any, Protocol, runtime_checkable

import aiohttp
from aiohttp import ClientSession
from homeassistant.util import uuid
from paho.mqtt.client import PayloadType

from ..device_data import DeviceData
from ..devices import DiagnosticDevice, EcoflowDeviceInfo
from . import EcoflowApiClient, EcoflowException
from .message import Message

_LOGGER = logging.getLogger(__name__)


@runtime_checkable
class PrivateAPIMessageProtocol(Protocol):
    def private_api_to_mqtt_payload(self) -> PayloadType:
        raise NotImplementedError()


class EcoflowPrivateApiClient(EcoflowApiClient):
    def __init__(
        self, api_domain: str, ecoflow_username: str, ecoflow_password: str, group: str
    ):
        super().__init__()
        self.api_domain = api_domain
        self.ecoflow_password = ecoflow_password
        self.ecoflow_username = ecoflow_username
        self.group = group
        self.user_id = None
        self.token = None
        self.user_name = None
        self.session: ClientSession | None = None

    async def login(self):
        self.session = ClientSession()
        url = f"https://{self.api_domain}/auth/login"
        headers = {"lang": "en_US", "content-type": "application/json"}
        data = {
            "email": self.ecoflow_username,
            "password": base64.b64encode(self.ecoflow_password.encode()).decode(),
            "scene": "IOT_APP",
            "userType": "ECOFLOW",
        }

        _LOGGER.info(f"Login to EcoFlow API {url}")

        resp = await self.session.post(url, headers=headers, json=data)
        response = await self._get_json_response(resp)

        try:
            self.token = response["data"]["token"]
            self.user_id = response["data"]["user"]["userId"]
            self.user_name = response["data"]["user"].get("name", "<no user name>")
        except KeyError as key:
            raise EcoflowException(
                f"Failed to extract key {key} from response: {response}"
            )

        _LOGGER.info(f"Successfully logged in: {self.user_name}")

        _LOGGER.info("Requesting IoT MQTT credentials")
        response = await self.__call_api("/iot-auth/app/certification")
        self._accept_mqqt_certification(response)

        # Should be ANDROID_..str.._user_id !!!
        self.mqtt_info.client_id = (
            f"ANDROID_{str(uuid.random_uuid_hex()).upper()}_{self.user_id}"
        )

    # Failed to connect to MQTT: not authorised
    def gen_client_id(self):
        base = f"ANDROID_{str(uuid.random_uuid_hex()).upper()}_{self.user_id}"
        millis = int(time() * 1000)
        verify_info = "0000000000000000000000000000000000000000000000000000000000000000"
        pub = verify_info[:32]
        priv = verify_info[32:]
        k = priv + base + str(millis)
        res = (
            base
            + "_"
            + pub
            + "_"
            + str(millis)
            + "_"
            + hashlib.md5(k.encode("utf-8")).hexdigest()
        )
        return res

    async def fetch_all_available_devices(self):
        return []

    async def quota_all(self, device_sn: str | None):
        if not device_sn:
            target_devices = self.devices.items()
        else:
            target_devices = [(device_sn, self.devices[device_sn])]

        for sn, device in target_devices:
            self.send_get_message(sn, device.private_api_get_quota())

    def configure_device(self, device_data: DeviceData):
        if device_data.parent is not None:
            info = self.__create_device_info(
                device_data.parent.sn, device_data.name, device_data.parent.device_type
            )
        else:
            info = self.__create_device_info(
                device_data.sn, device_data.name, device_data.device_type
            )

        from ..devices.registry import devices

        if device_data.device_type in devices:
            device = devices[device_data.device_type](info, device_data)
        elif device_data.parent.device_type in devices:
            # this can be problematic if a parent chain is recursive (so a parent has a parent again)
            # the current data structure alows this, but it is not supported here.
            device = devices[device_data.parent.device_type](info, device_data)
        else:
            device = DiagnosticDevice(info, device_data)

        self.add_device(device)

        return device

    def __create_device_info(
        self, device_sn: str, device_name: str, device_type: str, status: int = -1
    ) -> EcoflowDeviceInfo:
        return EcoflowDeviceInfo(
            public_api=False,
            sn=device_sn,
            name=device_name,
            device_type=device_type,
            status=status,
            data_topic=f"/app/device/property/{device_sn}",
            set_topic=f"/app/{self.user_id}/{device_sn}/thing/property/set",
            set_reply_topic=f"/app/{self.user_id}/{device_sn}/thing/property/set_reply",
            get_topic=f"/app/{self.user_id}/{device_sn}/thing/property/get",
            get_reply_topic=f"/app/{self.user_id}/{device_sn}/thing/property/get_reply",
        )

    async def __call_api(
        self, endpoint: str, params: dict[str:any] | None = None
    ) -> dict:
        assert self.session is not None
        headers = {
            "lang": "en_US",
            "authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }
        user_data = {"userId": self.user_id}
        req_params = {}
        if params is not None:
            req_params.update(params)

        resp = await self.session.get(
            f"https://{self.api_domain}{endpoint}",
            data=user_data,
            params=req_params,
            headers=headers,
        )
        _LOGGER.info(f"Request: {endpoint} {req_params}: got {resp}")
        return await self._get_json_response(resp)

    def send_get_message(self, device_sn: str, command: dict | Message):
        if isinstance(command, PrivateAPIMessageProtocol):
            self.mqtt_client.publish(
                self.devices[device_sn].device_info.get_topic,
                command.private_api_to_mqtt_payload(),
            )
        else:
            super().send_get_message(device_sn, command)

    def send_set_message(
        self,
        device_sn: str,
        mqtt_state: dict[str, Any],
        command: dict | Message,
        interaction: str | None = None,
    ):
        if isinstance(command, PrivateAPIMessageProtocol):
            self.devices[device_sn].data.update_to_target_state(mqtt_state)
            self.mqtt_client.publish(
                self.devices[device_sn].device_info.set_topic,
                command.private_api_to_mqtt_payload(),
            )
            if interaction is not None:
                _LOGGER.info(
                    "Interaction '%s' triggered set on %s with %s",
                    interaction,
                    device_sn,
                    mqtt_state,
                )
        else:
            super().send_set_message(device_sn, mqtt_state, command, interaction)
