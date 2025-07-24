from custom_components.ecoflow_cloud.api import EcoflowApiClient
from custom_components.ecoflow_cloud.entities import (
    BaseNumberEntity,
    BaseSelectEntity,
    BaseSensorEntity,
    BaseSwitchEntity,
)
from custom_components.ecoflow_cloud.number import (
    BatteryBackupLevel,
    ChargingPowerEntity,
    MaxBatteryLevelEntity,
    MaxGenStopLevelEntity,
    MinBatteryLevelEntity,
    MinGenStartLevelEntity,
)
from custom_components.ecoflow_cloud.sensor import (
    CapacitySensorEntity,
    InWattsSensorEntity,
    LevelSensorEntity,
    OutWattsSensorEntity,
    RemainSensorEntity,
    TempSensorEntity,
    VoltSensorEntity,
    AmpSensorEntity,
    FrequencySensorEntity,
)
from custom_components.ecoflow_cloud.switch import BeeperEntity, EnabledEntity
from custom_components.ecoflow_cloud.devices import BaseDevice, const


class DeltaPro3(BaseDevice):
    def sensors(self, client: EcoflowApiClient) -> list[BaseSensorEntity]:
        return [
            LevelSensorEntity(
                client, self, "bmsBattSoc", const.MAIN_BATTERY_LEVEL
            ).attr("bmsDesignCap", const.ATTR_DESIGN_CAPACITY, 0),
            CapacitySensorEntity(
                client, self, "bmsDesignCap", const.MAIN_DESIGN_CAPACITY, False
            ),
            LevelSensorEntity(client, self, "bmsBattSoh", const.SOH),
            RemainSensorEntity(client, self, "bmsChgRemTime", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, self, "bmsDsgRemTime", const.DISCHARGE_REMAINING_TIME),
            TempSensorEntity(client, self, "bmsMinCellTemp", const.MIN_CELL_TEMP, False),
            TempSensorEntity(client, self, "bmsMaxCellTemp", const.MAX_CELL_TEMP, False),
            TempSensorEntity(client, self, "bmsMinMosTemp", const.MIN_MOS_TEMP, False),
            TempSensorEntity(client, self, "bmsMaxMosTemp", const.MAX_MOS_TEMP, False),
            LevelSensorEntity(client, self, "cmsBattSoc", const.COMBINED_BATTERY_LEVEL),
            LevelSensorEntity(client, self, "cmsBattSoh", const.SOH),
            InWattsSensorEntity(client, self, "powInSumW", const.TOTAL_IN_POWER),
            OutWattsSensorEntity(client, self, "powOutSumW", const.TOTAL_OUT_POWER),
            InWattsSensorEntity(client, self, "powGetAcIn", const.AC_IN_POWER),
            OutWattsSensorEntity(client, self, "powGetAc", const.AC_OUT_POWER),
            InWattsSensorEntity(client, self, "powGetPvL", const.SOLAR_IN_POWER),
            InWattsSensorEntity(client, self, "powGetPvH", const.PV_HV_POWER),
            OutWattsSensorEntity(client, self, "powGetAcHvOut", const.AC_HV_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetTypec1", const.TYPEC_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetTypec2", const.TYPEC_2_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGet12v", const.DC_12V_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGet24v", const.DC_24V_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetAcLvOut", const.AC_LV_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetAcLvTt30Out", const.AC_LV_TT30_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGet5p8", const.POWER_INOUT_PORT),
            OutWattsSensorEntity(client, self, "powGetQcusb1", const.USB_QC_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetQcusb2", const.USB_QC_2_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGet4p81", const.EXTRA_BATTERY_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGet4p82", const.EXTRA_BATTERY_2_OUT_POWER),
            FrequencySensorEntity(client, self, "acOutFreq", const.AC_FREQUENCY),
            VoltSensorEntity(client, self, "plugInInfoPvHChgVolMax", const.PV_VOLTAGE, False),
            AmpSensorEntity(client, self, "plugInInfoPvHChgAmpMax", const.PV_CURRENT, False),
            VoltSensorEntity(client, self, "plugInInfoPvLChgVolMax", const.PV_VOLTAGE, False),
            AmpSensorEntity(client, self, "plugInInfoPvLChgAmpMax", const.PV_CURRENT, False),
            RemainSensorEntity(client, self, "cmsChgRemTime", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, self, "cmsDsgRemTime", const.DISCHARGE_REMAINING_TIME),
        ]

    def numbers(self, client: EcoflowApiClient) -> list[BaseNumberEntity]:
        return [
            MaxBatteryLevelEntity(
                client,
                self,
                "cmsMaxChgSoc",
                const.MAX_CHARGE_LEVEL,
                50,
                100,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgMaxChgSoc": value},
                },
            ),
            MinBatteryLevelEntity(
                client,
                self,
                "cmsMinDsgSoc",
                const.MIN_DISCHARGE_LEVEL,
                0,
                30,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgMinDsgSoc": value},
                },
            ),
            BatteryBackupLevel(
                client,
                self,
                "energyBackupStartSoc",
                const.BACKUP_RESERVE_LEVEL,
                5,
                100,
                "cmsMinDsgSoc",
                "cmsMaxChgSoc",
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {
                        "cfgEnergyBackup": {
                            "energyBackupStartSoc": int(value),
                            "energyBackupEn": True,
                        }
                    },
                },
            ),
            MinGenStartLevelEntity(
                client,
                self,
                "cmsOilOnSoc",
                const.GEN_AUTO_START_LEVEL,
                0,
                30,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgCmsOilOnSoc": value},
                },
            ),
            MaxGenStopLevelEntity(
                client,
                self,
                "cmsOilOffSoc",
                const.GEN_AUTO_STOP_LEVEL,
                50,
                100,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgCmsOilOffSoc": value},
                },
            ),
            ChargingPowerEntity(
                client,
                self,
                "cfgPlugInInfoAcInChgPowMax",
                const.AC_CHARGING_POWER,
                400,
                2900,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgPlugInInfoAcInChgPowMax": value},
                },
            ),
        ]

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        return [
            BeeperEntity(
                client,
                self,
                "enBeep",
                const.BEEPER,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgBeepEn": value},
                },
            ),
            EnabledEntity(
                client,
                self,
                "flowInfo12v",
                const.DC_ENABLED,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgDc12vOutOpen": value},
                },
                enableValue=2,
            ),
            EnabledEntity(
                client,
                self,
                "flowInfoAcHvOut",
                const.AC_ENABLED,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgHvAcOutOpen": value},
                },
                enableValue=2,
            ),
            EnabledEntity(
                client,
                self,
                "xboostEn",
                const.XBOOST_ENABLED,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "cmdFunc": 254,
                    "dest": 2,
                    "params": {"cfgXboostEn": value},
                },
            ),
        ]

    def selects(self, client: EcoflowApiClient) -> list[BaseSelectEntity]:
        return []
