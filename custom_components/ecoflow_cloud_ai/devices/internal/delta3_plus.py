from custom_components.ecoflow_cloud_ai.api import EcoflowApiClient
from custom_components.ecoflow_cloud_ai.devices import const
from custom_components.ecoflow_cloud_ai.entities import BaseSwitchEntity
from custom_components.ecoflow_cloud_ai.switch import EnabledEntity
from .delta3 import Delta3
from .delta_pro_3 import DeltaPro3SetMessage


class Delta3Plus(Delta3):
    """Device class for Delta 3 Plus.

    The AC output does not expose separate high- or low-voltage modes.
    Instead, the generic ``acOutCfg`` command toggles power delivery.
    The current state can be read from ``flowInfoAcOut``.
    """

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        switches = super().switches(client)
        switches.extend(
            [
                EnabledEntity(
                    client,
                    self,
                    "flowInfoAcOut",
                    const.AC_ENABLED,
                    lambda value: {
                        "moduleType": 5,
                        "operateType": "acOutCfg",
                        "params": {
                            "enabled": value,
                            "out_voltage": -1,
                            "out_freq": 255,
                            "xboost": 255,
                        },
                    },
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
