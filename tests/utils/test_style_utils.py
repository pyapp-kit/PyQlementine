"""Tests for StyleUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, QWidget


def test_should_have_hover_events(qapp):
    w = QWidget()
    result = Qlementine.utils.shouldHaveHoverEvents(w)
    assert isinstance(result, bool)


def test_should_have_mouse_tracking(qapp):
    w = QWidget()
    result = Qlementine.utils.shouldHaveMouseTracking(w)
    assert isinstance(result, bool)


def test_should_have_bold_font(qapp):
    w = QWidget()
    result = Qlementine.utils.shouldHaveBoldFont(w)
    assert isinstance(result, bool)


def test_should_have_external_focus_frame(qapp):
    w = QWidget()
    result = Qlementine.utils.shouldHaveExternalFocusFrame(w)
    assert isinstance(result, bool)


def test_should_have_tab_focus(qapp):
    w = QWidget()
    result = Qlementine.utils.shouldHaveTabFocus(w)
    assert isinstance(result, bool)


def test_should_not_be_vertically_compressed(qapp):
    w = QWidget()
    result = Qlementine.utils.shouldNotBeVerticallyCompressed(w)
    assert isinstance(result, bool)


def test_should_not_have_wheel_events(qapp):
    w = QWidget()
    result = Qlementine.utils.shouldNotHaveWheelEvents(w)
    assert isinstance(result, bool)


def test_get_tab_count(qapp):
    w = QWidget()
    result = Qlementine.utils.getTabCount(w)
    assert isinstance(result, int)
