from __future__ import annotations

import sys

if sys.platform == "win32":
    import os

    try:
        import PySide6
        import shiboken6
    except ImportError:
        raise ImportError(
            "PySide6 must be installed to use PySide6Qlementine."
        ) from None

    # Register DLL directories for Qt, PySide6, and shiboken6
    for _mod in (PySide6, shiboken6):
        _dir = os.path.dirname(_mod.__file__)
        os.add_dll_directory(_dir)
    # Qt DLLs may be in PySide6/Qt/bin on Windows
    _qt_bin = os.path.join(os.path.dirname(PySide6.__file__), "Qt", "bin")
    if os.path.isdir(_qt_bin):
        os.add_dll_directory(_qt_bin)

    del PySide6, shiboken6, os, _mod, _dir, _qt_bin

def _init():
    import types
    from . import PySide6Qlementine as _ql

    ns = globals()
    _promoted = frozenset({"appStyle"})
    for name in dir(_ql):
        if name.startswith("_"):
            continue
        obj = getattr(_ql, name)
        if not isinstance(obj, types.BuiltinFunctionType) or name in _promoted:
            ns[name] = obj

_init()
del _init

from . import utils as utils
