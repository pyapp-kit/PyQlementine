"""Tests for StateUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, Qt, QtWidgets

MouseState = Qlementine.MouseState
FocusState = Qlementine.FocusState
CheckState = Qlementine.CheckState
ActiveState = Qlementine.ActiveState
SelectionState = Qlementine.SelectionState
ColorRole = Qlementine.ColorRole

QStyle = QtWidgets.QStyle

pytestmark = __import__("conftest").skip_no_utils


def test_get_mouse_state_from_flags(qapp):
    state = QStyle.StateFlag.State_Enabled | QStyle.StateFlag.State_MouseOver
    result = Qlementine.utils.getMouseState(state)
    assert result == MouseState.Hovered


def test_get_mouse_state_disabled(qapp):
    state = QStyle.StateFlag(0)  # no flags = disabled
    result = Qlementine.utils.getMouseState(state)
    assert result == MouseState.Disabled


def test_get_mouse_state_from_bools(qapp):
    assert Qlementine.utils.getMouseState(False, True, True) == MouseState.Hovered
    assert Qlementine.utils.getMouseState(True, False, True) == MouseState.Pressed
    assert Qlementine.utils.getMouseState(False, False, False) == MouseState.Disabled
    assert Qlementine.utils.getMouseState(False, False, True) == MouseState.Normal


def test_get_focus_state_from_flags(qapp):
    focused = QStyle.StateFlag.State_Enabled | QStyle.StateFlag.State_HasFocus
    result = Qlementine.utils.getFocusState(focused)
    assert result == FocusState.Focused


def test_get_focus_state_from_bool(qapp):
    assert Qlementine.utils.getFocusState(True) == FocusState.Focused
    assert Qlementine.utils.getFocusState(False) == FocusState.NotFocused


def test_get_check_state_from_bool(qapp):
    assert Qlementine.utils.getCheckState(True) == CheckState.Checked
    assert Qlementine.utils.getCheckState(False) == CheckState.NotChecked


def test_get_check_state_from_qt(qapp):
    result = Qlementine.utils.getCheckState(Qt.CheckState.Checked)
    assert result == CheckState.Checked


def test_get_active_state(qapp):
    active = QStyle.StateFlag.State_Active | QStyle.StateFlag.State_Enabled
    result = Qlementine.utils.getActiveState(active)
    assert result == ActiveState.Active


def test_get_selection_state(qapp):
    selected = QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_Enabled
    result = Qlementine.utils.getSelectionState(selected)
    assert result == SelectionState.Selected


def test_get_state_roundtrip(qapp):
    state = Qlementine.utils.getState(True, True, False)
    result = Qlementine.utils.getMouseState(state)
    assert result == MouseState.Hovered


def test_get_color_role_from_check_state(qapp):
    result = Qlementine.utils.getColorRole(CheckState.Checked)
    assert isinstance(result, ColorRole)


def test_get_icon_mode(qapp):
    from _qt_compat import QtGui

    result = Qlementine.utils.getIconMode(MouseState.Normal)
    assert isinstance(result, QtGui.QIcon.Mode)


def test_get_icon_state(qapp):
    from _qt_compat import QtGui

    result = Qlementine.utils.getIconState(CheckState.Checked)
    assert isinstance(result, QtGui.QIcon.State)


def test_get_palette_color_group_from_state(qapp):
    from _qt_compat import QtGui

    state = QStyle.StateFlag.State_Enabled
    result = Qlementine.utils.getPaletteColorGroup(state)
    assert isinstance(result, QtGui.QPalette.ColorGroup)


def test_get_palette_color_group_from_mouse(qapp):
    from _qt_compat import QtGui

    result = Qlementine.utils.getPaletteColorGroup(MouseState.Normal)
    assert isinstance(result, QtGui.QPalette.ColorGroup)


def test_mouse_state_to_string(qapp):
    result = Qlementine.utils.mouseStateToString(MouseState.Hovered)
    assert isinstance(result, str)
    assert len(result) > 0


def test_focus_state_to_string(qapp):
    result = Qlementine.utils.focusStateToString(FocusState.Focused)
    assert isinstance(result, str)


def test_check_state_to_string(qapp):
    result = Qlementine.utils.checkStateToString(CheckState.Checked)
    assert isinstance(result, str)


def test_print_state(qapp):
    state = QStyle.StateFlag.State_Enabled | QStyle.StateFlag.State_MouseOver
    result = Qlementine.utils.printState(state)
    assert isinstance(result, str)
