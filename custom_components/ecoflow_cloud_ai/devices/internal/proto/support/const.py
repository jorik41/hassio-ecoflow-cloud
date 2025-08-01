import enum
from typing import NamedTuple, cast

from google.protobuf.message import Message as ProtoMessageRaw

from .. import platform_pb2 as platform
from .. import wn511_socket_sys_pb2 as socket_sys


# https://github.com/tomvd/local-powerstream/issues/4#issuecomment-2781354316
class AddressId(enum.Enum):
    IOT = 1
    APP = 32
    MQTT = 53


class DirectionId(enum.Enum):
    DEFAULT = 1


class CommandFunc(enum.IntEnum):
    DEFAULT = 0
    SMART_PLUG = 2
    POWERSTREAM = 20
    REPORTS = 32
    PLATFORM = platform.PlCmdSets.PL_EXT_CMD_SETS


class CommandFuncAndId(NamedTuple):
    func: int
    id: int


class Command(enum.Enum):
    @enum.property
    def func(self) -> CommandFunc | int:
        return self.value.func

    @enum.property
    def id(self) -> int:
        return self.value.id

    PRIVATE_API_POWERSTREAM_HEARTBEAT = CommandFuncAndId(
        func=CommandFunc.POWERSTREAM, id=1
    )

    PRIVATE_API_POWERSTREAM_HEARTBEAT2 = CommandFuncAndId(
        func=CommandFunc.POWERSTREAM, id=4
    )

    WN511_SET_PERMANENT_WATTS_PACK = CommandFuncAndId(
        func=CommandFunc.POWERSTREAM, id=129
    )
    WN511_SET_SUPPLY_PRIORITY_PACK = CommandFuncAndId(
        func=CommandFunc.POWERSTREAM, id=130
    )
    WN511_SET_BAT_LOWER_PACK = CommandFuncAndId(func=CommandFunc.POWERSTREAM, id=132)
    WN511_SET_BAT_UPPER_PACK = CommandFuncAndId(func=CommandFunc.POWERSTREAM, id=133)
    WN511_SET_BRIGHTNESS_PACK = CommandFuncAndId(func=CommandFunc.POWERSTREAM, id=135)
    WN511_SET_VALUE_PACK = CommandFuncAndId(func=CommandFunc.POWERSTREAM, id=136)

    WN511_TIME_TASK_CONFIG_POST = CommandFuncAndId(
        func=CommandFunc.POWERSTREAM,
        id=134,
    )

    WN511_ACK_138 = CommandFuncAndId(func=CommandFunc.POWERSTREAM, id=138)

    REPORT_ENERGY_TOTAL = CommandFuncAndId(func=CommandFunc.REPORTS, id=11)

    PRIVATE_API_POWERSTREAM_SET_FEED_PROTECT = CommandFuncAndId(
        func=CommandFunc.POWERSTREAM, id=143
    )

    PRIVATE_API_PLATFORM_WATTH = CommandFuncAndId(
        func=CommandFunc.PLATFORM, id=platform.PlCmdId.PL_CMD_ID_WATTH
    )


# https://github.com/peuter/ecoflow/blob/04bb01fb3d6dcd845b0a896342b0d895f532cf85/model/ecoflow/constant.py#L9
class WatthType(enum.IntEnum):
    TO_SMART_PLUGS = 2  # ?
    TO_BATTERY = 3  # ?
    FROM_BATTERY = 4  # ?
    PV1 = 7  # ?
    PV2 = 8  # ?


_expected_payload_types = dict[Command, type[ProtoMessageRaw]]()


def get_expected_payload_type(cmd: Command) -> type[ProtoMessageRaw]:
    from .. import powerstream_pb2 as powerstream

    global _expected_payload_types
    if not _expected_payload_types:
        _expected_payload_types.update(
            cast(
                dict[Command, type[ProtoMessageRaw]],
                {
                    Command.PRIVATE_API_POWERSTREAM_HEARTBEAT: powerstream.InverterHeartbeat,
                    Command.PRIVATE_API_POWERSTREAM_HEARTBEAT2: powerstream.InverterHeartbeat2,
                    Command.WN511_SET_PERMANENT_WATTS_PACK: socket_sys.permanent_watts_pack,
                    Command.WN511_SET_SUPPLY_PRIORITY_PACK: socket_sys.include_plug,
                    Command.WN511_SET_BAT_LOWER_PACK: socket_sys.bat_lower_pack,
                    Command.WN511_SET_BAT_UPPER_PACK: socket_sys.bat_upper_pack,
                    Command.WN511_SET_BRIGHTNESS_PACK: socket_sys.brightness_pack,
                    Command.WN511_SET_VALUE_PACK: powerstream.SetValue,
                    Command.PRIVATE_API_POWERSTREAM_SET_FEED_PROTECT: powerstream.SetValue,
                    Command.PRIVATE_API_PLATFORM_WATTH: platform.BatchEnergyTotalReport,
                    Command.WN511_TIME_TASK_CONFIG_POST: socket_sys.time_task_config_post,
                    Command.WN511_ACK_138: socket_sys.ret_pack,
                },
            )
        )

    return _expected_payload_types[cmd]
