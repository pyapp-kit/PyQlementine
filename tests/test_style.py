"""Tests for QlementineStyle."""

from __future__ import annotations

from _qt_compat import Qlementine

QlementineStyle = Qlementine.QlementineStyle
Theme = Qlementine.Theme
AutoIconColor = Qlementine.AutoIconColor


def test_create_style(qapp):
    style = QlementineStyle()
    assert style is not None


def test_animations_enabled_by_default(qapp):
    style = QlementineStyle()
    assert style.animationsEnabled() is True


def test_set_animations_disabled(qapp):
    style = QlementineStyle()
    style.setAnimationsEnabled(False)
    assert style.animationsEnabled() is False


def test_default_auto_icon_color(qapp):
    style = QlementineStyle()
    assert style.autoIconColor() == AutoIconColor.None_


def test_set_auto_icon_color(qapp):
    style = QlementineStyle()
    style.setAutoIconColor(AutoIconColor.ForegroundColor)
    assert style.autoIconColor() == AutoIconColor.ForegroundColor

    style.setAutoIconColor(AutoIconColor.TextColor)
    assert style.autoIconColor() == AutoIconColor.TextColor


def test_theme_returns_theme_object(qapp):
    style = QlementineStyle()
    theme = style.theme()
    assert isinstance(theme, Theme)


def test_set_theme(qapp):
    style = QlementineStyle()
    theme = Theme()
    theme.meta.name = "Custom"
    theme.borderRadius = 20.0
    style.setTheme(theme)
    assert style.theme().borderRadius == 20.0


def test_trigger_complete_repaint(qapp):
    """Just verify it doesn't crash."""
    style = QlementineStyle()
    style.triggerCompleteRepaint()
