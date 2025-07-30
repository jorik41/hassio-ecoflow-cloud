from model.protos import options_pb2 as _options_pb2
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

class Header(_message.Message):
    __slots__ = [
        "ack_type",
        "check_type",
        "cmd_func",
        "cmd_id",
        "code",
        "d_dest",
        "d_src",
        "data_len",
        "dest",
        "device_sn",
        "enc_type",
        "is_ack",
        "is_queue",
        "is_rw_cmd",
        "module_sn",
        "need_ack",
        "payload_ver",
        "pdata",
        "product_id",
        "seq",
        "src",
        "time_snap",
        "version",
    ]
    ACK_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHECK_TYPE_FIELD_NUMBER: _ClassVar[int]
    CMD_FUNC_FIELD_NUMBER: _ClassVar[int]
    CMD_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_LEN_FIELD_NUMBER: _ClassVar[int]
    DEST_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SN_FIELD_NUMBER: _ClassVar[int]
    D_DEST_FIELD_NUMBER: _ClassVar[int]
    D_SRC_FIELD_NUMBER: _ClassVar[int]
    ENC_TYPE_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    IS_ACK_FIELD_NUMBER: _ClassVar[int]
    IS_QUEUE_FIELD_NUMBER: _ClassVar[int]
    IS_RW_CMD_FIELD_NUMBER: _ClassVar[int]
    MODULE_SN_FIELD_NUMBER: _ClassVar[int]
    NEED_ACK_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_VER_FIELD_NUMBER: _ClassVar[int]
    PDATA_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    SRC_FIELD_NUMBER: _ClassVar[int]
    TIME_SNAP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ack_type: int
    check_type: int
    cmd_func: int
    cmd_id: int
    code: str
    d_dest: int
    d_src: int
    data_len: int
    dest: int
    device_sn: str
    enc_type: int
    is_ack: int
    is_queue: int
    is_rw_cmd: int
    module_sn: str
    need_ack: int
    payload_ver: int
    pdata: bytes
    product_id: int
    seq: int
    src: int
    time_snap: int
    version: int
    def __init__(
        self,
        pdata: _Optional[bytes] = ...,
        src: _Optional[int] = ...,
        dest: _Optional[int] = ...,
        d_src: _Optional[int] = ...,
        d_dest: _Optional[int] = ...,
        enc_type: _Optional[int] = ...,
        check_type: _Optional[int] = ...,
        cmd_func: _Optional[int] = ...,
        cmd_id: _Optional[int] = ...,
        data_len: _Optional[int] = ...,
        need_ack: _Optional[int] = ...,
        is_ack: _Optional[int] = ...,
        seq: _Optional[int] = ...,
        product_id: _Optional[int] = ...,
        version: _Optional[int] = ...,
        payload_ver: _Optional[int] = ...,
        time_snap: _Optional[int] = ...,
        is_rw_cmd: _Optional[int] = ...,
        is_queue: _Optional[int] = ...,
        ack_type: _Optional[int] = ...,
        code: _Optional[str] = ...,
        module_sn: _Optional[str] = ...,
        device_sn: _Optional[str] = ...,
        **kwargs
    ) -> None: ...

class InverterHeartbeat(_message.Message):
    __slots__ = [
        "batChargingTime",
        "batDischargingTime",
        "batErrCode",
        "batInputCur",
        "batInputVolt",
        "batInputWatts",
        "batOpVolt",
        "batSoc",
        "batStatus",
        "batTemp",
        "batWarningCode",
        "bpType",
        "dynamicWatts",
        "feedPriority",
        "heartbeatFrequency",
        "installCountry",
        "installTown",
        "invBrightness",
        "invDcCur",
        "invErrCode",
        "invFreq",
        "invInputVolt",
        "invOnOff",
        "invOpVolt",
        "invOutputCur",
        "invOutputWatts",
        "invRelayStatus",
        "invStatus",
        "invTemp",
        "invWarnCode",
        "llcErrCode",
        "llcInputVolt",
        "llcOpVolt",
        "llcStatus",
        "llcTemp",
        "llcWarningCode",
        "lowerLimit",
        "permanentWatts",
        "pv1ErrCode",
        "pv1InputCur",
        "pv1InputVolt",
        "pv1InputWatts",
        "pv1OpVolt",
        "pv1RelayStatus",
        "pv1Status",
        "pv1Temp",
        "pv1WarnCode",
        "pv2ErrCode",
        "pv2InputCur",
        "pv2InputVolt",
        "pv2InputWatts",
        "pv2OpVolt",
        "pv2RelayStatus",
        "pv2Status",
        "pv2Temp",
        "pv2WarningCode",
        "ratedPower",
        "supplyPriority",
        "upperLimit",
        "wirelessErrCode",
        "wirelessWarnCode",
    ]
    BATCHARGINGTIME_FIELD_NUMBER: _ClassVar[int]
    BATDISCHARGINGTIME_FIELD_NUMBER: _ClassVar[int]
    BATERRCODE_FIELD_NUMBER: _ClassVar[int]
    BATINPUTCUR_FIELD_NUMBER: _ClassVar[int]
    BATINPUTVOLT_FIELD_NUMBER: _ClassVar[int]
    BATINPUTWATTS_FIELD_NUMBER: _ClassVar[int]
    BATOPVOLT_FIELD_NUMBER: _ClassVar[int]
    BATSOC_FIELD_NUMBER: _ClassVar[int]
    BATSTATUS_FIELD_NUMBER: _ClassVar[int]
    BATTEMP_FIELD_NUMBER: _ClassVar[int]
    BATWARNINGCODE_FIELD_NUMBER: _ClassVar[int]
    BPTYPE_FIELD_NUMBER: _ClassVar[int]
    DYNAMICWATTS_FIELD_NUMBER: _ClassVar[int]
    FEEDPRIORITY_FIELD_NUMBER: _ClassVar[int]
    HEARTBEATFREQUENCY_FIELD_NUMBER: _ClassVar[int]
    INSTALLCOUNTRY_FIELD_NUMBER: _ClassVar[int]
    INSTALLTOWN_FIELD_NUMBER: _ClassVar[int]
    INVBRIGHTNESS_FIELD_NUMBER: _ClassVar[int]
    INVDCCUR_FIELD_NUMBER: _ClassVar[int]
    INVERRCODE_FIELD_NUMBER: _ClassVar[int]
    INVFREQ_FIELD_NUMBER: _ClassVar[int]
    INVINPUTVOLT_FIELD_NUMBER: _ClassVar[int]
    INVONOFF_FIELD_NUMBER: _ClassVar[int]
    INVOPVOLT_FIELD_NUMBER: _ClassVar[int]
    INVOUTPUTCUR_FIELD_NUMBER: _ClassVar[int]
    INVOUTPUTWATTS_FIELD_NUMBER: _ClassVar[int]
    INVRELAYSTATUS_FIELD_NUMBER: _ClassVar[int]
    INVSTATUS_FIELD_NUMBER: _ClassVar[int]
    INVTEMP_FIELD_NUMBER: _ClassVar[int]
    INVWARNCODE_FIELD_NUMBER: _ClassVar[int]
    LLCERRCODE_FIELD_NUMBER: _ClassVar[int]
    LLCINPUTVOLT_FIELD_NUMBER: _ClassVar[int]
    LLCOPVOLT_FIELD_NUMBER: _ClassVar[int]
    LLCSTATUS_FIELD_NUMBER: _ClassVar[int]
    LLCTEMP_FIELD_NUMBER: _ClassVar[int]
    LLCWARNINGCODE_FIELD_NUMBER: _ClassVar[int]
    LOWERLIMIT_FIELD_NUMBER: _ClassVar[int]
    PERMANENTWATTS_FIELD_NUMBER: _ClassVar[int]
    PV1ERRCODE_FIELD_NUMBER: _ClassVar[int]
    PV1INPUTCUR_FIELD_NUMBER: _ClassVar[int]
    PV1INPUTVOLT_FIELD_NUMBER: _ClassVar[int]
    PV1INPUTWATTS_FIELD_NUMBER: _ClassVar[int]
    PV1OPVOLT_FIELD_NUMBER: _ClassVar[int]
    PV1RELAYSTATUS_FIELD_NUMBER: _ClassVar[int]
    PV1STATUS_FIELD_NUMBER: _ClassVar[int]
    PV1TEMP_FIELD_NUMBER: _ClassVar[int]
    PV1WARNCODE_FIELD_NUMBER: _ClassVar[int]
    PV2ERRCODE_FIELD_NUMBER: _ClassVar[int]
    PV2INPUTCUR_FIELD_NUMBER: _ClassVar[int]
    PV2INPUTVOLT_FIELD_NUMBER: _ClassVar[int]
    PV2INPUTWATTS_FIELD_NUMBER: _ClassVar[int]
    PV2OPVOLT_FIELD_NUMBER: _ClassVar[int]
    PV2RELAYSTATUS_FIELD_NUMBER: _ClassVar[int]
    PV2STATUS_FIELD_NUMBER: _ClassVar[int]
    PV2TEMP_FIELD_NUMBER: _ClassVar[int]
    PV2WARNINGCODE_FIELD_NUMBER: _ClassVar[int]
    RATEDPOWER_FIELD_NUMBER: _ClassVar[int]
    SUPPLYPRIORITY_FIELD_NUMBER: _ClassVar[int]
    UPPERLIMIT_FIELD_NUMBER: _ClassVar[int]
    WIRELESSERRCODE_FIELD_NUMBER: _ClassVar[int]
    WIRELESSWARNCODE_FIELD_NUMBER: _ClassVar[int]
    batChargingTime: int
    batDischargingTime: int
    batErrCode: int
    batInputCur: int
    batInputVolt: int
    batInputWatts: int
    batOpVolt: int
    batSoc: int
    batStatus: int
    batTemp: int
    batWarningCode: int
    bpType: int
    dynamicWatts: int
    feedPriority: int
    heartbeatFrequency: int
    installCountry: int
    installTown: int
    invBrightness: int
    invDcCur: int
    invErrCode: int
    invFreq: int
    invInputVolt: int
    invOnOff: int
    invOpVolt: int
    invOutputCur: int
    invOutputWatts: int
    invRelayStatus: int
    invStatus: int
    invTemp: int
    invWarnCode: int
    llcErrCode: int
    llcInputVolt: int
    llcOpVolt: int
    llcStatus: int
    llcTemp: int
    llcWarningCode: int
    lowerLimit: int
    permanentWatts: int
    pv1ErrCode: int
    pv1InputCur: int
    pv1InputVolt: int
    pv1InputWatts: int
    pv1OpVolt: int
    pv1RelayStatus: int
    pv1Status: int
    pv1Temp: int
    pv1WarnCode: int
    pv2ErrCode: int
    pv2InputCur: int
    pv2InputVolt: int
    pv2InputWatts: int
    pv2OpVolt: int
    pv2RelayStatus: int
    pv2Status: int
    pv2Temp: int
    pv2WarningCode: int
    ratedPower: int
    supplyPriority: int
    upperLimit: int
    wirelessErrCode: int
    wirelessWarnCode: int
    def __init__(
        self,
        invErrCode: _Optional[int] = ...,
        invWarnCode: _Optional[int] = ...,
        pv1ErrCode: _Optional[int] = ...,
        pv1WarnCode: _Optional[int] = ...,
        pv2ErrCode: _Optional[int] = ...,
        pv2WarningCode: _Optional[int] = ...,
        batErrCode: _Optional[int] = ...,
        batWarningCode: _Optional[int] = ...,
        llcErrCode: _Optional[int] = ...,
        llcWarningCode: _Optional[int] = ...,
        pv1Status: _Optional[int] = ...,
        pv2Status: _Optional[int] = ...,
        batStatus: _Optional[int] = ...,
        llcStatus: _Optional[int] = ...,
        invStatus: _Optional[int] = ...,
        pv1InputVolt: _Optional[int] = ...,
        pv1OpVolt: _Optional[int] = ...,
        pv1InputCur: _Optional[int] = ...,
        pv1InputWatts: _Optional[int] = ...,
        pv1Temp: _Optional[int] = ...,
        pv2InputVolt: _Optional[int] = ...,
        pv2OpVolt: _Optional[int] = ...,
        pv2InputCur: _Optional[int] = ...,
        pv2InputWatts: _Optional[int] = ...,
        pv2Temp: _Optional[int] = ...,
        batInputVolt: _Optional[int] = ...,
        batOpVolt: _Optional[int] = ...,
        batInputCur: _Optional[int] = ...,
        batInputWatts: _Optional[int] = ...,
        batTemp: _Optional[int] = ...,
        batSoc: _Optional[int] = ...,
        llcInputVolt: _Optional[int] = ...,
        llcOpVolt: _Optional[int] = ...,
        llcTemp: _Optional[int] = ...,
        invInputVolt: _Optional[int] = ...,
        invOpVolt: _Optional[int] = ...,
        invOutputCur: _Optional[int] = ...,
        invOutputWatts: _Optional[int] = ...,
        invTemp: _Optional[int] = ...,
        invFreq: _Optional[int] = ...,
        invDcCur: _Optional[int] = ...,
        bpType: _Optional[int] = ...,
        invRelayStatus: _Optional[int] = ...,
        pv1RelayStatus: _Optional[int] = ...,
        pv2RelayStatus: _Optional[int] = ...,
        installCountry: _Optional[int] = ...,
        installTown: _Optional[int] = ...,
        permanentWatts: _Optional[int] = ...,
        dynamicWatts: _Optional[int] = ...,
        supplyPriority: _Optional[int] = ...,
        lowerLimit: _Optional[int] = ...,
        upperLimit: _Optional[int] = ...,
        invOnOff: _Optional[int] = ...,
        wirelessErrCode: _Optional[int] = ...,
        wirelessWarnCode: _Optional[int] = ...,
        invBrightness: _Optional[int] = ...,
        heartbeatFrequency: _Optional[int] = ...,
        ratedPower: _Optional[int] = ...,
        batChargingTime: _Optional[int] = ...,
        batDischargingTime: _Optional[int] = ...,
        feedPriority: _Optional[int] = ...,
    ) -> None: ...

class InverterHeartbeat2(_message.Message):
    __slots__ = [
        "H2_X_Unknown_05",
        "H2_X_Unknown_13",
        "H2_X_Unknown_14",
        "H2_X_Unknown_15",
        "H2_X_Unknown_16",
        "H2_X_Unknown_17",
        "H2_X_Unknown_18",
        "H2_X_Unknown_19",
        "H2_X_Unknown_20",
        "H2_X_Unknown_21",
        "H2_X_Unknown_22",
        "H2_X_Unknown_23",
        "H2_X_Unknown_24",
        "H2_X_Unknown_25",
        "H2_X_Unknown_26",
        "H2_X_Unknown_27",
        "H2_X_Unknown_28",
        "H2_X_Unknown_29",
        "H2_X_Unknown_30",
        "H2_X_Unknown_31",
        "H2_X_Unknown_33",
        "H2_X_Unknown_34",
        "H2_X_Unknown_35",
        "H2_X_Unknown_36",
        "H2_X_Unknown_37",
        "H2_X_Unknown_38",
        "H2_X_Unknown_39",
        "H2_X_Unknown_40",
        "H2_X_Unknown_41",
        "H2_X_Unknown_42",
        "H2_X_Unknown_43",
        "H2_X_Unknown_44",
        "H2_X_Unknown_47",
        "H2_X_Unknown_49",
        "H2_X_Unknown_51",
        "H2_baseLoad",
        "H2_gridWatt_45",
        "H2_lowerLimit",
        "H2_powerPlugsNeg",
        "H2_powerPlugsPos",
        "H2_pv1Active",
        "H2_pv1Status",
        "H2_pv2Active",
        "H2_pv2Status",
        "H2_status_06",
        "H2_status_09",
        "H2_status_10",
        "H2_unixtime_48",
        "H2_unixtime_50",
        "H2_upperLimit",
        "H2_uptime",
        "H2_wifiRssi",
    ]
    H2_BASELOAD_FIELD_NUMBER: _ClassVar[int]
    H2_GRIDWATT_45_FIELD_NUMBER: _ClassVar[int]
    H2_LOWERLIMIT_FIELD_NUMBER: _ClassVar[int]
    H2_POWERPLUGSNEG_FIELD_NUMBER: _ClassVar[int]
    H2_POWERPLUGSPOS_FIELD_NUMBER: _ClassVar[int]
    H2_PV1ACTIVE_FIELD_NUMBER: _ClassVar[int]
    H2_PV1STATUS_FIELD_NUMBER: _ClassVar[int]
    H2_PV2ACTIVE_FIELD_NUMBER: _ClassVar[int]
    H2_PV2STATUS_FIELD_NUMBER: _ClassVar[int]
    H2_STATUS_06_FIELD_NUMBER: _ClassVar[int]
    H2_STATUS_09_FIELD_NUMBER: _ClassVar[int]
    H2_STATUS_10_FIELD_NUMBER: _ClassVar[int]
    H2_UNIXTIME_48_FIELD_NUMBER: _ClassVar[int]
    H2_UNIXTIME_50_FIELD_NUMBER: _ClassVar[int]
    H2_UPPERLIMIT_FIELD_NUMBER: _ClassVar[int]
    H2_UPTIME_FIELD_NUMBER: _ClassVar[int]
    H2_WIFIRSSI_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_05_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_13_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_14_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_15_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_16_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_17_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_18_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_19_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_20_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_21_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_22_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_23_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_24_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_25_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_26_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_27_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_28_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_29_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_30_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_31_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_33_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_34_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_35_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_36_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_37_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_38_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_39_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_40_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_41_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_42_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_43_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_44_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_47_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_49_FIELD_NUMBER: _ClassVar[int]
    H2_X_UNKNOWN_51_FIELD_NUMBER: _ClassVar[int]
    H2_X_Unknown_05: int
    H2_X_Unknown_13: int
    H2_X_Unknown_14: int
    H2_X_Unknown_15: int
    H2_X_Unknown_16: int
    H2_X_Unknown_17: int
    H2_X_Unknown_18: int
    H2_X_Unknown_19: int
    H2_X_Unknown_20: int
    H2_X_Unknown_21: int
    H2_X_Unknown_22: int
    H2_X_Unknown_23: int
    H2_X_Unknown_24: int
    H2_X_Unknown_25: int
    H2_X_Unknown_26: int
    H2_X_Unknown_27: int
    H2_X_Unknown_28: int
    H2_X_Unknown_29: int
    H2_X_Unknown_30: int
    H2_X_Unknown_31: int
    H2_X_Unknown_33: int
    H2_X_Unknown_34: int
    H2_X_Unknown_35: int
    H2_X_Unknown_36: int
    H2_X_Unknown_37: int
    H2_X_Unknown_38: int
    H2_X_Unknown_39: int
    H2_X_Unknown_40: int
    H2_X_Unknown_41: int
    H2_X_Unknown_42: int
    H2_X_Unknown_43: int
    H2_X_Unknown_44: int
    H2_X_Unknown_47: int
    H2_X_Unknown_49: int
    H2_X_Unknown_51: int
    H2_baseLoad: int
    H2_gridWatt_45: int
    H2_lowerLimit: int
    H2_powerPlugsNeg: int
    H2_powerPlugsPos: int
    H2_pv1Active: int
    H2_pv1Status: int
    H2_pv2Active: int
    H2_pv2Status: int
    H2_status_06: int
    H2_status_09: int
    H2_status_10: int
    H2_unixtime_48: int
    H2_unixtime_50: int
    H2_upperLimit: int
    H2_uptime: int
    H2_wifiRssi: int
    def __init__(
        self,
        H2_pv1Active: _Optional[int] = ...,
        H2_pv1Status: _Optional[int] = ...,
        H2_pv2Active: _Optional[int] = ...,
        H2_pv2Status: _Optional[int] = ...,
        H2_X_Unknown_05: _Optional[int] = ...,
        H2_status_06: _Optional[int] = ...,
        H2_upperLimit: _Optional[int] = ...,
        H2_lowerLimit: _Optional[int] = ...,
        H2_status_09: _Optional[int] = ...,
        H2_status_10: _Optional[int] = ...,
        H2_baseLoad: _Optional[int] = ...,
        H2_powerPlugsPos: _Optional[int] = ...,
        H2_X_Unknown_13: _Optional[int] = ...,
        H2_X_Unknown_14: _Optional[int] = ...,
        H2_X_Unknown_15: _Optional[int] = ...,
        H2_X_Unknown_16: _Optional[int] = ...,
        H2_X_Unknown_17: _Optional[int] = ...,
        H2_X_Unknown_18: _Optional[int] = ...,
        H2_X_Unknown_19: _Optional[int] = ...,
        H2_X_Unknown_20: _Optional[int] = ...,
        H2_X_Unknown_21: _Optional[int] = ...,
        H2_X_Unknown_22: _Optional[int] = ...,
        H2_X_Unknown_23: _Optional[int] = ...,
        H2_X_Unknown_24: _Optional[int] = ...,
        H2_X_Unknown_25: _Optional[int] = ...,
        H2_X_Unknown_26: _Optional[int] = ...,
        H2_X_Unknown_27: _Optional[int] = ...,
        H2_X_Unknown_28: _Optional[int] = ...,
        H2_X_Unknown_29: _Optional[int] = ...,
        H2_X_Unknown_30: _Optional[int] = ...,
        H2_X_Unknown_31: _Optional[int] = ...,
        H2_uptime: _Optional[int] = ...,
        H2_X_Unknown_33: _Optional[int] = ...,
        H2_X_Unknown_34: _Optional[int] = ...,
        H2_X_Unknown_35: _Optional[int] = ...,
        H2_X_Unknown_36: _Optional[int] = ...,
        H2_X_Unknown_37: _Optional[int] = ...,
        H2_X_Unknown_38: _Optional[int] = ...,
        H2_X_Unknown_39: _Optional[int] = ...,
        H2_X_Unknown_40: _Optional[int] = ...,
        H2_X_Unknown_41: _Optional[int] = ...,
        H2_X_Unknown_42: _Optional[int] = ...,
        H2_X_Unknown_43: _Optional[int] = ...,
        H2_X_Unknown_44: _Optional[int] = ...,
        H2_gridWatt_45: _Optional[int] = ...,
        H2_powerPlugsNeg: _Optional[int] = ...,
        H2_X_Unknown_47: _Optional[int] = ...,
        H2_unixtime_48: _Optional[int] = ...,
        H2_X_Unknown_49: _Optional[int] = ...,
        H2_unixtime_50: _Optional[int] = ...,
        H2_X_Unknown_51: _Optional[int] = ...,
        H2_wifiRssi: _Optional[int] = ...,
    ) -> None: ...

class SendHeaderMsg(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: _containers.RepeatedCompositeFieldContainer[Header]
    def __init__(
        self, msg: _Optional[_Iterable[_Union[Header, _Mapping]]] = ...
    ) -> None: ...

class SetMessage(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: Header
    def __init__(self, msg: _Optional[_Union[Header, _Mapping]] = ...) -> None: ...

class SetValue(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...
