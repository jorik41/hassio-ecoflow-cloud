from __future__ import annotations

import logging
from typing import Any, Dict

from .devices.internal.proto import (
    ecopacket_pb2,
    powerstream_pb2,
    deltapro3_pb2,
    wn511_socket_sys_pb2,
)
from .devices.internal.proto.support.const import (
    Command,
    CommandFunc,
)

from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)


def _log_proto(msg_name: str, data: Dict[str, Any]) -> None:
    if any(key.startswith("unknown") for key in data):
        _LOGGER.info("Protobuf %s contains unknown fields: %s", msg_name, data)
    else:
        _LOGGER.debug("Protobuf %s: %s", msg_name, data)


def decode_ecopacket(raw_data: bytes) -> Dict[str, Any] | None:
    """Decode EcoFlow protobuf message using powerstream definitions.

    XOR encrypted payloads with ``enc_type`` 1 or 6 are automatically
    decrypted using the packet sequence number as key.
    """
    try:
        packet = ecopacket_pb2.SendHeaderMsg()
        packet.ParseFromString(raw_data)
    except Exception:
        return None

    result: Dict[str, Any] = {"params": {}}
    heartbeat_ids = {
        Command.PRIVATE_API_POWERSTREAM_HEARTBEAT.id,
        50,  # tentative Delta Pro 3 heartbeat; see issue #270
    }

    for message in packet.msg:
        payload = message.pdata
        # enc_type 1 and 6 indicate payload is XOR encrypted with the
        # lower byte of the sequence number
        if message.enc_type in {1, 6} and message.src != 32:
            xor_key = message.seq & 0xFF
            payload = bytes(b ^ xor_key for b in payload)
        if (
            message.cmd_func == CommandFunc.POWERSTREAM
            and message.cmd_id in heartbeat_ids
        ):
            heartbeat = powerstream_pb2.InverterHeartbeat()
            try:
                heartbeat.ParseFromString(message.pdata)
                data = MessageToDict(heartbeat, preserving_proto_field_name=True)
                _log_proto("InverterHeartbeat", data)
                result["params"].update(
                    MessageToDict(heartbeat, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = message.pdata.hex()
        elif message.cmd_func == CommandFunc.POWERSTREAM and message.cmd_id == 4:
            heartbeat2 = powerstream_pb2.InverterHeartbeat2()
            try:
                heartbeat2.ParseFromString(payload)
                data = MessageToDict(heartbeat2, preserving_proto_field_name=True)
                _log_proto("InverterHeartbeat2", data)
                result["params"].update(
                    MessageToDict(heartbeat2, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        elif message.cmd_func == CommandFunc.POWERSTREAM and message.cmd_id == 134:
            tasks = wn511_socket_sys_pb2.time_task_config_post()
            try:
                tasks.ParseFromString(payload)
                data = MessageToDict(tasks, preserving_proto_field_name=True)
                _log_proto("time_task_config_post", data)
                result["params"].update(
                    MessageToDict(tasks, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        elif (
            message.cmd_func == CommandFunc.POWERSTREAM
            and message.cmd_id == Command.WN511_SET_VALUE_PACK.id
        ):
            set_value = powerstream_pb2.SetValue()
            try:
                set_value.ParseFromString(payload)
                data = MessageToDict(set_value, preserving_proto_field_name=True)
                _log_proto("SetValue136", data)
                result["params"].update(
                    MessageToDict(set_value, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        elif message.cmd_func == 254 and message.cmd_id == 21:
            display = deltapro3_pb2.DisplayPropertyUpload()
            try:
                display.ParseFromString(payload)
                data = MessageToDict(display, preserving_proto_field_name=True)
                _log_proto("DisplayPropertyUpload", data)
                result["params"].update(
                    MessageToDict(display, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        elif message.cmd_func == 254 and message.cmd_id == 22:
            runtime = deltapro3_pb2.RuntimePropertyUpload()
            try:
                runtime.ParseFromString(payload)
                data = MessageToDict(runtime, preserving_proto_field_name=True)
                _log_proto("RuntimePropertyUpload", data)
                result["params"].update(
                    MessageToDict(runtime, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        elif message.cmd_func == 254 and message.cmd_id == 23:
            report = deltapro3_pb2.cmdFunc254_cmdId23_Report()
            try:
                report.ParseFromString(payload)
                data = MessageToDict(report, preserving_proto_field_name=True)
                _log_proto("cmdFunc254_cmdId23_Report", data)
                result["params"].update(
                    MessageToDict(report, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        elif message.cmd_func == 32 and message.cmd_id == 2:
            report = deltapro3_pb2.cmdFunc32_cmdId2_Report()
            try:
                report.ParseFromString(payload)
                data = MessageToDict(report, preserving_proto_field_name=True)
                _log_proto("cmdFunc32_cmdId2_Report", data)
                result["params"].update(
                    MessageToDict(report, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        elif message.cmd_func == 50 and message.cmd_id == 30:
            report = deltapro3_pb2.cmdFunc50_cmdId30_Report()
            try:
                report.ParseFromString(payload)
                data = MessageToDict(report, preserving_proto_field_name=True)
                _log_proto("cmdFunc50_cmdId30_Report", data)
                result["params"].update(
                    MessageToDict(report, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = payload.hex()
        else:
            key = f"cmd_{message.cmd_func}_{message.cmd_id}"
            result["params"][key] = payload.hex()
    return result
