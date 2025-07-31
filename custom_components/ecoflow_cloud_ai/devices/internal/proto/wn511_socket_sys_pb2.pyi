from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class PowerAckPack(_message.Message):
    __slots__ = ["sys_seq"]
    SYS_SEQ_FIELD_NUMBER: _ClassVar[int]
    sys_seq: int
    def __init__(self, sys_seq: _Optional[int] = ...) -> None: ...

class PowerItem(_message.Message):
    __slots__ = ["plug_power", "timestamp", "timezone"]
    PLUG_POWER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    plug_power: int
    timestamp: int
    timezone: str
    def __init__(
        self,
        timestamp: _Optional[int] = ...,
        timezone: _Optional[str] = ...,
        plug_power: _Optional[int] = ...,
    ) -> None: ...

class PowerPack(_message.Message):
    __slots__ = ["sys_power_stream", "sys_seq"]
    SYS_POWER_STREAM_FIELD_NUMBER: _ClassVar[int]
    SYS_SEQ_FIELD_NUMBER: _ClassVar[int]
    sys_power_stream: _containers.RepeatedCompositeFieldContainer[PowerItem]
    sys_seq: int
    def __init__(
        self,
        sys_seq: _Optional[int] = ...,
        sys_power_stream: _Optional[_Iterable[_Union[PowerItem, _Mapping]]] = ...,
    ) -> None: ...

class bat_lower_pack(_message.Message):
    __slots__ = ["lower_limit"]
    LOWER_LIMIT_FIELD_NUMBER: _ClassVar[int]
    lower_limit: int
    def __init__(self, lower_limit: _Optional[int] = ...) -> None: ...

class bat_upper_pack(_message.Message):
    __slots__ = ["upper_limit"]
    UPPER_LIMIT_FIELD_NUMBER: _ClassVar[int]
    upper_limit: int
    def __init__(self, upper_limit: _Optional[int] = ...) -> None: ...

class brightness_pack(_message.Message):
    __slots__ = ["brightness"]
    BRIGHTNESS_FIELD_NUMBER: _ClassVar[int]
    brightness: int
    def __init__(self, brightness: _Optional[int] = ...) -> None: ...

class include_plug(_message.Message):
    __slots__ = ["include_plug"]
    INCLUDE_PLUG_FIELD_NUMBER: _ClassVar[int]
    include_plug: bool
    def __init__(self, include_plug: bool = ...) -> None: ...

class max_cur_pack(_message.Message):
    __slots__ = ["max_cur"]
    MAX_CUR_FIELD_NUMBER: _ClassVar[int]
    max_cur: int
    def __init__(self, max_cur: _Optional[int] = ...) -> None: ...

class max_watts_pack(_message.Message):
    __slots__ = ["max_watts"]
    MAX_WATTS_FIELD_NUMBER: _ClassVar[int]
    max_watts: int
    def __init__(self, max_watts: _Optional[int] = ...) -> None: ...

class mesh_ctrl_pack(_message.Message):
    __slots__ = ["mesh_enable"]
    MESH_ENABLE_FIELD_NUMBER: _ClassVar[int]
    mesh_enable: int
    def __init__(self, mesh_enable: _Optional[int] = ...) -> None: ...

class permanent_watts_pack(_message.Message):
    __slots__ = ["permanent_watts"]
    PERMANENT_WATTS_FIELD_NUMBER: _ClassVar[int]
    permanent_watts: int
    def __init__(self, permanent_watts: _Optional[int] = ...) -> None: ...

class plug_ack_message(_message.Message):
    __slots__ = ["ack"]
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: int
    def __init__(self, ack: _Optional[int] = ...) -> None: ...

class plug_heartbeat_pack(_message.Message):
    __slots__ = [
        "brightness",
        "country",
        "current",
        "err_code",
        "freq",
        "heartbeat_frequency",
        "max_cur",
        "max_watts",
        "mesh_enable",
        "switch",
        "temp",
        "town",
        "volt",
        "warn_code",
        "watts",
    ]
    BRIGHTNESS_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    FREQ_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    MAX_CUR_FIELD_NUMBER: _ClassVar[int]
    MAX_WATTS_FIELD_NUMBER: _ClassVar[int]
    MESH_ENABLE_FIELD_NUMBER: _ClassVar[int]
    SWITCH_FIELD_NUMBER: _ClassVar[int]
    TEMP_FIELD_NUMBER: _ClassVar[int]
    TOWN_FIELD_NUMBER: _ClassVar[int]
    VOLT_FIELD_NUMBER: _ClassVar[int]
    WARN_CODE_FIELD_NUMBER: _ClassVar[int]
    WATTS_FIELD_NUMBER: _ClassVar[int]
    brightness: int
    country: int
    current: int
    err_code: int
    freq: int
    heartbeat_frequency: int
    max_cur: int
    max_watts: int
    mesh_enable: bool
    switch: bool
    temp: int
    town: int
    volt: int
    warn_code: int
    watts: int
    def __init__(
        self,
        err_code: _Optional[int] = ...,
        warn_code: _Optional[int] = ...,
        country: _Optional[int] = ...,
        town: _Optional[int] = ...,
        max_cur: _Optional[int] = ...,
        temp: _Optional[int] = ...,
        freq: _Optional[int] = ...,
        current: _Optional[int] = ...,
        volt: _Optional[int] = ...,
        watts: _Optional[int] = ...,
        switch: bool = ...,
        brightness: _Optional[int] = ...,
        max_watts: _Optional[int] = ...,
        heartbeat_frequency: _Optional[int] = ...,
        mesh_enable: bool = ...,
    ) -> None: ...

class plug_switch_message(_message.Message):
    __slots__ = ["plug_switch"]
    PLUG_SWITCH_FIELD_NUMBER: _ClassVar[int]
    plug_switch: int
    def __init__(self, plug_switch: _Optional[int] = ...) -> None: ...

class ret_pack(_message.Message):
    __slots__ = ["ret_sta"]
    RET_STA_FIELD_NUMBER: _ClassVar[int]
    ret_sta: bool
    def __init__(self, ret_sta: bool = ...) -> None: ...

class rtc_data(_message.Message):
    __slots__ = ["day", "hour", "min", "month", "sec", "week", "year"]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    day: int
    hour: int
    min: int
    month: int
    sec: int
    week: int
    year: int
    def __init__(
        self,
        week: _Optional[int] = ...,
        sec: _Optional[int] = ...,
        min: _Optional[int] = ...,
        hour: _Optional[int] = ...,
        day: _Optional[int] = ...,
        month: _Optional[int] = ...,
        year: _Optional[int] = ...,
    ) -> None: ...

class time_range_strategy(_message.Message):
    __slots__ = [
        "is_config",
        "is_enable",
        "start_time",
        "stop_time",
        "time_data",
        "time_mode",
    ]
    IS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    IS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STOP_TIME_FIELD_NUMBER: _ClassVar[int]
    TIME_DATA_FIELD_NUMBER: _ClassVar[int]
    TIME_MODE_FIELD_NUMBER: _ClassVar[int]
    is_config: bool
    is_enable: bool
    start_time: rtc_data
    stop_time: rtc_data
    time_data: int
    time_mode: int
    def __init__(
        self,
        is_config: bool = ...,
        is_enable: bool = ...,
        time_mode: _Optional[int] = ...,
        time_data: _Optional[int] = ...,
        start_time: _Optional[_Union[rtc_data, _Mapping]] = ...,
        stop_time: _Optional[_Union[rtc_data, _Mapping]] = ...,
    ) -> None: ...

class time_task_config(_message.Message):
    __slots__ = ["task_name", "time_range", "type"]
    TASK_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    task_name: str
    time_range: time_range_strategy
    type: int
    def __init__(
        self,
        task_name: _Optional[str] = ...,
        time_range: _Optional[_Union[time_range_strategy, _Mapping]] = ...,
        type: _Optional[int] = ...,
    ) -> None: ...

class time_task_config_post(_message.Message):
    __slots__ = ["task_config"]
    TASK_CONFIG_FIELD_NUMBER: _ClassVar[int]
    task_config: _containers.RepeatedCompositeFieldContainer[time_task_config]
    def __init__(
        self,
        task_config: _Optional[_Iterable[_Union[time_task_config, _Mapping]]] = ...,
    ) -> None: ...
