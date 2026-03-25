"""Standalone reproduction of QWidget::mapTo() warning with QlementineStyle.

Qlementine's ``WidgetWithFocusFrameEventFilter`` installs a ``QFocusFrame``
on ``QAbstractButton`` widgets (and others matching
``shouldHaveExternalFocusFrame``).  On ``QEvent::Show`` (after the initial
deferred setup via ``QTimer::singleShot``), it calls::

    _focusFrame->setWidget(nullptr);
    _focusFrame->setWidget(_widget);

``QFocusFrame::setWidget`` internally calls ``QWidget::mapTo()`` to position
the frame relative to a parent widget.  After reparenting, the
``QFocusFrame``'s parent is stale, producing::

    QWidget::mapTo(): parent must be in parent hierarchy

This happens in practice when rebuilding QtWidgets.QSplitter trees: widgets are
detached via ``setParent(None)``, then ``show()`` is called while they
are not yet in a connected widget hierarchy.

The fix in qlementine's WidgetWithFocusFrameEventFilter should guard the
``QEvent::Show`` handler — either by deferring ``setWidget`` via
``QTimer::singleShot(0, ...)`` (like the ``QEvent::Paint`` path already
does), or by checking that the widget's parent hierarchy is connected
before calling ``setWidget``.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

import pytest
from _qt_compat import QtCore, QtWidgets

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pytestqt.qtbot import QtBot


@contextmanager
def collect_qt_warnings() -> Iterator[list[str]]:
    """Collect Qt warning messages during the context."""
    warnings: list[str] = []
    prev = QtCore.qInstallMessageHandler(
        lambda _msg_type, _context, msg: warnings.append(msg)
    )
    try:
        yield warnings
    finally:
        QtCore.qInstallMessageHandler(prev)


@pytest.fixture()
def qlementine_app(qapp: QtWidgets.QApplication) -> QtWidgets.QApplication:
    try:
        from PyQt6Qlementine import QlementineStyle
    except ImportError:
        pytest.skip("PyQt6Qlementine not installed")
    qapp.setStyle(QlementineStyle())
    return qapp


def test_focus_frame_mapto_warning_on_show_after_reparent(
    qlementine_app: QtWidgets.QApplication, qtbot: QtBot
) -> None:
    """Showing a reparented widget with buttons triggers mapTo warning.

    Reproduction:
    1. Create a widget with a QtWidgets.QToolButton inside a visible QtWidgets.QSplitter
    2. Process events (Qlementine's deferred QFocusFrame setup runs)
    3. Detach the widget via setParent(None)
    4. Call show() on the detached widget (still parentless)
    -> The QtWidgets.QToolButton's QFocusFrame still references the old parent,
       so QFocusFrame::setWidget -> mapTo() warns.
    """
    toolbar = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(toolbar)
    layout.addWidget(QtWidgets.QToolButton())

    container = QtWidgets.QWidget()
    container_layout = QtWidgets.QVBoxLayout(container)
    splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
    splitter.addWidget(toolbar)
    splitter.addWidget(QtWidgets.QWidget())
    container_layout.addWidget(splitter)

    container.show()
    qtbot.waitExposed(container)

    # Let Qlementine's QTimer::singleShot(0, ...) fire to install focus frames
    QtWidgets.QApplication.processEvents()

    # Detach — toolbar is now parentless
    toolbar.setParent(None)

    with collect_qt_warnings() as warnings:
        # show() while parentless triggers the bug
        toolbar.show()
        # Process events so any deferred QTimer::singleShot(0, ...) fires too
        QtWidgets.QApplication.processEvents()

    mapto_warnings = [w for w in warnings if "mapTo" in w]

    assert len(mapto_warnings) == 0, f"Unexpected warnings: {mapto_warnings}"
