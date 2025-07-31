from ...api import EcoflowApiClient
from ...sensor import StatusSensorEntity
from ..internal.delta3_plus import Delta3Plus as InternalDelta3Plus
from .data_bridge import to_plain


class Delta3Plus(InternalDelta3Plus):
    """Public API device class for Delta 3 Plus."""

    def _prepare_data(self, raw_data) -> dict[str, any]:
        res = super()._prepare_data(raw_data)
        res = to_plain(res)
        return res

    def _status_sensor(self, client: EcoflowApiClient) -> StatusSensorEntity:
        return StatusSensorEntity(client, self)
