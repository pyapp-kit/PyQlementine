"""Tests for ColorUtils free functions."""

from __future__ import annotations

from _qt_compat import QColor, Qlementine

pytestmark = __import__("conftest").skip_no_utils


def test_get_contrast_ratio():
    # NOTE: upstream getContrastRatio is a stub returning 4.5
    ratio = Qlementine.utils.getContrastRatio(QColor(0, 0, 0), QColor(255, 255, 255))
    assert isinstance(ratio, float)


def test_color_with_alpha_f():
    c = QColor(255, 0, 0)
    result = Qlementine.utils.colorWithAlphaF(c, 0.5)
    assert isinstance(result, QColor)
    assert abs(result.alphaF() - 0.5) < 0.01


def test_color_with_alpha():
    c = QColor(255, 0, 0)
    result = Qlementine.utils.colorWithAlpha(c, 128)
    assert isinstance(result, QColor)
    assert result.alpha() == 128


def test_get_color_source_over():
    bg = QColor(255, 255, 255, 255)
    fg = QColor(255, 0, 0, 128)
    result = Qlementine.utils.getColorSourceOver(bg, fg)
    assert isinstance(result, QColor)
    assert result.red() > 128  # blended toward red


def test_to_hex_rgb():
    result = Qlementine.utils.toHexRGB(QColor(255, 0, 128))
    assert isinstance(result, str)
    assert result.startswith("#")
    assert len(result) == 7


def test_to_hex_rgba():
    result = Qlementine.utils.toHexRGBA(QColor(255, 0, 128, 200))
    assert isinstance(result, str)
    assert result.startswith("#")
    assert len(result) == 9
