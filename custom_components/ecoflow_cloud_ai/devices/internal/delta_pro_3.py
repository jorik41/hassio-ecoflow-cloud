from custom_components.ecoflow_cloud_ai.api import EcoflowApiClient
from custom_components.ecoflow_cloud_ai.api.message import JSONMessage, Message
from custom_components.ecoflow_cloud_ai.api.private_api import PrivateAPIMessageProtocol
from custom_components.ecoflow_cloud_ai.entities import (
    BaseNumberEntity,
    BaseSelectEntity,
    BaseSensorEntity,
    BaseSwitchEntity,
)
from custom_components.ecoflow_cloud_ai.number import (
    BatteryBackupLevel,
    ChargingPowerEntity,
    MaxBatteryLevelEntity,
    MaxGenStopLevelEntity,
    MinBatteryLevelEntity,
    MinGenStartLevelEntity,
)
from custom_components.ecoflow_cloud_ai.sensor import (
    AmpSensorEntity,
    CapacitySensorEntity,
    CyclesSensorEntity,
    FrequencySensorEntity,
    InMilliVoltSensorEntity,
    InMilliampSolarSensorEntity,
    InProtectedEnergySensorEntity,
    InProtectedEnergySolarSensorEntity,
    InVoltSensorEntity,
    InVoltSolarSensorEntity,
    InWattsSensorEntity,
    InWattsSolarSensorEntity,
    LevelSensorEntity,
    MilliVoltSensorEntity,
    InEnergySensorEntity,
    OutEnergySensorEntity,
    OutProtectedEnergySensorEntity,
    OutVoltDcSensorEntity,
    OutVoltSensorEntity,
    OutWattsDcSensorEntity,
    OutWattsSensorEntity,
    QuotaStatusSensorEntity,
    RemainSensorEntity,
    TempSensorEntity,
    VoltSensorEntity,
)
from custom_components.ecoflow_cloud_ai.switch import BeeperEntity, EnabledEntity
from custom_components.ecoflow_cloud_ai.devices import BaseDevice, const
from ..internal.proto import deltapro3_pb2


class DeltaPro3SetMessage(Message, PrivateAPIMessageProtocol):
    def __init__(
        self, device_sn: str, field: str, value: int, data_len: int | None = None
    ) -> None:
        super().__init__()
        self.device_sn = device_sn
        self.field = field
        self.value = value
        self.data_len = data_len

    def _build(self) -> deltapro3_pb2.setMessage:
        msg = deltapro3_pb2.setMessage()
        header = msg.header
        header.src = 32
        header.dest = 2
        header.d_src = 1
        header.d_dest = 1
        header.enc_type = 1
        header.check_type = 3
        header.cmd_func = 254
        header.cmd_id = 17
        header.need_ack = 1
        header.seq = JSONMessage.gen_seq()
        header.version = 19
        header.payload_ver = 1
        # The generated protobuf uses the reserved word "from" as a field name.
        # Since Python does not allow using "from" directly as an attribute, use
        # ``setattr`` to set the value.
        setattr(header, "from", "HomeAssistant")
        header.device_sn = self.device_sn
        setattr(header.pdata, self.field, int(self.value))
        if self.data_len is None:
            header.data_len = header.pdata.ByteSize()
        else:
            header.data_len = self.data_len
        return msg

    def private_api_to_mqtt_payload(self):
        return self._build().SerializeToString()

    def to_mqtt_payload(self):
        return self.private_api_to_mqtt_payload()


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
            RemainSensorEntity(
                client, self, "bmsChgRemTime", const.CHARGE_REMAINING_TIME
            ),
            RemainSensorEntity(
                client, self, "bmsDsgRemTime", const.DISCHARGE_REMAINING_TIME
            ),
            TempSensorEntity(
                client, self, "bmsMinCellTemp", const.MIN_CELL_TEMP, False
            ),
            TempSensorEntity(
                client, self, "bmsMaxCellTemp", const.MAX_CELL_TEMP, False
            ),
            TempSensorEntity(client, self, "bmsMinMosTemp", const.MIN_MOS_TEMP, False),
            TempSensorEntity(client, self, "bmsMaxMosTemp", const.MAX_MOS_TEMP, False),
            MilliVoltSensorEntity(
                client, self, "bmsBattVol", const.BATTERY_VOLT, False
            )
            .attr("bmsMinCellVol", const.ATTR_MIN_CELL_VOLT, 0)
            .attr("bmsMaxCellVol", const.ATTR_MAX_CELL_VOLT, 0),
            MilliVoltSensorEntity(
                client, self, "bmsMinCellVol", const.MIN_CELL_VOLT, False
            ),
            MilliVoltSensorEntity(
                client, self, "bmsMaxCellVol", const.MAX_CELL_VOLT, False
            ),
            AmpSensorEntity(
                client, self, "bmsBattAmp", const.MAIN_BATTERY_CURRENT, False
            ),
            CyclesSensorEntity(client, self, "cycles", const.CYCLES),
            CapacitySensorEntity(
                client, self, "bmsFullCap", const.MAIN_FULL_CAPACITY, False
            ),
            CapacitySensorEntity(
                client, self, "bmsRemainCap", const.MAIN_REMAIN_CAPACITY, False
            ),
            LevelSensorEntity(client, self, "cmsBattSoc", const.COMBINED_BATTERY_LEVEL),
            LevelSensorEntity(client, self, "cmsBattSoh", const.SOH),
            InWattsSensorEntity(client, self, "powInSumW", const.TOTAL_IN_POWER),
            OutWattsSensorEntity(client, self, "powOutSumW", const.TOTAL_OUT_POWER),
            InWattsSensorEntity(client, self, "powGetAcIn", const.AC_IN_POWER),
            OutWattsSensorEntity(client, self, "powGetAc", const.AC_OUT_POWER),
            InWattsSolarSensorEntity(
                client, self, "powGetPvL", const.SOLAR_IN_POWER
            ),
            InWattsSolarSensorEntity(
                client, self, "powGetPvH", const.PV_HV_POWER
            ),
            OutWattsSensorEntity(client, self, "powGetAcHvOut", const.AC_HV_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetTypec1", const.TYPEC_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetTypec2", const.TYPEC_2_OUT_POWER),
            OutWattsDcSensorEntity(client, self, "powGet12v", const.DC_12V_OUT_POWER),
            OutWattsDcSensorEntity(client, self, "powGet24v", const.DC_24V_OUT_POWER),
            OutVoltDcSensorEntity(client, self, "powGet12vVol", "12V DC Output Voltage"),
            OutVoltDcSensorEntity(client, self, "powGet24vVol", "24V DC Output Voltage"),
            OutWattsSensorEntity(client, self, "powGetAcLvOut", const.AC_LV_OUT_POWER),
            OutWattsSensorEntity(
                client, self, "powGetAcLvTt30Out", const.AC_LV_TT30_OUT_POWER
            ),
            OutWattsDcSensorEntity(client, self, "powGet5p8", const.POWER_INOUT_PORT),
            OutWattsSensorEntity(
                client, self, "powGetQcusb1", const.USB_QC_1_OUT_POWER
            ),
            OutWattsSensorEntity(
                client, self, "powGetQcusb2", const.USB_QC_2_OUT_POWER
            ),
            OutWattsDcSensorEntity(
                client, self, "powGet4p81", const.EXTRA_BATTERY_1_OUT_POWER
            ),
            OutWattsDcSensorEntity(
                client, self, "powGet4p82", const.EXTRA_BATTERY_2_OUT_POWER
            ),
            LevelSensorEntity(client, self, "cmsMaxChgSoc", const.MAX_CHARGE_LEVEL),
            LevelSensorEntity(client, self, "cmsMinDsgSoc", const.MIN_DISCHARGE_LEVEL),
            InProtectedEnergySensorEntity(client, self, "powGetAcIn", const.AC_IN_ENERGY),
            InProtectedEnergySolarSensorEntity(client, self, "powGetPvL", const.SOLAR_IN_ENERGY),
            InProtectedEnergySensorEntity(client, self, "powGetPvH", const.PV_HV_ENERGY),
            OutProtectedEnergySensorEntity(client, self, "powGet5p8", const.POWER_INOUT_PORT_ENERGY),
            OutProtectedEnergySensorEntity(client, self, "powGet4p81", const.EXTRA_BATTERY_1_ENERGY),
            OutProtectedEnergySensorEntity(client, self, "powGet4p82", const.EXTRA_BATTERY_2_ENERGY),
            OutProtectedEnergySensorEntity(client, self, "powGetAc", const.DISCHARGE_AC_ENERGY),
            InProtectedEnergySensorEntity(client, self, "powInSumW", const.TOTAL_IN_ENERGY),
            OutProtectedEnergySensorEntity(client, self, "powOutSumW", const.TOTAL_OUT_ENERGY),
            InEnergySensorEntity(
                client, self, "powInSumEnergy", "Total Input Energy"
            ),
            OutEnergySensorEntity(
                client, self, "powOutSumEnergy", "Total Output Energy"
            ),
            InEnergySensorEntity(
                client, self, "acInEnergyTotal", const.CHARGE_AC_ENERGY
            ),
            OutEnergySensorEntity(
                client, self, "acOutEnergyTotal", const.DISCHARGE_AC_ENERGY
            ),
            InEnergySensorEntity(
                client, self, "pvInEnergyTotal", const.SOLAR_IN_ENERGY
            ),
            OutEnergySensorEntity(
                client, self, "dcOutEnergyTotal", const.DISCHARGE_DC_ENERGY
            ),
            FrequencySensorEntity(client, self, "acOutFreq", const.AC_FREQUENCY),
            InMilliVoltSensorEntity(client, self, "plugInInfoAcInVol", const.AC_IN_VOLT),
            InMilliampSolarSensorEntity(client, self, "plugInInfoAcInAmp", "AC Input Current"),
            OutVoltSensorEntity(client, self, "plugInInfoAcOutVol", const.AC_OUT_VOLT),
            VoltSensorEntity(
                client, self, "plugInInfoPvHChgVolMax", const.PV_VOLTAGE, False
            ),
            AmpSensorEntity(
                client, self, "plugInInfoPvHChgAmpMax", const.PV_CURRENT, False
            ),
            VoltSensorEntity(
                client, self, "plugInInfoPvLChgVolMax", const.PV_VOLTAGE, False
            ),
            AmpSensorEntity(
                client, self, "plugInInfoPvLChgAmpMax", const.PV_CURRENT, False
            ),
            InVoltSolarSensorEntity(
                client, self, "powGetPvHVol", "Solar HV Input Voltage"
            ),
            InVoltSolarSensorEntity(
                client, self, "powGetPvLVol", "Solar LV Input Voltage"
            ),
            InMilliampSolarSensorEntity(
                client, self, "powGetPvHAmp", const.SOLAR_IN_CURRENT
            ),
            InMilliampSolarSensorEntity(
                client, self, "powGetPvLAmp", const.SOLAR_IN_CURRENT
            ),
            RemainSensorEntity(
                client, self, "cmsChgRemTime", const.CHARGE_REMAINING_TIME
            ),
            RemainSensorEntity(
                client, self, "cmsDsgRemTime", const.DISCHARGE_REMAINING_TIME
            ),
            QuotaStatusSensorEntity(client, self),
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
                lambda value: DeltaPro3SetMessage(
                    self.device_info.sn, "cmsMaxChgSoc", value
                ),
            ),
            MinBatteryLevelEntity(
                client,
                self,
                "cmsMinDsgSoc",
                const.MIN_DISCHARGE_LEVEL,
                0,
                30,
                lambda value: DeltaPro3SetMessage(
                    self.device_info.sn, "cmsMinDsgSoc", value
                ),
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
                "plugInInfoAcInChgPowMax",
                const.AC_CHARGING_POWER,
                400,
                2900,

                lambda value: DeltaPro3SetMessage(
                    self.device_info.sn, "plugInInfoAcInChgPowMax", value
                ),

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
                lambda value: DeltaPro3SetMessage(
                    self.device_info.sn, "cfgDc12vOutOpen", value
                ),
                enableValue=2,
            ),
            EnabledEntity(
                client,
                self,
                "flowInfoAcHvOut",
                const.AC_ENABLED,
                lambda value: DeltaPro3SetMessage(
                    self.device_info.sn, "cfgHvAcOutOpen", value
                ),
                enableValue=2,
            ),
            EnabledEntity(
                client,
                self,
                "xboostEn",
                const.XBOOST_ENABLED,
                lambda value: DeltaPro3SetMessage(
                    self.device_info.sn, "xboostEn", value
                ),
            ),
        ]

    def selects(self, client: EcoflowApiClient) -> list[BaseSelectEntity]:
        return []
