"""Tests for LayoutUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, QtWidgets, QWidget


def test_get_layout_margins(qapp):
    w = QWidget()
    w.setLayout(QtWidgets.QVBoxLayout())
    margins = Qlementine.utils.getLayoutMargins(w)
    assert isinstance(margins, QtWidgets.QStyle.__class__) or margins is not None


def test_get_layout_h_spacing(qapp):
    w = QWidget()
    w.setLayout(QtWidgets.QHBoxLayout())
    spacing = Qlementine.utils.getLayoutHSpacing(w)
    assert isinstance(spacing, int)


def test_get_layout_v_spacing(qapp):
    w = QWidget()
    w.setLayout(QtWidgets.QVBoxLayout())
    spacing = Qlementine.utils.getLayoutVSpacing(w)
    assert isinstance(spacing, int)


def test_clear_layout(qapp):
    w = QWidget()
    layout = QtWidgets.QVBoxLayout()
    w.setLayout(layout)
    layout.addWidget(QWidget())
    layout.addWidget(QWidget())
    assert layout.count() == 2
    Qlementine.utils.clearLayout(layout)
    assert layout.count() == 0
