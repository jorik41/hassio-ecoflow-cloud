"""Helpers for the internal protobuf definitions.

This module previously imported several submodules on load which in turn
triggered the compilation of generated protobuf files. During integration
startup Home Assistant imports :mod:`_preload_proto` before these protos are
available which caused a ``TypeError`` because the required ``options.proto``
file had not yet been registered in the descriptor pool.  To avoid this
problem the imports are now performed lazily.
"""

from importlib import import_module



def __getattr__(name: str):
    if name in {"AddressId", "Command", "DirectionId"}:
        mod = import_module(".support.const", __name__)
        return getattr(mod, name)
    if name == "PrivateAPIProtoDeviceMixin":
        mod = import_module(".support.device", __name__)
        return getattr(mod, name)
    if name == "ProtoMessage":
        mod = import_module(".support.message", __name__)
        return getattr(mod, name)
    raise AttributeError(name)

__all__ = [
    "AddressId",
    "Command",
    "DirectionId",
    "PrivateAPIProtoDeviceMixin",
    "ProtoMessage",
]
