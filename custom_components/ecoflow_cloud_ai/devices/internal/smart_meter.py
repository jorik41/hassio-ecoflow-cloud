from custom_components.ecoflow_cloud_ai.api import EcoflowApiClient
from custom_components.ecoflow_cloud_ai.devices import const, BaseDevice
from custom_components.ecoflow_cloud_ai.entities import (
    BaseSensorEntity,
    BaseNumberEntity,
    BaseSwitchEntity,
    BaseSelectEntity,
)
from custom_components.ecoflow_cloud_ai.sensor import (
    WattsSensorEntity,
    InAmpSensorEntity,
    MilliVoltSensorEntity,
    EnergySensorEntity,
    MiscBinarySensorEntity,
)


class SmartMeter(BaseDevice):
    def sensors(self, client: EcoflowApiClient) -> list[BaseSensorEntity]:
        return [
            WattsSensorEntity(
                client, self, "powGetSysGrid", const.SMART_METER_POWER_GLOBAL
            ),
            WattsSensorEntity(
                client, self, "gridConnectionPowerL1", const.SMART_METER_POWER_L1, False
            ),
            WattsSensorEntity(
                client, self, "gridConnectionPowerL2", const.SMART_METER_POWER_L2, False
            ),
            WattsSensorEntity(
                client, self, "gridConnectionPowerL3", const.SMART_METER_POWER_L3, False
            ),
            InAmpSensorEntity(
                client, self, "gridConnectionAmpL1", const.SMART_METER_IN_AMPS_L1, False
            ),
            InAmpSensorEntity(
                client, self, "gridConnectionAmpL2", const.SMART_METER_IN_AMPS_L2, False
            ),
            InAmpSensorEntity(
                client, self, "gridConnectionAmpL3", const.SMART_METER_IN_AMPS_L3, False
            ),
            MilliVoltSensorEntity(
                client, self, "gridConnectionVolL1", const.SMART_METER_VOLT_L1, False
            ),
            MilliVoltSensorEntity(
                client, self, "gridConnectionVolL2", const.SMART_METER_VOLT_L2, False
            ),
            MilliVoltSensorEntity(
                client, self, "gridConnectionVolL3", const.SMART_METER_VOLT_L3, False
            ),
            MiscBinarySensorEntity(
                client, self, "gridConnectionFlagL1", const.SMART_METER_FLAG_L1, False
            ),
            MiscBinarySensorEntity(
                client, self, "gridConnectionFlagL2", const.SMART_METER_FLAG_L2, False
            ),
            MiscBinarySensorEntity(
                client, self, "gridConnectionFlagL3", const.SMART_METER_FLAG_L3, False
            ),
            EnergySensorEntity(
                client,
                self,
                "gridConnectionDataRecord.todayActiveL1",
                const.SMART_METER_RECORD_ACTIVE_TODAY_L1,
                False,
            ),
            EnergySensorEntity(
                client,
                self,
                "gridConnectionDataRecord.todayActiveL2",
                const.SMART_METER_RECORD_ACTIVE_TODAY_L2,
                False,
            ),
            EnergySensorEntity(
                client,
                self,
                "gridConnectionDataRecord.todayActiveL3",
                const.SMART_METER_RECORD_ACTIVE_TODAY_L3,
                False,
            ),
            EnergySensorEntity(
                client,
                self,
                "gridConnectionDataRecord.todayActive",
                const.SMART_METER_RECORD_ACTIVE_TODAY,
            ),
            EnergySensorEntity(
                client,
                self,
                "gridConnectionDataRecord.todayReactive",
                const.SMART_METER_RECORD_REACTIVE_TODAY,
                False,
            ),
            EnergySensorEntity(
                client,
                self,
                "gridConnectionDataRecord.totalActiveEnergy",
                const.SMART_METER_RECORD_ACTIVE_TOTAL,
            ),
            EnergySensorEntity(
                client,
                self,
                "gridConnectionDataRecord.totalReactiveEnergy",
                const.SMART_METER_RECORD_REACTIVE_TOTAL,
            ),
        ]

    def numbers(self, client: EcoflowApiClient) -> list[BaseNumberEntity]:
        return []

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        return []

    def selects(self, client: EcoflowApiClient) -> list[BaseSelectEntity]:
        return []
