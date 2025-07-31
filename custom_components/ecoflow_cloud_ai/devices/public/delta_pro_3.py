from ...api import EcoflowApiClient
from ...sensor import StatusSensorEntity
from ..internal.delta_pro_3 import DeltaPro3 as InternalDeltaPro3


class DeltaPro3(InternalDeltaPro3):
    def _status_sensor(self, client: EcoflowApiClient) -> StatusSensorEntity:
        return StatusSensorEntity(client, self)
