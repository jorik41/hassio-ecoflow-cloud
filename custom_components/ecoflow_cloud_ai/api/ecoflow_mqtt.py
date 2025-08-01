import logging
import ssl
import asyncio
from _socket import SocketType
from typing import Any

from homeassistant.core import callback
from paho.mqtt.client import MQTTMessage, PayloadType

from ..devices import BaseDevice
from . import EcoflowMqttInfo

_LOGGER = logging.getLogger(__name__)


class EcoflowMQTTClient:
    def __init__(self, mqtt_info: EcoflowMqttInfo, devices: dict[str, BaseDevice]):
        from ..devices import BaseDevice

        self.connected = False
        self.__mqtt_info = mqtt_info
        self.__devices: dict[str, BaseDevice] = devices
        self.__topic_device_map: dict[str, BaseDevice] = {}
        for device in self.__devices.values():
            self._register_device_topics(device)

        from homeassistant.components.mqtt.async_client import AsyncMQTTClient

        self.__client: AsyncMQTTClient = AsyncMQTTClient(
            client_id=self.__mqtt_info.client_id,
            reconnect_on_failure=True,
            clean_session=True,
        )

        # self.__client._connect_timeout = 15.0
        self.__client.setup()
        self.__client.username_pw_set(
            self.__mqtt_info.username, self.__mqtt_info.password
        )
        if self.__mqtt_info.ssl:
            self.__client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED)
            self.__client.tls_insecure_set(False)
        self.__client.on_connect = self._on_connect
        self.__client.on_disconnect = self._on_disconnect
        self.__client.on_message = self._on_message
        self.__client.on_socket_close = self._on_socket_close

        _LOGGER.info(
            f"Connecting to MQTT Broker {self.__mqtt_info.url}:{self.__mqtt_info.port} with client id {self.__mqtt_info.client_id} and username {self.__mqtt_info.username}"
        )
        self.__client.connect(self.__mqtt_info.url, self.__mqtt_info.port, keepalive=15)
        self.__client.loop_start()

    def _register_device_topics(self, device: BaseDevice) -> None:
        for topic in device.device_info.topics():
            self.__topic_device_map[topic] = device

    def _unregister_device_topics(self, device: BaseDevice) -> list[str]:
        removed = []
        for topic, dev in list(self.__topic_device_map.items()):
            if dev == device:
                removed.append(topic)
                self.__topic_device_map.pop(topic, None)
        return removed

    def add_device(self, device: BaseDevice) -> None:
        self.__devices[device.device_data.sn] = device
        self._register_device_topics(device)
        if self.connected:
            self.__client.subscribe([(t, 1) for t in device.device_info.topics()])

    def remove_device(self, device: BaseDevice) -> None:
        self.__devices.pop(device.device_data.sn, None)
        topics = self._unregister_device_topics(device)
        if self.connected and topics:
            self.__client.unsubscribe(topics)

    def is_connected(self):
        return self.__client.is_connected()

    def reconnect(self) -> bool:
        try:
            _LOGGER.info(
                f"Re-connecting to MQTT Broker {self.__mqtt_info.url}:{self.__mqtt_info.port}"
            )
            self.__client.loop_stop(True)
            self.__client.reconnect()
            self.__client.loop_start()
            return True
        except Exception as e:
            _LOGGER.error(e)
            return False

    async def _schedule_reconnect(self) -> None:
        """Wait and then attempt to reconnect."""
        await asyncio.sleep(5)
        if not self.reconnect():
            _LOGGER.error("Failed to reconnect MQTT after scheduled disconnect")

    @callback
    def _on_socket_close(self, client, userdata: Any, sock: SocketType) -> None:
        _LOGGER.warning(
            f"MQTT socket disconnected: {str(sock)} - attempting to reconnect"
        )
        self.connected = False
        if not self.reconnect():
            _LOGGER.error("Failed to reconnect MQTT after socket close")

    @callback
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            target_topics = [(topic, 1) for topic in self.__target_topics()]
            self.__client.subscribe(target_topics)
            _LOGGER.info(f"Subscribed to MQTT topics {target_topics}")
        else:
            self.__log_with_reason("connect", client, userdata, rc)

    @callback
    def _on_disconnect(self, client, userdata, rc):
        if not self.connected:
            # from homeassistant/components/mqtt/client.py
            # This function is re-entrant and may be called multiple times
            # when there is a broken pipe error.
            return
        self.connected = False
        if rc != 0:
            self.__log_with_reason("disconnect", client, userdata, rc)
            asyncio.create_task(self._schedule_reconnect())

    @callback
    def _on_message(self, client, userdata, message: MQTTMessage):
        try:
            device = self.__topic_device_map.get(message.topic)
            if device is None:
                return
            if device.update_data(message.payload, message.topic):
                sn = getattr(getattr(device, "device_data", device), "sn", "")
                _LOGGER.debug(
                    f"Message for {sn} and Topic {message.topic} : {message.payload}"
                )
        except UnicodeDecodeError as error:
            _LOGGER.error(
                f"UnicodeDecodeError: {error}. Ignoring message and waiting for the next one."
            )

    def stop(self):
        self.__client.unsubscribe(self.__target_topics())
        self.__client.loop_stop()
        self.__client.disconnect()

    def __log_with_reason(self, action: str, client, userdata, rc):
        import paho.mqtt.client as mqtt_client

        _LOGGER.error(
            f"MQTT {action}: {mqtt_client.error_string(rc)} ({self.__mqtt_info.client_id}) - {userdata}"
        )

    def publish(self, topic: str, message: PayloadType) -> None:
        try:
            info = self.__client.publish(topic, message, 1)
            _LOGGER.debug(
                "Sending "
                + str(message)
                + " :"
                + str(info)
                + "("
                + str(info.is_published())
                + ")"
            )
        except RuntimeError as error:
            _LOGGER.error(
                error, "Error on topic " + topic + " and message " + str(message)
            )
        except Exception as error:
            _LOGGER.debug(
                error, "Error on topic " + topic + " and message " + str(message)
            )

    def __target_topics(self) -> list[str]:
        return list(self.__topic_device_map.keys())
