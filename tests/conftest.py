from __future__ import annotations

import pytest

from _qt_compat import Qlementine

# True when the backend exposes utility free functions (PyQt6 does, PySide6
# currently does not due to shiboken overload-generation bugs).
has_utils = hasattr(Qlementine.utils, "getContrastRatio")

skip_no_utils = pytest.mark.skipif(
    not has_utils, reason="utils functions not available in this backend"
)
