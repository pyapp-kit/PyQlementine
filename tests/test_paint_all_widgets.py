"""Instantiate and paint every QWidget subclass under QlementineStyle."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

import pytest
from _qt_compat import QtCore, QTimer, QtWidgets

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot

SKIP = (
    "QAbstract",
    "QHeaderView",
    "QRhiWidget",
    "QRubberBand",
    "QSizeGrip",
    "QSplitterHandle",
)
# SKIP += ("QErrorMessage",)
_ALL_WIDGET_CLASSES: list[type[QtWidgets.QWidget]] = sorted(
    (
        obj
        for _name, obj in inspect.getmembers(QtWidgets)
        if inspect.isclass(obj)
        and issubclass(obj, QtWidgets.QWidget)
        and not _name.startswith(SKIP)
    ),
    key=lambda c: c.__name__,
)


def _widget_ids() -> list[str]:
    return [c.__name__ for c in _ALL_WIDGET_CLASSES]


@pytest.mark.parametrize("cls", _ALL_WIDGET_CLASSES, ids=_widget_ids())
def test_paint_widget(qlementine_app, qtbot, cls):

    widget = cls()
    qtbot.addWidget(widget)

    if isinstance(widget, QtWidgets.QDialog):
        if isinstance(widget, QtWidgets.QColorDialog):
            widget.setOption(
                QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog
            )
        if isinstance(widget, QtWidgets.QFontDialog):
            widget.setOption(QtWidgets.QFontDialog.FontDialogOption.DontUseNativeDialog)

        QTimer.singleShot(200, widget.close)
        widget.show()
    else:
        # Non-dialog widgets: show briefly, process events, then render.
        widget.show()
    qtbot.waitExposed(widget)

    # Paint to a pixmap to exercise the style's drawing code.
    w = max(widget.sizeHint().width(), 200)
    h = max(widget.sizeHint().height(), 100)
    widget.resize(w, h)
    widget.ensurePolished()
    widget.grab()

    widget.close()


def test_small_button_text_is_visible(
    qlementine_app: QtWidgets.QApplication,
    qtbot: QtBot,
) -> None:
    """Button text should be drawn even when the button is smaller than sizeHint."""
    btn_with_text = QtWidgets.QPushButton("1")
    btn_blank = QtWidgets.QPushButton("")
    qtbot.addWidget(btn_with_text)
    qtbot.addWidget(btn_blank)

    small = QtCore.QSize(30, 28)
    for btn in (btn_with_text, btn_blank):
        btn.setFixedSize(small)
        btn.ensurePolished()
        btn.show()

    qtbot.waitExposed(btn_with_text)
    qtbot.waitExposed(btn_blank)

    img_text = btn_with_text.grab().toImage()
    img_blank = btn_blank.grab().toImage()

    assert img_text != img_blank, (
        "Button with label '1' rendered identically to a blank button "
        "— text was not drawn."
    )
