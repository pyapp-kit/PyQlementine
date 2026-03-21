"""Tests for BadgeUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, QtCore, QtGui

StatusBadge = Qlementine.StatusBadge
StatusBadgeSize = Qlementine.StatusBadgeSize
Theme = Qlementine.Theme

pytestmark = __import__("conftest").skip_no_utils


def test_draw_status_badge(qapp):
    pixmap = QtGui.QPixmap(64, 64)
    pixmap.fill(QtGui.QColor(255, 255, 255))
    painter = QtGui.QPainter(pixmap)
    theme = Theme()
    rect = QtCore.QRect(0, 0, 64, 64)
    Qlementine.utils.drawStatusBadge(
        painter, rect, StatusBadge.Success, StatusBadgeSize.Medium, theme
    )
    painter.end()


def test_draw_all_badge_types(qapp):
    pixmap = QtGui.QPixmap(64, 64)
    theme = Theme()
    rect = QtCore.QRect(0, 0, 64, 64)
    for badge in [
        StatusBadge.Success,
        StatusBadge.Info,
        StatusBadge.Warning,
        StatusBadge.Error,
    ]:
        for size in [StatusBadgeSize.Small, StatusBadgeSize.Medium]:
            pixmap.fill(QtGui.QColor(255, 255, 255))
            painter = QtGui.QPainter(pixmap)
            Qlementine.utils.drawStatusBadge(painter, rect, badge, size, theme)
            painter.end()
