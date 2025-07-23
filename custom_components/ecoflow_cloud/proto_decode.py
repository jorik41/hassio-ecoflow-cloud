from __future__ import annotations

from typing import Any, Dict

from google.protobuf.json_format import MessageToDict

from .devices.internal.proto import ecopacket_pb2, powerstream_pb2


def decode_ecopacket(raw_data: bytes) -> Dict[str, Any] | None:
    """Decode EcoFlow protobuf message using powerstream definitions."""
    try:
        packet = ecopacket_pb2.SendHeaderMsg()
        packet.ParseFromString(raw_data)
    except Exception:
        return None

    result: Dict[str, Any] = {"params": {}}
    for message in packet.msg:
        if message.cmd_id == 1:
            heartbeat = powerstream_pb2.InverterHeartbeat()
            try:
                heartbeat.ParseFromString(message.pdata)
                result["params"].update(
                    MessageToDict(heartbeat, preserving_proto_field_name=False)
                )
            except Exception:
                result["params"]["raw_payload"] = message.pdata.hex()
        else:
            result["params"][f"cmd_{message.cmd_func}_{message.cmd_id}"] = message.pdata.hex()
    return result
