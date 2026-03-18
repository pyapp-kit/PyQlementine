"""Tests for all enums exposed by the Qlementine bindings."""

from __future__ import annotations

from _qt_compat import Qlementine


class TestColorRole:
    def test_members(self):
        assert Qlementine.ColorRole.Primary is not None
        assert Qlementine.ColorRole.Secondary is not None

    def test_distinct(self):
        assert Qlementine.ColorRole.Primary != Qlementine.ColorRole.Secondary


class TestMouseState:
    def test_all_members(self):
        ms = Qlementine.MouseState
        assert ms.Transparent is not None
        assert ms.Normal is not None
        assert ms.Hovered is not None
        assert ms.Pressed is not None
        assert ms.Disabled is not None

    def test_all_distinct(self):
        ms = Qlementine.MouseState
        values = {ms.Transparent, ms.Normal, ms.Hovered, ms.Pressed, ms.Disabled}
        assert len(values) == 5


class TestCheckState:
    def test_all_members(self):
        cs = Qlementine.CheckState
        assert cs.NotChecked is not None
        assert cs.Checked is not None
        assert cs.Indeterminate is not None


class TestFocusState:
    def test_all_members(self):
        assert Qlementine.FocusState.NotFocused is not None
        assert Qlementine.FocusState.Focused is not None


class TestActiveState:
    def test_all_members(self):
        assert Qlementine.ActiveState.NotActive is not None
        assert Qlementine.ActiveState.Active is not None


class TestSelectionState:
    def test_all_members(self):
        assert Qlementine.SelectionState.NotSelected is not None
        assert Qlementine.SelectionState.Selected is not None


class TestAlternateState:
    def test_all_members(self):
        assert Qlementine.AlternateState.NotAlternate is not None
        assert Qlementine.AlternateState.Alternate is not None


class TestDefaultState:
    def test_all_members(self):
        assert Qlementine.DefaultState.NotDefault is not None
        assert Qlementine.DefaultState.Default is not None


class TestStatus:
    def test_all_members(self):
        s = Qlementine.Status
        assert s.Default is not None
        assert s.Info is not None
        assert s.Success is not None
        assert s.Warning is not None
        assert s.Error is not None

    def test_all_distinct(self):
        s = Qlementine.Status
        values = {s.Default, s.Info, s.Success, s.Warning, s.Error}
        assert len(values) == 5


class TestTextRole:
    def test_all_members(self):
        tr = Qlementine.TextRole
        assert tr.Caption is not None
        assert tr.Default is not None
        assert tr.H1 is not None
        assert tr.H2 is not None
        assert tr.H3 is not None
        assert tr.H4 is not None
        assert tr.H5 is not None

    def test_all_distinct(self):
        tr = Qlementine.TextRole
        values = {tr.Caption, tr.Default, tr.H1, tr.H2, tr.H3, tr.H4, tr.H5}
        assert len(values) == 7


class TestColorMode:
    def test_all_members(self):
        assert Qlementine.ColorMode.RGB is not None
        assert Qlementine.ColorMode.RGBA is not None

    def test_distinct(self):
        assert Qlementine.ColorMode.RGB != Qlementine.ColorMode.RGBA


class TestAutoIconColor:
    def test_all_members(self):
        aic = Qlementine.AutoIconColor
        assert aic.None_ is not None
        assert aic.ForegroundColor is not None
        assert aic.TextColor is not None


class TestStatusBadge:
    def test_all_members(self):
        sb = Qlementine.StatusBadge
        assert sb.Success is not None
        assert sb.Info is not None
        assert sb.Warning is not None
        assert sb.Error is not None


class TestStatusBadgeSize:
    def test_all_members(self):
        sbs = Qlementine.StatusBadgeSize
        assert sbs.Small is not None
        assert sbs.Medium is not None


class TestColorizeMode:
    def test_all_members(self):
        cm = Qlementine.ColorizeMode
        assert cm.Colorize is not None
        assert cm.Tint is not None
