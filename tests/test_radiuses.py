"""Tests for the RadiusesF struct."""

from __future__ import annotations

from _qt_compat import Qlementine

RadiusesF = Qlementine.RadiusesF


def test_default_constructor():
    r = RadiusesF()
    assert r.topLeft == 0.0
    assert r.topRight == 0.0
    assert r.bottomRight == 0.0
    assert r.bottomLeft == 0.0


def test_uniform_constructor():
    r = RadiusesF(5.0)
    assert r.topLeft == 5.0
    assert r.topRight == 5.0
    assert r.bottomRight == 5.0
    assert r.bottomLeft == 5.0


def test_per_corner_constructor():
    r = RadiusesF(1.0, 2.0, 3.0, 4.0)
    assert r.topLeft == 1.0
    assert r.topRight == 2.0
    assert r.bottomRight == 3.0
    assert r.bottomLeft == 4.0


def test_has_same_radius_uniform():
    assert RadiusesF(5.0).hasSameRadius() is True


def test_has_same_radius_default():
    assert RadiusesF().hasSameRadius() is True


def test_has_same_radius_different():
    assert RadiusesF(1.0, 2.0, 3.0, 4.0).hasSameRadius() is False


def test_has_different_radius():
    assert RadiusesF(1.0, 2.0, 3.0, 4.0).hasDifferentRadius() is True


def test_has_different_radius_uniform():
    assert RadiusesF(5.0).hasDifferentRadius() is False


def test_equality():
    assert RadiusesF(1.0, 2.0, 3.0, 4.0) == RadiusesF(1.0, 2.0, 3.0, 4.0)


def test_inequality():
    assert RadiusesF(1.0, 2.0, 3.0, 4.0) != RadiusesF(5.0)


def test_attribute_assignment():
    r = RadiusesF()
    r.topLeft = 10.0
    r.topRight = 20.0
    r.bottomRight = 30.0
    r.bottomLeft = 40.0
    assert r.topLeft == 10.0
    assert r.topRight == 20.0
    assert r.bottomRight == 30.0
    assert r.bottomLeft == 40.0
