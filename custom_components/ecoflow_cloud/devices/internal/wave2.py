from custom_components.ecoflow_cloud.switch import (
    EnabledEntity,
    InvertedBeeperEntity,
    BaseSwitchEntity,
)

from custom_components.ecoflow_cloud.api import EcoflowApiClient
from custom_components.ecoflow_cloud.devices import const, BaseDevice
from custom_components.ecoflow_cloud.entities import BaseSensorEntity, BaseNumberEntity, BaseSelectEntity
from custom_components.ecoflow_cloud.number import SetTempEntity, ValueUpdateEntity
from custom_components.ecoflow_cloud.select import DictSelectEntity, TimeoutDictSelectEntity
from custom_components.ecoflow_cloud.sensor import (
    LevelSensorEntity,
    RemainSensorEntity,
    TempSensorEntity,
    WattsSensorEntity,
    MilliCelsiusSensorEntity,
    CapacitySensorEntity,
    QuotaStatusSensorEntity,
    CentivoltSensorEntity,
    DecivoltSensorEntity,
    DecihertzSensorEntity,
    MilliampSensorEntity,
    EnumSensorEntity,
    FanSensorEntity,
)


class Wave2(BaseDevice):
    def sensors(self, client: EcoflowApiClient) -> list[BaseSensorEntity]:
        return [
            # Power and Battery Entities
            LevelSensorEntity(client, self, "bms.soc", const.MAIN_BATTERY_LEVEL)
            .attr("bms.remainCap", const.ATTR_REMAIN_CAPACITY, 0),
            CapacitySensorEntity(client, self, "bms.remainCap", const.MAIN_REMAIN_CAPACITY, False),

            TempSensorEntity(client, self, "bms.tmp", const.BATTERY_TEMP)
            .attr("bms.minCellTemp", const.ATTR_MIN_CELL_TEMP, 0)
            .attr("bms.maxCellTemp", const.ATTR_MAX_CELL_TEMP, 0),
            TempSensorEntity(client, self, "bms.minCellTmp", const.MIN_CELL_TEMP, False),
            TempSensorEntity(client, self, "bms.maxCellTmp", const.MAX_CELL_TEMP, False),

            RemainSensorEntity(client, self, "pd.batChgRemain", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, self, "pd.batDsgRemain", const.DISCHARGE_REMAINING_TIME),

            # heat pump
            MilliCelsiusSensorEntity(client, self, "pd.condTemp", "Condensation temperature", False),
            MilliCelsiusSensorEntity(client, self, "pd.heatEnv", "Return air temperature in condensation zone", False),
            MilliCelsiusSensorEntity(client, self, "pd.coolEnv", "Air outlet temperature", False),
            MilliCelsiusSensorEntity(client, self, "pd.evapTemp", "Evaporation temperature", False),
            MilliCelsiusSensorEntity(client, self, "pd.motorOutTemp", "Exhaust temperature", False),
            MilliCelsiusSensorEntity(client, self, "pd.airInTemp", "Evaporation zone return air temperature", False),

            TempSensorEntity(client, self, "pd.coolTemp", "Air outlet temperature", False),
            TempSensorEntity(client, self, "pd.envTemp", "Ambient temperature", False),

            FanSensorEntity(client, self, "motor.condeFanRpm", const.CONDENSER_FAN_RPM, False),
            FanSensorEntity(client, self, "motor.evapFanRpm", const.EVAP_FAN_RPM, False),
            BaseSensorEntity(client, self, "motor.fourWayState", const.FOUR_WAY_VALVE, False),

            LevelSensorEntity(client, self, "pd.batSoc", const.BATTERY_LEVEL_SOC),
            CentivoltSensorEntity(client, self, "pd.batVolt", const.BATTERY_VOLT, False),
            MilliampSensorEntity(client, self, "pd.batCurr", const.BATTERY_AMP, False),
            CentivoltSensorEntity(client, self, "pd.mpptVol", const.PV_VOLTAGE, False),
            MilliampSensorEntity(client, self, "pd.mpptCur", const.PV_CURRENT, False),
            DecihertzSensorEntity(client, self, "pd.acFreq", const.AC_FREQUENCY),
            DecivoltSensorEntity(client, self, "pd.acVoltRms", const.AC_VOLT_RMS),
            MilliampSensorEntity(client, self, "pd.acCurrRms", const.AC_CURR_RMS),
            DecivoltSensorEntity(client, self, "power.busVol", const.BUS_VOLTAGE),
            EnumSensorEntity(client, self, "pd.mpptWork", const.MPPT_WORK, const.MPPT_WORK_OPTIONS),

            # power (pd)
            WattsSensorEntity(client, self, "pd.mpptPwr", const.PV_INPUT_POWER),
            WattsSensorEntity(client, self, "pd.batPwrOut", "Battery output power"),
            WattsSensorEntity(client, self, "pd.pvPower", const.PV_CHARGING_POWER),
            WattsSensorEntity(client, self, "pd.acPwrIn", "AC input power"),
            WattsSensorEntity(client, self, "pd.psdrPower", "Power supply power"),
            WattsSensorEntity(client, self, "pd.sysPowerWatts", "System power"),
            WattsSensorEntity(client, self, "pd.batPower", "Battery power"),

            # power (motor)
            WattsSensorEntity(client, self, "motor.power", "Motor operating power"),

            # power (power)
            WattsSensorEntity(client, self, "power.batPwrOut", "Battery output power"),
            WattsSensorEntity(client, self, "power.acPwrIn", "AC input power"),
            WattsSensorEntity(client, self, "power.mpptPwr", const.PV_INPUT_POWER),

            QuotaStatusSensorEntity(client, self)
        ]

    def numbers(self, client: EcoflowApiClient) -> list[BaseNumberEntity]:
        return [
            SetTempEntity(client, self, "pd.setTemp", "Set Temperature", 0, 40,
                          lambda value: {"moduleType": 1, "operateType": "setTemp",
                                         "sn": self.device_info.sn,
                                         "params": {"setTemp": int(value)}}),
            ValueUpdateEntity(
                client,
                self,
                "pd.timeSet",
                const.TIMER_DURATION,
                0,
                65535,
                lambda value: {
                    "moduleType": 1,
                    "operateType": "sacTiming",
                    "sn": self.device_info.sn,
                    "params": {"timeSet": int(value), "timeEn": 1},
                },
            ),
        ]

    def selects(self, client: EcoflowApiClient) -> list[BaseSelectEntity]:
        return [
            DictSelectEntity(client, self, "pd.fanValue", const.FAN_MODE, const.FAN_MODE_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "fanValue",
                                            "sn": self.device_info.sn,
                                            "params": {"fanValue": value}}),
            DictSelectEntity(client, self, "pd.mainMode", const.MAIN_MODE, const.MAIN_MODE_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "mainMode",
                                            "sn": self.device_info.sn,
                                            "params": {"mainMode": value}}),
            DictSelectEntity(client, self, "pd.powerMode", const.REMOTE_MODE, const.REMOTE_MODE_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "powerMode",
                                            "sn": self.device_info.sn,
                                            "params": {"powerMode": value}}),
            DictSelectEntity(client, self, "pd.subMode", const.POWER_SUB_MODE, const.POWER_SUB_MODE_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "subMode",
                                            "sn": self.device_info.sn,
                                            "params": {"subMode": value}}),
            DictSelectEntity(client, self, "pd.tempSys", const.TEMP_SYS, const.TEMP_SYS_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "tempSys",
                                            "sn": self.device_info.sn,
                                            "params": {"mode": value}}),
            DictSelectEntity(client, self, "pd.tempDisplay", const.TEMP_DISPLAY, const.TEMP_DISPLAY_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "tempDisplay",
                                            "sn": self.device_info.sn,
                                            "params": {"tempDisplay": value}}),
            DictSelectEntity(client, self, "pd.rgbState", const.RGB_STATE, const.RGB_STATE_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "rgbState",
                                            "sn": self.device_info.sn,
                                            "params": {"rgbState": value}}),
            DictSelectEntity(client, self, "pd.wteFthEn", const.AUTO_DRAIN, const.AUTO_DRAIN_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "wteFthEn",
                                            "sn": self.device_info.sn,
                                            "params": {"wteFthEn": value}}),
            TimeoutDictSelectEntity(client, self, "pd.idleTime", const.SCREEN_TIMEOUT, const.SCREEN_TIMEOUT_OPTIONS,
                                   lambda value: {"moduleType": 1, "operateType": "display",
                                                  "sn": self.device_info.sn,
                                                  "params": {"idleTime": value,
                                                             "idleMode": 0 if value == 0 else 1}}),
        ]

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        return [
            InvertedBeeperEntity(
                client,
                self,
                "pd.beepEn",
                const.BEEPER,
                lambda value: {
                    "moduleType": 1,
                    "operateType": "beepEn",
                    "sn": self.device_info.sn,
                    "params": {"en": value},
                },
            ),
            EnabledEntity(
                client,
                self,
                "pd.timeEn",
                const.TIMER_ENABLED,
                lambda value, params: {
                    "moduleType": 1,
                    "operateType": "sacTiming",
                    "sn": self.device_info.sn,
                    "params": {"timeEn": value, "timeSet": int(params.get("pd.timeSet", 0))},
                },
            ),
        ]
