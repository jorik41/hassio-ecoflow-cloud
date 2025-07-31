from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

AT_LEAST_ONCE: Qos
AT_MOST_ONCE: Qos
AVG: Operator
DERIVED_FIELD_FIELD_NUMBER: _ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
EXACTLY_ONCE: Qos
HOMIE_NODE_FIELD_NUMBER: _ClassVar[int]
MAPPING_OPTIONS_FIELD_NUMBER: _ClassVar[int]
SUM: Operator
UNSET: Qos
derived_field: _descriptor.FieldDescriptor
homie_node: _descriptor.FieldDescriptor
mapping_options: _descriptor.FieldDescriptor

class DerivedField(_message.Message):
    __slots__ = ["display_name", "field_name", "fields", "node", "operator", "unit"]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    field_name: str
    fields: _containers.RepeatedScalarFieldContainer[str]
    node: str
    operator: Operator
    unit: str
    def __init__(self, operator: _Optional[_Union[Operator, str]] = ..., field_name: _Optional[str] = ..., display_name: _Optional[str] = ..., node: _Optional[str] = ..., fields: _Optional[_Iterable[str]] = ..., unit: _Optional[str] = ...) -> None: ...

class HomieNode(_message.Message):
    __slots__ = ["id", "name", "no_retain", "qos", "type"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NO_RETAIN_FIELD_NUMBER: _ClassVar[int]
    QOS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    no_retain: bool
    qos: Qos
    type: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., no_retain: bool = ..., qos: _Optional[_Union[Qos, str]] = ...) -> None: ...

class MappingOptions(_message.Message):
    __slots__ = ["converter", "display_name", "divisor", "id", "node", "settable", "simulated_settable", "unit"]
    CONVERTER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DIVISOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    SETTABLE_FIELD_NUMBER: _ClassVar[int]
    SIMULATED_SETTABLE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    converter: str
    display_name: str
    divisor: int
    id: str
    node: str
    settable: bool
    simulated_settable: bool
    unit: str
    def __init__(self, divisor: _Optional[int] = ..., unit: _Optional[str] = ..., converter: _Optional[str] = ..., id: _Optional[str] = ..., node: _Optional[str] = ..., display_name: _Optional[str] = ..., settable: bool = ..., simulated_settable: bool = ...) -> None: ...

class Qos(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Operator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
