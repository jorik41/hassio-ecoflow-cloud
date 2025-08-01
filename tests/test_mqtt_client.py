import os
import sys
from types import SimpleNamespace
from unittest.mock import Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from custom_components.ecoflow_cloud_ai.api.ecoflow_mqtt import EcoflowMQTTClient
from custom_components.ecoflow_cloud_ai.api import EcoflowMqttInfo
from custom_components.ecoflow_cloud_ai.devices import EcoflowDeviceInfo

class DummyAsyncClient:
    def __init__(self, *args, **kwargs):
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        self.on_socket_close = None
        self.subscribed = []
        self.unsubscribed = []

    def setup(self):
        pass

    def username_pw_set(self, *a, **k):
        pass

    def tls_set(self, *a, **k):
        pass

    def tls_insecure_set(self, *a, **k):
        pass

    def connect(self, *a, **k):
        pass

    def loop_start(self):
        pass

    def subscribe(self, topics):
        self.subscribed.extend(topics)

    def unsubscribe(self, topics):
        self.unsubscribed.extend(topics)

    def loop_stop(self, *a, **k):
        pass

    def disconnect(self):
        pass

    def is_connected(self):
        return True

    def reconnect(self):
        return True

    def publish(self, *a, **k):
        pass

def make_device(sn):
    info = EcoflowDeviceInfo(
        public_api=True,
        sn=sn,
        name=sn,
        device_type="type",
        status=0,
        data_topic=f"{sn}/data",
        set_topic=f"{sn}/set",
        set_reply_topic=f"{sn}/set_reply",
        get_topic=f"{sn}/get",
        get_reply_topic=f"{sn}/get_reply",
        status_topic=None,
    )
    dev = SimpleNamespace(device_info=info, device_data=SimpleNamespace(sn=sn))
    dev.update_data = Mock(return_value=True)
    return dev

@pytest.fixture(autouse=True)
def patch_client(monkeypatch):
    monkeypatch.setattr(
        "homeassistant.components.mqtt.async_client.AsyncMQTTClient", DummyAsyncClient
    )


def test_topic_dispatch(monkeypatch):
    info = EcoflowMqttInfo("localhost", 1883, "u", "p")
    d1 = make_device("sn1")
    d2 = make_device("sn2")
    client = EcoflowMQTTClient(info, {"sn1": d1, "sn2": d2})
    assert client._EcoflowMQTTClient__topic_device_map[d1.device_info.data_topic] == d1
    msg = SimpleNamespace(payload=b"data", topic=d1.device_info.data_topic)
    client._on_message(None, None, msg)
    d1.update_data.assert_called_with(b"data", d1.device_info.data_topic)
    d2.update_data.assert_not_called()


def test_add_remove_device(monkeypatch):
    info = EcoflowMqttInfo("localhost", 1883, "u", "p")
    d1 = make_device("sn1")
    client = EcoflowMQTTClient(info, {"sn1": d1})
    d2 = make_device("sn2")
    client.add_device(d2)
    assert client._EcoflowMQTTClient__topic_device_map[d2.device_info.data_topic] == d2
    client.remove_device(d2)
    assert d2.device_info.data_topic not in client._EcoflowMQTTClient__topic_device_map

