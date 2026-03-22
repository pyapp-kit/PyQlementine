"""Tests for IconUtils free functions and IconTheme struct."""

from __future__ import annotations

import tempfile
from pathlib import Path

from _qt_compat import QColor, QIcon, Qlementine, QSize

IconTheme = Qlementine.IconTheme


SVG_CONTENT = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'
    "<circle cx='8' cy='8' r='6'/></svg>"
)


def test_icon_theme_single_color():
    theme = IconTheme(QColor(255, 0, 0))
    assert theme.normal == QColor(255, 0, 0)


def test_icon_theme_two_colors():
    theme = IconTheme(QColor(255, 0, 0), QColor(128, 128, 128))
    assert theme.normal == QColor(255, 0, 0)
    assert theme.disabled == QColor(128, 128, 128)


def test_icon_theme_four_colors():
    theme = IconTheme(
        QColor(255, 0, 0),
        QColor(128, 128, 128),
        QColor(0, 255, 0),
        QColor(64, 64, 64),
    )
    assert theme.checkedNormal == QColor(0, 255, 0)
    assert theme.checkedDisabled == QColor(64, 64, 64)


def test_icon_theme_color_method():
    theme = IconTheme(QColor(255, 0, 0), QColor(128, 128, 128))
    color = theme.color(QIcon.Mode.Normal, QIcon.State.Off)
    assert color == QColor(255, 0, 0)
    color = theme.color(QIcon.Mode.Disabled, QIcon.State.Off)
    assert color == QColor(128, 128, 128)


def test_make_icon_from_svg(qapp, tmp_path):
    svg_file = tmp_path / "icon.svg"
    svg_file.write_text(SVG_CONTENT)
    icon = Qlementine.utils.makeIconFromSvg(str(svg_file), QSize(16, 16))
    assert isinstance(icon, QIcon)


def test_make_icon_from_svg_with_theme(qapp, tmp_path):
    svg_file = tmp_path / "icon.svg"
    svg_file.write_text(SVG_CONTENT)
    theme = IconTheme(QColor(255, 0, 0))
    icon = Qlementine.utils.makeIconFromSvg(str(svg_file), theme, QSize(16, 16))
    assert isinstance(icon, QIcon)
