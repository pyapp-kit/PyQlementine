"""Tests for WidgetUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, QWidget



def test_make_vertical_line(qapp):
    parent = QWidget()
    line = Qlementine.utils.makeVerticalLine(parent)
    assert line is not None
    assert isinstance(line, QWidget)


def test_make_horizontal_line(qapp):
    parent = QWidget()
    line = Qlementine.utils.makeHorizontalLine(parent)
    assert line is not None
    assert isinstance(line, QWidget)


def test_make_vertical_line_with_max_height(qapp):
    parent = QWidget()
    line = Qlementine.utils.makeVerticalLine(parent, 50)
    assert line is not None


def test_center_widget(qapp):
    w = QWidget()
    # Just verify it doesn't crash
    Qlementine.utils.centerWidget(w)


def test_get_dpi(qapp):
    w = QWidget()
    dpi = Qlementine.utils.getDpi(w)
    assert isinstance(dpi, float)
    assert dpi > 0


def test_clear_focus(qapp):
    w = QWidget()
    # Just verify it doesn't crash
    Qlementine.utils.clearFocus(w, False)
    Qlementine.utils.clearFocus(w, True)
