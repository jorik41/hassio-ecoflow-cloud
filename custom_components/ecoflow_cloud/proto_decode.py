from __future__ import annotations

from typing import Any, Dict

from google.protobuf.json_format import MessageToDict

from .devices.internal.proto import (
    ecopacket_pb2,
    powerstream_pb2,
    deltapro3_pb2,
)
from .devices.internal.proto.support.const import (
    Command,
    CommandFunc,
)


def decode_ecopacket(raw_data: bytes) -> Dict[str, Any] | None:
    """Decode EcoFlow protobuf message using powerstream definitions."""
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
        if (
            message.cmd_func == CommandFunc.POWERSTREAM
            and message.cmd_id in heartbeat_ids
        ):
            heartbeat = powerstream_pb2.InverterHeartbeat()
            try:
                heartbeat.ParseFromString(message.pdata)
                result["params"].update(
                    MessageToDict(heartbeat, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = message.pdata.hex()
        elif message.cmd_func == 254 and message.cmd_id == 21:
            display = deltapro3_pb2.DisplayPropertyUpload()
            try:
                display.ParseFromString(message.pdata)
                result["params"].update(
                    MessageToDict(display, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = message.pdata.hex()
        elif message.cmd_func == 254 and message.cmd_id == 22:
            runtime = deltapro3_pb2.RuntimePropertyUpload()
            try:
                runtime.ParseFromString(message.pdata)
                result["params"].update(
                    MessageToDict(runtime, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = message.pdata.hex()
        else:
            result["params"][f"cmd_{message.cmd_func}_{message.cmd_id}"] = message.pdata.hex()
    return result
