from __future__ import annotations

import pytest
from _qt_compat import Qlementine, QtCore, QtWidgets

QlementineStyle = Qlementine.QlementineStyle


@pytest.fixture()
def qlementine_app(qapp: QtWidgets.QApplication):
    """Apply QlementineStyle to the application for the duration of the test."""
    style = QlementineStyle(qapp)
    qapp.setStyle(style)
    warnings: list[str] = []
    QtCore.qInstallMessageHandler(lambda mode, ctx, msg: warnings.append(msg))
    try:
        yield qapp
    finally:
        QtCore.qInstallMessageHandler(None)
    assert not warnings, "Qt warnings emitted:\n" + "\n".join(warnings)
