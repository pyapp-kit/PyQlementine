"""Tests for GeometryUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, QtCore

pytestmark = __import__("conftest").skip_no_utils


def test_point_inside_rounded_rect():
    rect = QtCore.QRectF(0, 0, 100, 100)
    center = QtCore.QPointF(50, 50)
    assert Qlementine.utils.isPointInRoundedRect(center, rect, 10.0) is True


def test_point_outside_rounded_rect():
    rect = QtCore.QRectF(0, 0, 100, 100)
    outside = QtCore.QPointF(200, 200)
    assert Qlementine.utils.isPointInRoundedRect(outside, rect, 10.0) is False


def test_point_in_corner_excluded_by_radius():
    rect = QtCore.QRectF(0, 0, 100, 100)
    # Point at the very corner, with large radius should be outside
    corner = QtCore.QPointF(0.1, 0.1)
    assert Qlementine.utils.isPointInRoundedRect(corner, rect, 50.0) is False
