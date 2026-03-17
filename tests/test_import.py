from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QApplication


def test_import():
    from PyQt6Qlementine import QlementineStyle

    assert QlementineStyle is not None


def test_create_style(qapp: QApplication):
    from PyQt6Qlementine import QlementineStyle

    style = QlementineStyle()
    assert style is not None
    assert style.animationsEnabled() is True


def test_enums():
    from PyQt6Qlementine import ColorRole, MouseState, Status, TextRole

    assert ColorRole.Primary is not None
    assert MouseState.Hovered is not None
    assert Status.Error is not None
    assert TextRole.H1 is not None


def test_widgets(qapp: QApplication):
    from PyQt6Qlementine import Label, LineEdit, LoadingSpinner, Switch

    switch = Switch()
    assert switch is not None

    label = Label("Hello")
    assert label is not None

    line_edit = LineEdit()
    assert line_edit is not None

    spinner = LoadingSpinner()
    assert spinner is not None
