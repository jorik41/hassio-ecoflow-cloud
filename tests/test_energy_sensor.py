import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from custom_components.ecoflow_cloud_ai.sensor import EnergySensorEntity
from custom_components.ecoflow_cloud_ai.devices import EcoflowDeviceInfo
from custom_components.ecoflow_cloud_ai.device_data import DeviceData, DeviceOptions

class DummyDevice:
    def __init__(self):
        self.device_info = EcoflowDeviceInfo(
            public_api=True,
            sn="sn123",
            name="dev",
            device_type="type",
            status=0,
            data_topic="data",
            set_topic="set",
            set_reply_topic="set_reply",
            get_topic=None,
            get_reply_topic=None,
            status_topic=None,
        )
        self.device_data = DeviceData(
            sn="sn123",
            name="dev",
            device_type="type",
            options=DeviceOptions(refresh_period=10, power_step=1, diagnostic_mode=False),
            display_name=None,
            parent=None,
        )
        self.coordinator = None

    def flat_json(self):
        return True


def test_energy_sensor_unique_id_and_key():
    device = DummyDevice()
    sensor = EnergySensorEntity(object(), device, "254_32.watthPv1", "PV1 Today Energy Total")
    assert sensor.mqtt_key == "254_32.watthPv1"
    assert sensor.unique_id == "ecoflow-api-sn123-254-32-watthPv1-energy"
