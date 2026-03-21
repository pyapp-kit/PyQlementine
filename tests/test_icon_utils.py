"""Tests for IconTheme, makeIconFromSvg, and image utility functions."""

from __future__ import annotations

import os
import tempfile

from _qt_compat import QColor, QIcon, QImage, Qlementine, QPixmap, QSize, QWidget

IconTheme = Qlementine.IconTheme
AutoIconColor = Qlementine.AutoIconColor
ColorizeMode = Qlementine.ColorizeMode


# ---- Minimal SVG for testing ----

SVG_CONTENT = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">'
    '<rect width="16" height="16" fill="black"/>'
    "</svg>"
)


def _write_svg(directory: str, name: str = "test.svg") -> str:
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        f.write(SVG_CONTENT)
    return path


# ---- IconTheme construction ----


def test_icon_theme_single_color():
    theme = IconTheme(QColor("red"))
    assert theme.normal == QColor("red")
    assert theme.disabled == QColor("red")
    assert theme.checkedNormal == QColor("red")
    assert theme.checkedDisabled == QColor("red")


def test_icon_theme_two_colors():
    theme = IconTheme(QColor("red"), QColor("gray"))
    assert theme.normal == QColor("red")
    assert theme.disabled == QColor("gray")


def test_icon_theme_four_colors():
    theme = IconTheme(QColor("red"), QColor("gray"), QColor("blue"), QColor("darkGray"))
    assert theme.normal == QColor("red")
    assert theme.disabled == QColor("gray")
    assert theme.checkedNormal == QColor("blue")
    assert theme.checkedDisabled == QColor("darkGray")


def test_icon_theme_field_assignment():
    theme = IconTheme(QColor("red"))
    theme.normal = QColor("green")
    assert theme.normal == QColor("green")


def test_icon_theme_color_method():
    theme = IconTheme(QColor("red"), QColor("gray"), QColor("blue"), QColor("darkGray"))
    assert theme.color(QIcon.Mode.Normal, QIcon.State.Off) == QColor("red")
    assert theme.color(QIcon.Mode.Disabled, QIcon.State.Off) == QColor("gray")
    assert theme.color(QIcon.Mode.Normal, QIcon.State.On) == QColor("blue")
    assert theme.color(QIcon.Mode.Disabled, QIcon.State.On) == QColor("darkGray")


# ---- makeIconFromSvg ----


def test_make_icon_from_svg_uncolored(qapp):
    with tempfile.TemporaryDirectory() as d:
        path = _write_svg(d)
        icon = Qlementine.makeIconFromSvg(path, QSize(16, 16))
        assert isinstance(icon, QIcon)
        assert not icon.isNull()


def test_make_icon_from_svg_with_theme(qapp):
    with tempfile.TemporaryDirectory() as d:
        path = _write_svg(d)
        theme = IconTheme(QColor("red"), QColor("gray"))
        icon = Qlementine.makeIconFromSvg(path, theme, QSize(16, 16))
        assert isinstance(icon, QIcon)
        assert not icon.isNull()


def test_make_icon_from_svg_themed_default_size(qapp):
    with tempfile.TemporaryDirectory() as d:
        path = _write_svg(d)
        theme = IconTheme(QColor("red"))
        icon = Qlementine.makeIconFromSvg(path, theme)
        assert isinstance(icon, QIcon)
        assert not icon.isNull()


# ---- Pixmap utility functions ----


def _make_test_pixmap() -> QPixmap:
    img = QImage(16, 16, QImage.Format.Format_ARGB32)
    img.fill(QColor("blue"))
    return QPixmap.fromImage(img)


def test_colorize_pixmap(qapp):
    src = _make_test_pixmap()
    result = Qlementine.colorizePixmap(src, QColor("red"))
    assert isinstance(result, QPixmap)
    assert not result.isNull()
    assert result.size() == src.size()


def test_tint_pixmap(qapp):
    src = _make_test_pixmap()
    result = Qlementine.tintPixmap(src, QColor("green"))
    assert isinstance(result, QPixmap)
    assert not result.isNull()


def test_get_colorized_pixmap(qapp):
    src = _make_test_pixmap()
    result = Qlementine.getColorizedPixmap(src, QColor("red"))
    assert isinstance(result, QPixmap)
    assert not result.isNull()


def test_get_colorized_pixmap_cached(qapp):
    """Calling twice should return equivalent results (cache hit)."""
    src = _make_test_pixmap()
    r1 = Qlementine.getColorizedPixmap(src, QColor("red"))
    r2 = Qlementine.getColorizedPixmap(src, QColor("red"))
    assert r1.size() == r2.size()


def test_get_tinted_pixmap(qapp):
    src = _make_test_pixmap()
    result = Qlementine.getTintedPixmap(src, QColor("yellow"))
    assert isinstance(result, QPixmap)
    assert not result.isNull()


def test_get_cached_pixmap_colorize(qapp):
    src = _make_test_pixmap()
    result = Qlementine.getCachedPixmap(src, QColor("red"), ColorizeMode.Colorize)
    assert isinstance(result, QPixmap)
    assert not result.isNull()


def test_get_cached_pixmap_tint(qapp):
    src = _make_test_pixmap()
    result = Qlementine.getCachedPixmap(src, QColor("red"), ColorizeMode.Tint)
    assert isinstance(result, QPixmap)
    assert not result.isNull()


def test_make_pixmap_from_svg(qapp):
    with tempfile.TemporaryDirectory() as d:
        path = _write_svg(d)
        result = Qlementine.makePixmapFromSvg(path, QSize(16, 16))
        assert isinstance(result, QPixmap)
        assert not result.isNull()
        assert result.size() == QSize(16, 16)


def test_make_pixmap_from_svg_layered(qapp):
    with tempfile.TemporaryDirectory() as d:
        bg = _write_svg(d, "bg.svg")
        fg = _write_svg(d, "fg.svg")
        result = Qlementine.makePixmapFromSvg(
            bg, QColor("white"), fg, QColor("black"), QSize(16, 16)
        )
        assert isinstance(result, QPixmap)
        assert not result.isNull()


# ---- QlementineStyle.getColorizedPixmap ----


def test_style_get_colorized_pixmap(qapp):
    style = Qlementine.QlementineStyle()
    src = _make_test_pixmap()
    result = style.getColorizedPixmap(
        src, AutoIconColor.ForegroundColor, QColor("red"), QColor("blue")
    )
    assert isinstance(result, QPixmap)


def test_style_get_colorized_pixmap_none(qapp):
    """AutoIconColor.None_ should return the original pixmap unmodified."""
    style = Qlementine.QlementineStyle()
    src = _make_test_pixmap()
    result = style.getColorizedPixmap(
        src, AutoIconColor.None_, QColor("red"), QColor("blue")
    )
    assert isinstance(result, QPixmap)
    assert result.size() == src.size()


def test_style_get_colorized_pixmap_text_color(qapp):
    style = Qlementine.QlementineStyle()
    src = _make_test_pixmap()
    result = style.getColorizedPixmap(
        src, AutoIconColor.TextColor, QColor("red"), QColor("blue")
    )
    assert isinstance(result, QPixmap)


# ---- Per-widget autoIconColor ----


def test_per_widget_auto_icon_color(qapp):
    style = Qlementine.QlementineStyle()
    w = QWidget()
    w.setStyle(style)
    Qlementine.QlementineStyle.setAutoIconColor(w, AutoIconColor.ForegroundColor)
    assert style.autoIconColor(w) == AutoIconColor.ForegroundColor


def test_per_widget_auto_icon_color_text(qapp):
    style = Qlementine.QlementineStyle()
    w = QWidget()
    w.setStyle(style)
    Qlementine.QlementineStyle.setAutoIconColor(w, AutoIconColor.TextColor)
    assert style.autoIconColor(w) == AutoIconColor.TextColor
