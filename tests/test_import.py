"""Basic smoke tests for the Qlementine bindings import."""

from __future__ import annotations

from _qt_compat import Qlementine


def test_import():
    assert Qlementine.QlementineStyle is not None


def test_create_style(qapp):
    style = Qlementine.QlementineStyle()
    assert style is not None
    assert style.animationsEnabled() is True


def test_core_enums_exist():
    assert Qlementine.ColorRole.Primary is not None
    assert Qlementine.MouseState.Hovered is not None
    assert Qlementine.Status.Error is not None
    assert Qlementine.TextRole.H1 is not None


def test_core_widgets_construct(qapp):
    assert Qlementine.Switch() is not None
    assert Qlementine.Label("Hello") is not None
    assert Qlementine.LineEdit() is not None
    assert Qlementine.LoadingSpinner() is not None
