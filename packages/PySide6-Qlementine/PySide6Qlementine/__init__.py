from __future__ import annotations

import sys

if sys.platform == "win32":
    try:
        import PySide6  # force Qt6/bin DLL directory registration
    except ImportError:
        raise ImportError(
            "PySide6 must be installed to use PySide6Qlementine."
        ) from None
    del PySide6

from .PySide6Qlementine import *  # noqa: F403
