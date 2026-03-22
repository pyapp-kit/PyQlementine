"""Tests for Theme, ThemeMeta, and ThemeManager."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from _qt_compat import QApplication, QColor, QJsonDocument, Qlementine, QSize

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot

THEMES_DIR = Path(__file__).parent / "themes"

Theme = Qlementine.Theme
ThemeMeta = Qlementine.ThemeMeta
ThemeManager = Qlementine.ThemeManager
QlementineStyle = Qlementine.QlementineStyle


# --- ThemeMeta ---


def test_theme_meta_default():
    meta = ThemeMeta()
    assert meta.name == ""
    assert meta.version == ""
    assert meta.author == ""


def test_theme_meta_set_fields():
    meta = ThemeMeta()
    meta.name = "MyTheme"
    meta.version = "1.0"
    meta.author = "Tester"
    assert meta.name == "MyTheme"
    assert meta.version == "1.0"
    assert meta.author == "Tester"


# --- Theme defaults ---


def test_theme_default_meta(qapp: QApplication) -> None:
    t = Theme()
    assert t.meta.name == ""


def test_theme_default_animation_duration(qapp: QApplication) -> None:
    assert Theme().animationDuration == 192


def test_theme_default_border_radius(qapp: QApplication) -> None:
    assert Theme().borderRadius == 6.0


def test_theme_default_control_heights(qapp: QApplication) -> None:
    t = Theme()
    assert t.controlHeightLarge == 28
    assert t.controlHeightMedium == 24
    assert t.controlHeightSmall == 16


def test_theme_default_font_size(qapp: QApplication) -> None:
    assert Theme().fontSize == 12


def test_theme_default_spacing(qapp: QApplication) -> None:
    assert Theme().spacing == 8


def test_theme_default_icon_size(qapp: QApplication) -> None:
    assert Theme().iconSize == QSize(16, 16)


def test_theme_default_border_width(qapp: QApplication) -> None:
    assert Theme().borderWidth == 1.0


# --- Theme color properties ---


def test_theme_colors_are_qcolor(qapp: QApplication) -> None:
    t = Theme()
    assert isinstance(t.backgroundColorMain1, QColor)
    assert isinstance(t.primaryColor, QColor)
    assert isinstance(t.secondaryColor, QColor)
    assert isinstance(t.statusColorSuccess, QColor)
    assert isinstance(t.statusColorInfo, QColor)
    assert isinstance(t.statusColorWarning, QColor)
    assert isinstance(t.statusColorError, QColor)
    assert isinstance(t.focusColor, QColor)
    assert isinstance(t.borderColor, QColor)


# --- Theme serialization ---


def test_theme_to_json_not_null(qapp: QApplication) -> None:
    doc = Theme().toJson()
    assert not doc.isNull()


def test_theme_json_roundtrip(qapp: QApplication) -> None:
    t = Theme()
    t.meta.name = "RoundTrip"
    t.meta.version = "2.0"
    t.meta.author = "Test"
    doc = t.toJson()
    restored = Theme.fromJsonDoc(doc)
    assert restored is not None
    assert restored.meta.name == "RoundTrip"
    assert restored.meta.version == "2.0"
    assert restored.meta.author == "Test"
    assert restored.animationDuration == t.animationDuration
    assert restored.borderRadius == t.borderRadius


def test_theme_from_json_path_light(qapp: QApplication) -> None:
    t = Theme.fromJsonPath(str(THEMES_DIR / "light.json"))
    assert t is not None
    assert t.meta.name == "Light"
    assert t.meta.author == "Olivier Cléro"
    assert t.meta.version == "1.5.0"
    assert t.backgroundColorMain1 == QColor("#ffffff")


def test_theme_from_json_path_dark(qapp: QApplication) -> None:
    t = Theme.fromJsonPath(str(THEMES_DIR / "dark.json"))
    assert t is not None
    assert t.meta.name == "Dark"
    assert t.backgroundColorMain1 == QColor("#1f2127")


def test_theme_from_json_path_nonexistent(qapp: QApplication) -> None:
    with pytest.raises(ValueError, match="Failed to load theme"):
        Theme.fromJsonPath("/nonexistent/path.json")


def test_theme_from_json_doc_with_fixture(qapp: QApplication) -> None:
    path = THEMES_DIR / "light.json"
    doc = QJsonDocument.fromJson(path.read_bytes())
    t = Theme.fromJsonDoc(doc)
    assert t is not None
    assert t.meta.name == "Light"


def test_theme_equality(qapp: QApplication) -> None:
    assert Theme() == Theme()


def test_theme_inequality_after_change(qapp: QApplication) -> None:
    a = Theme()
    b = Theme()
    b.borderRadius = 999.0
    assert a != b


# --- ThemeManager ---


def test_theme_manager_empty(qapp: QApplication) -> None:
    tm = ThemeManager()
    assert tm.themeCount() == 0
    assert tm.currentTheme() == ""


def test_theme_manager_add_theme(qapp: QApplication) -> None:
    tm = ThemeManager()
    t = Theme()
    t.meta.name = "Light"
    tm.addTheme(t)
    assert tm.themeCount() == 1


def test_theme_manager_set_current_theme(qapp: QApplication) -> None:
    tm = ThemeManager()
    t1 = Theme()
    t1.meta.name = "Light"
    t2 = Theme()
    t2.meta.name = "Dark"
    tm.addTheme(t1)
    tm.addTheme(t2)

    tm.setCurrentTheme("Dark")
    assert tm.currentTheme() == "Dark"
    assert tm.currentThemeIndex() == 1


def test_theme_manager_set_current_theme_index(qapp: QApplication) -> None:
    tm = ThemeManager()
    for name in ("A", "B", "C"):
        t = Theme()
        t.meta.name = name
        tm.addTheme(t)

    tm.setCurrentThemeIndex(2)
    assert tm.currentTheme() == "C"
    assert tm.currentThemeIndex() == 2


def test_theme_manager_theme_index_lookup(qapp: QApplication) -> None:
    tm = ThemeManager()
    for name in ("X", "Y", "Z"):
        t = Theme()
        t.meta.name = name
        tm.addTheme(t)

    assert tm.themeIndex("X") == 0
    assert tm.themeIndex("Y") == 1
    assert tm.themeIndex("Z") == 2


def test_theme_manager_next_previous(qapp: QApplication) -> None:
    tm = ThemeManager()
    for name in ("A", "B", "C"):
        t = Theme()
        t.meta.name = name
        tm.addTheme(t)

    tm.setCurrentThemeIndex(0)
    assert tm.currentTheme() == "A"

    tm.setNextTheme()
    assert tm.currentTheme() == "B"

    tm.setNextTheme()
    assert tm.currentTheme() == "C"

    tm.setPreviousTheme()
    assert tm.currentTheme() == "B"


def test_theme_manager_with_style(qapp: QApplication) -> None:
    style = QlementineStyle()
    tm = ThemeManager()
    tm.setStyle(style)

    t = Theme()
    t.meta.name = "Styled"
    t.borderRadius = 12.0
    tm.addTheme(t)
    tm.setCurrentTheme("Styled")

    # Verify the style was actually updated via the ThemeManager
    assert style.theme().borderRadius == 12.0


def test_theme_manager_constructor_with_style(qapp: QApplication) -> None:
    """Regression test for oclero/qlementine#148."""
    style = QlementineStyle()
    tm = ThemeManager(style)

    # style() previously returned nullptr
    assert tm.style() is style

    # setParent(style) in constructor caused ownership conflict,
    # invalidating the internal QPointer so setCurrentTheme silently failed
    t = Theme()
    t.meta.name = "Test"
    t.borderRadius = 42.0
    tm.addTheme(t)
    tm.setCurrentTheme("Test")
    assert tm.currentTheme() == "Test"
    assert style.theme().borderRadius == 42.0


def test_theme_manager_load_directory(qapp: QApplication) -> None:
    tm = ThemeManager()
    tm.loadDirectory(str(THEMES_DIR))
    assert tm.themeCount() == 2


def test_theme_manager_load_directory_and_select(qapp: QApplication) -> None:
    style = QlementineStyle()
    tm = ThemeManager()
    tm.setStyle(style)
    tm.loadDirectory(str(THEMES_DIR))

    tm.setCurrentTheme("Dark")
    assert tm.currentTheme() == "Dark"
    assert style.theme().backgroundColorMain1 == QColor("#1f2127")

    tm.setCurrentTheme("Light")
    assert tm.currentTheme() == "Light"
    assert style.theme().backgroundColorMain1 == QColor("#ffffff")


def test_theme_manager_load_directory_navigate(qapp: QApplication) -> None:
    tm = ThemeManager()
    tm.loadDirectory(str(THEMES_DIR))
    assert tm.themeCount() == 2

    tm.setCurrentThemeIndex(0)
    first = tm.currentTheme()
    tm.setNextTheme()
    second = tm.currentTheme()
    assert first != second
    assert {first, second} == {"Light", "Dark"}


# --- ThemeManager signals ---


def test_theme_manager_current_theme_changed_signal(qtbot: QtBot) -> None:
    tm = ThemeManager()
    for name in ("A", "B"):
        t = Theme()
        t.meta.name = name
        tm.addTheme(t)
    # addTheme auto-selects index 0 ("A"), so switching to "B" triggers the signal.
    with qtbot.waitSignal(tm.currentThemeChanged):
        tm.setCurrentTheme("B")


def test_theme_manager_theme_count_changed_signal(qtbot: QtBot) -> None:
    tm = ThemeManager()
    t = Theme()
    t.meta.name = "New"
    with qtbot.waitSignal(tm.themeCountChanged):
        tm.addTheme(t)
