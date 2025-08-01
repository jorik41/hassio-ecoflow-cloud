import logging
from collections.abc import Sequence
from typing import Any, cast, override

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.util import dt

from custom_components.ecoflow_cloud_ai.devices import const
from custom_components.ecoflow_cloud_ai.select import PowerDictSelectEntity

from ...devices import BaseDevice, EcoflowDeviceInfo
from ...device_data import DeviceData
from ...devices.internal.proto.support import (
    to_lower_camel_case,
)

from ...api import EcoflowApiClient
from ...api.message import JSONDict
from ...number import (
    BrightnessLevelEntity,
    DeciChargingPowerEntity,
    MaxBatteryLevelEntity,
    MinBatteryLevelEntity,
)
from ...sensor import (
    CelsiusSensorEntity,
    CentivoltSensorEntity,
    DeciampSensorEntity,
    DecicelsiusSensorEntity,
    DecihertzSensorEntity,
    DecivoltSensorEntity,
    DeciwattsSensorEntity,
    InWattsSolarSensorEntity,
    SignalStrengthSensorEntity,
    LevelSensorEntity,
    MilliampSensorEntity,
    MiscSensorEntity,
    QuotaStatusSensorEntity,
    RemainSensorEntity,
    ResettingInEnergySensorEntity,
    ResettingInEnergySolarSensorEntity,
    ResettingOutEnergySensorEntity,
    StatusSensorEntity,
)

from google.protobuf.message import Message as ProtoMessageRaw

from ...switch import EnabledEntity
from ..internal.proto import platform_pb2 as platform
from ..internal.proto import powerstream_pb2 as powerstream
from ..internal.proto import wn511_socket_sys_pb2 as socket_sys
from ..internal.proto import AddressId, Command, ProtoMessage
from .proto import PrivateAPIProtoDeviceMixin
from .proto.support.const import WatthType, get_expected_payload_type

_LOGGER = logging.getLogger(__name__)


def build_command(
    device_sn: str, command: Command, payload: ProtoMessageRaw
) -> ProtoMessage:
    return ProtoMessage(
        device_sn=device_sn,
        command=command,
        payload=payload,
        src=AddressId.APP,
        dest=AddressId.MQTT,
    )


class PowerStream(PrivateAPIProtoDeviceMixin, BaseDevice):
    def __init__(self, device_info: EcoflowDeviceInfo, device_data: DeviceData):
        super().__init__(device_info, device_data)
        self._client: EcoflowApiClient | None = None
        self._last_energy_req = dt.utcnow().replace(year=2000)

    @override
    def sensors(self, client: EcoflowApiClient) -> Sequence[SensorEntity]:
        self._client = client
        return [
            InWattsSolarSensorEntity(
                client, self, "20_1.pv1InputWatts", "Solar 1 Watts"
            ),
            DecivoltSensorEntity(
                client, self, "20_1.pv1InputVolt", "Solar 1 Input Potential"
            ),
            CentivoltSensorEntity(
                client, self, "20_1.pv1OpVolt", "Solar 1 Op Potential"
            ),
            DeciampSensorEntity(client, self, "20_1.pv1InputCur", "Solar 1 Current"),
            DecicelsiusSensorEntity(
                client, self, "20_1.pv1Temp", "Solar 1 Temperature"
            ),
            MiscSensorEntity(
                client, self, "20_1.pv1RelayStatus", "Solar 1 Relay Status"
            ),
            MiscSensorEntity(
                client, self, "20_1.pv1ErrCode", "Solar 1 Error Code", False
            ),
            MiscSensorEntity(
                client, self, "20_1.pv1WarnCode", "Solar 1 Warning Code", False
            ),
            MiscSensorEntity(client, self, "20_1.pv1Status", "Solar 1 Status", False),
            InWattsSolarSensorEntity(
                client, self, "20_1.pv2InputWatts", "Solar 2 Watts"
            ),
            DecivoltSensorEntity(
                client, self, "20_1.pv2InputVolt", "Solar 2 Input Potential"
            ),
            CentivoltSensorEntity(
                client, self, "20_1.pv2OpVolt", "Solar 2 Op Potential"
            ),
            DeciampSensorEntity(client, self, "20_1.pv2InputCur", "Solar 2 Current"),
            DecicelsiusSensorEntity(
                client, self, "20_1.pv2Temp", "Solar 2 Temperature"
            ),
            MiscSensorEntity(
                client, self, "20_1.pv2RelayStatus", "Solar 2 Relay Status"
            ),
            MiscSensorEntity(
                client, self, "20_1.pv2ErrCode", "Solar 2 Error Code", False
            ),
            MiscSensorEntity(
                client, self, "20_1.pv2WarningCode", "Solar 2 Warning Code", False
            ),
            MiscSensorEntity(client, self, "20_1.pv2Status", "Solar 2 Status", False),
            MiscSensorEntity(client, self, "20_1.bpType", "Battery Type", False),
            LevelSensorEntity(client, self, "20_1.batSoc", "Battery Charge"),
            DeciwattsSensorEntity(
                client, self, "20_1.batInputWatts", "Battery Input Watts"
            ),
            DecivoltSensorEntity(
                client, self, "20_1.batInputVolt", "Battery Input Potential"
            ),
            DecivoltSensorEntity(
                client, self, "20_1.batOpVolt", "Battery Op Potential"
            ),
            MilliampSensorEntity(
                client, self, "20_1.batInputCur", "Battery Input Current"
            ),
            DecicelsiusSensorEntity(
                client, self, "20_1.batTemp", "Battery Temperature"
            ),
            RemainSensorEntity(client, self, "20_1.chgRemainTime", "Charge Time"),
            RemainSensorEntity(client, self, "20_1.dsgRemainTime", "Discharge Time"),
            MiscSensorEntity(
                client, self, "20_1.batErrCode", "Battery Error Code", False
            ),
            MiscSensorEntity(
                client, self, "20_1.batWarningCode", "Battery Warning Code", False
            ),
            MiscSensorEntity(client, self, "20_1.batStatus", "Battery Status", False),
            DecivoltSensorEntity(
                client, self, "20_1.llcInputVolt", "LLC Input Potential", False
            ),
            DecivoltSensorEntity(
                client, self, "20_1.llcOpVolt", "LLC Op Potential", False
            ),
            DecicelsiusSensorEntity(client, self, "20_1.llcTemp", "LLC Temperature"),
            MiscSensorEntity(client, self, "20_1.llcErrCode", "LLC Error Code", False),
            MiscSensorEntity(
                client, self, "20_1.llcWarningCode", "LLC Warning Code", False
            ),
            MiscSensorEntity(client, self, "20_1.llcStatus", "LLC Status", False),
            MiscSensorEntity(client, self, "20_1.invOnOff", "Inverter On/Off Status"),
            DeciwattsSensorEntity(
                client, self, "20_1.invOutputWatts", "Inverter Output Watts"
            ),
            DecivoltSensorEntity(
                client, self, "20_1.invInputVolt", "Inverter Output Potential", False
            ),
            DecivoltSensorEntity(
                client, self, "20_1.invOpVolt", "Inverter Op Potential"
            ),
            MilliampSensorEntity(
                client, self, "20_1.invOutputCur", "Inverter Output Current"
            ),
            #  MilliampSensorEntity(client, self, "inv_dc_cur", "Inverter DC Current"),
            DecihertzSensorEntity(client, self, "20_1.invFreq", "Inverter Frequency"),
            DecicelsiusSensorEntity(
                client, self, "20_1.invTemp", "Inverter Temperature"
            ),
            MiscSensorEntity(
                client, self, "20_1.invRelayStatus", "Inverter Relay Status"
            ),
            MiscSensorEntity(
                client, self, "20_1.invErrCode", "Inverter Error Code", False
            ),
            MiscSensorEntity(
                client, self, "20_1.invWarnCode", "Inverter Warning Code", False
            ),
            MiscSensorEntity(client, self, "20_1.invStatus", "Inverter Status", False),
            DeciwattsSensorEntity(client, self, "20_1.permanentWatts", "Other Loads"),
            DeciwattsSensorEntity(
                client, self, "20_1.dynamicWatts", "Smart Plug Loads"
            ),
            DeciwattsSensorEntity(client, self, "20_1.ratedPower", "Rated Power"),
            DeciwattsSensorEntity(client, self, "20_4.h2BaseLoad", "Base Load"),
            DeciwattsSensorEntity(
                client, self, "20_4.h2PowerPlugsPos", "Smart Plug Watts +"
            ),
            DeciwattsSensorEntity(client, self, "20_4.h2GridWatt45", "Grid Watts"),
            DeciwattsSensorEntity(
                client, self, "20_4.h2PowerPlugsNeg", "Smart Plug Watts -"
            ),
            SignalStrengthSensorEntity(client, self, "20_4.h2WifiRssi", "WiFi RSSI"),
            MiscSensorEntity(
                client, self, "20_1.lowerLimit", "Lower Battery Limit", False
            ),
            MiscSensorEntity(
                client, self, "20_1.upperLimit", "Upper Battery Limit", False
            ),
            MiscSensorEntity(
                client, self, "20_1.wirelessErrCode", "Wireless Error Code", False
            ),
            MiscSensorEntity(
                client, self, "20_1.wirelessWarnCode", "Wireless Warning Code", False
            ),
            MiscSensorEntity(
                client, self, "20_1.invBrightness", "LED Brightness", False
            ),
            MiscSensorEntity(
                client, self, "20_1.heartbeatFrequency", "Heartbeat Frequency", False
            ),
            MiscSensorEntity(client, self, "20_1.feedPriority", "Feed-in Priority"),
            ResettingInEnergySolarSensorEntity(
                client,
                self,
                "254_32.watthPv1",
                "PV1 Today Energy Total",
                enabled=True,
            ),
            ResettingInEnergySolarSensorEntity(
                client,
                self,
                "254_32.watthPv2",
                "PV2 Today Energy Total",
                enabled=True,
            ),
            ResettingInEnergySensorEntity(
                client,
                self,
                "254_32.watthFromBattery",
                "From Battery Today Energy Total",
                enabled=True,
            ),
            ResettingOutEnergySensorEntity(
                client,
                self,
                "254_32.watthToBattery",
                "To Battery Today Energy Total",
                enabled=True,
            ),
            ResettingOutEnergySensorEntity(
                client,
                self,
                "254_32.watthToSmartPlugs",
                "To Smart Plugs Today Energy Total",
                enabled=True,
            ),
            ResettingInEnergySensorEntity(
                client,
                self,
                "32_11.watth",
                "Total Energy Report",
                enabled=True,
            ),
            self._status_sensor(client),
        ]

    @override
    def switches(self, client: EcoflowApiClient) -> Sequence[SwitchEntity]:
        return [
            EnabledEntity(
                client,
                self,
                "20_1.feedPriority",
                "Feed-in Priority",
                lambda value: build_command(
                    device_sn=self.device_info.sn,
                    command=Command.WN511_SET_VALUE_PACK,
                    payload=powerstream.SetValue(value=value),
                ),
                enabled=True,
                enableValue=1,
            )
        ]

    @override
    def selects(self, client: EcoflowApiClient) -> Sequence[SelectEntity]:
        return [
            PowerDictSelectEntity(
                client,
                self,
                "20_1.supplyPriority",
                "Power supply mode",
                const.POWER_SUPPLY_PRIORITY_OPTIONS,
                lambda value: build_command(
                    device_sn=self.device_info.sn,
                    command=Command.WN511_SET_SUPPLY_PRIORITY_PACK,
                    payload=socket_sys.include_plug(include_plug=value),
                ),
            ),
        ]

    @override
    def numbers(self, client: EcoflowApiClient) -> Sequence[NumberEntity]:
        return [
            MinBatteryLevelEntity(
                client,
                self,
                "20_1.lowerLimit",
                "Min Discharge Level",
                0,
                100,
                lambda value: build_command(
                    device_sn=self.device_info.sn,
                    command=Command.WN511_SET_BAT_LOWER_PACK,
                    payload=socket_sys.bat_lower_pack(lower_limit=value),
                ),
            ),
            MaxBatteryLevelEntity(
                client,
                self,
                "20_1.upperLimit",
                "Max Charge Level",
                0,
                100,
                lambda value: build_command(
                    device_sn=self.device_info.sn,
                    command=Command.WN511_SET_BAT_UPPER_PACK,
                    payload=socket_sys.bat_upper_pack(upper_limit=value),
                ),
            ),
            BrightnessLevelEntity(
                client,
                self,
                "20_1.invBrightness",
                const.BRIGHTNESS,
                0,
                1023,
                lambda value: build_command(
                    device_sn=self.device_info.sn,
                    command=Command.WN511_SET_BRIGHTNESS_PACK,
                    payload=socket_sys.brightness_pack(brightness=value),
                ),
            ),
            DeciChargingPowerEntity(
                client,
                self,
                "20_1.permanentWatts",
                "Custom load power settings",
                0,
                600,
                lambda value: build_command(
                    device_sn=self.device_info.sn,
                    command=Command.WN511_SET_PERMANENT_WATTS_PACK,
                    payload=socket_sys.permanent_watts_pack(permanent_watts=value),
                ),
            ),
        ]

    @override
    def _prepare_data(self, raw_data: bytes) -> dict[str, Any]:
        res: dict[str, Any] = {"params": {}}
        _LOGGER.debug("Raw data: %s", raw_data.hex())
        from google.protobuf.json_format import MessageToDict

        from .proto import ecopacket_pb2 as ecopacket
        from .proto.support.const import Command, CommandFuncAndId

        try:
            packet = ecopacket.SendHeaderMsg()
            _ = packet.ParseFromString(raw_data)
            for message in packet.msg:
                _LOGGER.debug(
                    'cmd_func %u, cmd_id %u, enc_type %u, seq %u, payload "%s"',
                    message.cmd_func,
                    message.cmd_id,
                    message.enc_type,
                    message.seq,
                    message.pdata.hex(),
                )

                payload_bytes = message.pdata
                if message.enc_type in {1, 6} and message.src != AddressId.APP.value:
                    xor_key = message.seq & 0xFF
                    payload_bytes = bytes(b ^ xor_key for b in payload_bytes)

                if (
                    message.HasField("device_sn")
                    and message.device_sn != self.device_data.sn
                ):
                    _LOGGER.info(
                        "Ignoring EcoPacket for SN %s on topic for SN %s",
                        message.device_sn,
                        self.device_data.sn,
                    )

                command_desc = CommandFuncAndId(
                    func=message.cmd_func, id=message.cmd_id
                )

                try:
                    command = Command(command_desc)
                except ValueError:
                    _LOGGER.info(
                        "Unsupported EcoPacket cmd_func %u, cmd_id %u, pdata %s, message %s",
                        command_desc.func,
                        command_desc.id,
                        message.pdata.hex(),
                        message,
                    )
                    continue

                params = cast(JSONDict, res.setdefault("params", {}))
                if command in {
                    Command.PRIVATE_API_POWERSTREAM_HEARTBEAT,
                    Command.PRIVATE_API_POWERSTREAM_HEARTBEAT2,
                }:
                    payload = get_expected_payload_type(command)()
                    _ = payload.ParseFromString(payload_bytes)
                    heartbeat_dict = cast(
                        JSONDict,
                        MessageToDict(payload, preserving_proto_field_name=False),
                    )
                    heartbeat_dict = {
                        key[:1].lower() + key[1:] if key else key: value
                        for key, value in heartbeat_dict.items()
                    }
                    _LOGGER.debug(
                        "Heartbeat %s payload: %s",
                        command.name,
                        heartbeat_dict,
                    )
                    _LOGGER.info(
                        "Heartbeat %s parsed fields: %s",
                        command.name,
                        heartbeat_dict,
                    )
                    params.update(
                        (f"{command.func}_{command.id}.{key}", value)
                        for key, value in heartbeat_dict.items()
                    )
                    if (
                        self._client is not None
                        and (dt.utcnow() - self._last_energy_req).total_seconds()
                        > 300
                    ):
                        self._client.send_get_message(
                            self.device_info.sn,
                            build_command(
                                device_sn=self.device_info.sn,
                                command=Command.REPORT_ENERGY_TOTAL,
                                payload=b"",
                            ),
                        )
                        self._last_energy_req = dt.utcnow()
                elif command in {Command.PRIVATE_API_PLATFORM_WATTH}:
                    payload = platform.BatchEnergyTotalReport()
                    _ = payload.ParseFromString(payload_bytes)
                    for watth_item in payload.watth_item:
                        try:
                            watth_type_name = to_lower_camel_case(
                                WatthType(watth_item.watth_type).name
                            )
                        except ValueError:
                            continue

                        field_name = (
                            f"watth{watth_type_name[0].upper()}{watth_type_name[1:]}"
                        )
                        params.update(
                            {
                                f"{command.func}_{command.id}.{field_name}": sum(
                                    watth_item.watth
                                ),
                                f"{command.func}_{command.id}.{field_name}Timestamp": watth_item.timestamp,
                            }
                        )

                elif command is Command.WN511_TIME_TASK_CONFIG_POST:
                    payload = socket_sys.time_task_config_post()
                    _ = payload.ParseFromString(payload_bytes)
                    params[f"{command.func}_{command.id}.tasks"] = [
                        {
                            "index": task.task_name,
                            "type": task.type,
                            "start": f"{task.time_range.start_time.hour:02d}:{task.time_range.start_time.min:02d}",
                            "stop": f"{task.time_range.stop_time.hour:02d}:{task.time_range.stop_time.min:02d}",
                        }
                        for task in payload.task_config
                    ]

                elif command is Command.WN511_ACK_138:
                    payload = socket_sys.ret_pack()
                    _ = payload.ParseFromString(payload_bytes)
                    params[f"{command.func}_{command.id}.retSta"] = payload.ret_sta

                elif command is Command.REPORT_ENERGY_TOTAL:
                    if len(payload_bytes) >= 4:
                        watth = int.from_bytes(payload_bytes[:4], "little")
                        params[f"{command.func}_{command.id}.watth"] = watth

                # Add cmd information to allow extraction in private_api_extract_quota_message
                res["cmdFunc"] = command_desc.func
                res["cmdId"] = command_desc.id
                res["timestamp"] = dt.utcnow()
                continue
        except Exception as error:
            _LOGGER.error(error)
            _LOGGER.info(raw_data.hex())
        _LOGGER.debug("Decoded packet result: %s", res)
        return res

    def _status_sensor(self, client: EcoflowApiClient) -> StatusSensorEntity:
        return QuotaStatusSensorEntity(client, self)
