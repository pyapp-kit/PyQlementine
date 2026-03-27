"""Tests for ImageUtils free functions."""

from __future__ import annotations

from _qt_compat import QColor, Qlementine, QSize, QtGui

ColorizeMode = Qlementine.ColorizeMode
RadiusesF = Qlementine.RadiusesF


def test_colorize_image(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.colorizeImage(pixmap, QColor(255, 0, 0))
    assert isinstance(result, QtGui.QImage)
    assert not result.isNull()


def test_colorize_pixmap(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.colorizePixmap(pixmap, QColor(255, 0, 0))
    assert isinstance(result, QtGui.QPixmap)
    assert not result.isNull()


def test_tint_pixmap(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.tintPixmap(pixmap, QColor(0, 255, 0))
    assert isinstance(result, QtGui.QPixmap)


def test_get_colorized_pixmap(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.getColorizedPixmap(pixmap, QColor(0, 0, 255))
    assert isinstance(result, QtGui.QPixmap)


def test_get_cached_pixmap(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.getCachedPixmap(
        pixmap, QColor(255, 0, 0), ColorizeMode.Tint
    )
    assert isinstance(result, QtGui.QPixmap)


def test_make_rounded_pixmap_single_radius(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.makeRoundedPixmap(pixmap, 5.0)
    assert isinstance(result, QtGui.QPixmap)


def test_make_rounded_pixmap_radiuses(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.makeRoundedPixmap(pixmap, RadiusesF(5.0))
    assert isinstance(result, QtGui.QPixmap)


def test_make_rounded_pixmap_four_corners(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.makeRoundedPixmap(pixmap, 1.0, 2.0, 3.0, 4.0)
    assert isinstance(result, QtGui.QPixmap)


def test_make_fit_pixmap(qapp):
    pixmap = QtGui.QPixmap(100, 50)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.makeFitPixmap(pixmap, QSize(32, 32))
    assert isinstance(result, QtGui.QPixmap)


def test_get_blurred_pixmap(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.getBlurredPixmap(pixmap, 3.0)
    assert isinstance(result, QtGui.QPixmap)


def test_get_drop_shadow_pixmap(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.getDropShadowPixmap(pixmap, 5.0)
    assert isinstance(result, QtGui.QPixmap)


def test_get_drop_shadow_pixmap_from_size(qapp):
    result = Qlementine.utils.getDropShadowPixmap(QSize(32, 32), 5.0, 3.0)
    assert isinstance(result, QtGui.QPixmap)


def test_blur_radius_necessary_space():
    result = Qlementine.utils.blurRadiusNecessarySpace(5.0)
    assert isinstance(result, int)
    assert result > 0


def test_get_extended_image_from_pixmap(qapp):
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QColor(128, 128, 128))
    result = Qlementine.utils.getExtendedImage(pixmap, 10)
    assert isinstance(result, QtGui.QImage)


def test_get_extended_image_from_image(qapp):
    image = QtGui.QImage(32, 32, QtGui.QImage.Format.Format_ARGB32)
    image.fill(QColor(128, 128, 128))
    result = Qlementine.utils.getExtendedImage(image, 10)
    assert isinstance(result, QtGui.QImage)
