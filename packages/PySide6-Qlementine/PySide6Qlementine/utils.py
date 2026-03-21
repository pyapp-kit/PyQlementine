"""Qlementine utility functions."""


def _init():
    import types
    from . import PySide6Qlementine as _ql

    ns = globals()
    for name in dir(_ql):
        if name.startswith("_"):
            continue
        obj = getattr(_ql, name)
        if isinstance(obj, types.BuiltinFunctionType):
            ns[name] = obj


_init()
del _init
