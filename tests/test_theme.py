"""Tests for Theme, ThemeMeta, and ThemeManager."""

from __future__ import annotations

from _qt_compat import Qlementine, QColor, QSize

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


def test_theme_default_meta():
    t = Theme()
    assert t.meta.name == ""


def test_theme_default_animation_duration():
    assert Theme().animationDuration == 192


def test_theme_default_border_radius():
    assert Theme().borderRadius == 6.0


def test_theme_default_control_heights():
    t = Theme()
    assert t.controlHeightLarge == 28
    assert t.controlHeightMedium == 24
    assert t.controlHeightSmall == 16


def test_theme_default_font_size():
    assert Theme().fontSize == 12


def test_theme_default_spacing():
    assert Theme().spacing == 8


def test_theme_default_icon_size():
    t = Theme()
    assert t.iconSize == QSize(16, 16)


def test_theme_default_border_width():
    t = Theme()
    assert t.borderWidth == 1.0


# --- Theme color properties ---


def test_theme_colors_are_qcolor():
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


def test_theme_to_json_not_null():
    t = Theme()
    doc = t.toJson()
    assert not doc.isNull()


def test_theme_json_roundtrip():
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


def test_theme_equality():
    a = Theme()
    b = Theme()
    assert a == b


def test_theme_inequality_after_change():
    a = Theme()
    b = Theme()
    b.borderRadius = 999.0
    assert a != b


# --- ThemeManager ---


def test_theme_manager_empty(qtbot):
    tm = ThemeManager()
    assert tm.themeCount() == 0
    assert tm.currentTheme() == ""


def test_theme_manager_add_theme(qtbot):
    tm = ThemeManager()
    t = Theme()
    t.meta.name = "Light"
    tm.addTheme(t)
    assert tm.themeCount() == 1


def test_theme_manager_set_current_theme(qtbot):
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


def test_theme_manager_set_current_theme_index(qtbot):
    tm = ThemeManager()
    for name in ("A", "B", "C"):
        t = Theme()
        t.meta.name = name
        tm.addTheme(t)

    tm.setCurrentThemeIndex(2)
    assert tm.currentTheme() == "C"
    assert tm.currentThemeIndex() == 2


def test_theme_manager_theme_index_lookup(qtbot):
    tm = ThemeManager()
    for name in ("X", "Y", "Z"):
        t = Theme()
        t.meta.name = name
        tm.addTheme(t)

    assert tm.themeIndex("X") == 0
    assert tm.themeIndex("Y") == 1
    assert tm.themeIndex("Z") == 2


def test_theme_manager_next_previous(qtbot):
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


def test_theme_manager_with_style(qtbot):
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
