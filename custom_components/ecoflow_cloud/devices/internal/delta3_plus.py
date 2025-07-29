from custom_components.ecoflow_cloud.api import EcoflowApiClient
from custom_components.ecoflow_cloud.devices import const
from custom_components.ecoflow_cloud.entities import BaseSwitchEntity
from custom_components.ecoflow_cloud.switch import EnabledEntity
from .delta3 import Delta3
from .delta_pro_3 import DeltaPro3SetMessage


class Delta3Plus(Delta3):
    """Device class for Delta 3 Plus."""

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        switches = super().switches(client)
        switches.extend(
            [
                EnabledEntity(
                    client,
                    self,
                    "flowInfoAcOut",
                    const.AC_ENABLED,
                    lambda value: DeltaPro3SetMessage(
                        self.device_info.sn, "cfgAcOutOpen", value
                    ),
                    enableValue=2,
                ),
                EnabledEntity(
                    client,
                    self,
                    "flowInfo12v",
                    const.DC_ENABLED,
                    lambda value: DeltaPro3SetMessage(
                        self.device_info.sn, "cfgDc12vOutOpen", value
                    ),
                    enableValue=2,
                ),
            ]
        )
        return switches
