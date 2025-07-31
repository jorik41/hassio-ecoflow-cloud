"""Preload protocol buffer modules and set up package aliases."""

from importlib import import_module
import sys

# The generated protobuf modules expect the package ``model.protos`` to be
# importable. When Home Assistant loads this integration as a custom component,
# the Python path does not include this subpackage.  To keep the generated code
# unchanged, expose the package here before importing any of the ``*_pb2``
# modules.
_model_pkg = import_module(".devices.internal.proto.model", __package__)
sys.modules.setdefault("model", _model_pkg)
sys.modules.setdefault(
    "model.protos", import_module(".devices.internal.proto.model.protos", __package__)
)

from .devices.internal.proto.model.protos import (  # noqa: F401
    options_pb2,  # noqa: F401 # pyright: ignore[reportUnusedImport]
)
from .devices.internal.proto import (  # noqa: F401
    ecopacket_pb2,  # noqa: F401 # pyright: ignore[reportUnusedImport]
    platform_pb2,  # noqa: F401 # pyright: ignore[reportUnusedImport]
    powerstream_pb2,  # noqa: F401 # pyright: ignore[reportUnusedImport]
    deltapro3_pb2,  # noqa: F401 # pyright: ignore[reportUnusedImport]
)
