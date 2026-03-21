"""Tests for PrimitiveUtils free functions."""

from __future__ import annotations

from _qt_compat import QColor, Qlementine, QSize, Qt, QtCore, QtGui, QWidget

CheckState = Qlementine.CheckState
MouseState = Qlementine.MouseState
RadiusesF = Qlementine.RadiusesF
Theme = Qlementine.Theme

pytestmark = __import__("conftest").skip_no_utils


def _make_painter():
    """Create a pixmap and painter for drawing tests."""
    pixmap = QtGui.QPixmap(100, 100)
    pixmap.fill(QColor(255, 255, 255))
    painter = QtGui.QPainter(pixmap)
    return pixmap, painter


def test_get_pixel_ratio(qapp):
    w = QWidget()
    ratio = Qlementine.utils.getPixelRatio(w)
    assert isinstance(ratio, float)
    assert ratio > 0


def test_draw_ellipse_border(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawEllipseBorder(
        painter, QtCore.QRectF(10, 10, 80, 80), QColor(255, 0, 0), 2.0
    )
    painter.end()


def test_get_multiple_radiuses_rect_path(qapp):
    path = Qlementine.utils.getMultipleRadiusesRectPath(
        QtCore.QRectF(0, 0, 100, 100), RadiusesF(5.0, 10.0, 15.0, 20.0)
    )
    assert isinstance(path, QtGui.QPainterPath)


def test_draw_rounded_rect_qrectf(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRoundedRect(
        painter, QtCore.QRectF(10, 10, 80, 80), QtGui.QBrush(QColor(0, 0, 255)), 5.0
    )
    painter.end()


def test_draw_rounded_rect_qrect(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRoundedRect(
        painter, QtCore.QRect(10, 10, 80, 80), QtGui.QBrush(QColor(0, 0, 255)), 5.0
    )
    painter.end()


def test_draw_rounded_rect_qrect_radiuses(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRoundedRect(
        painter,
        QtCore.QRect(10, 10, 80, 80),
        QtGui.QBrush(QColor(0, 255, 0)),
        RadiusesF(5.0),
    )
    painter.end()


def test_draw_rounded_rect_border(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRoundedRectBorder(
        painter, QtCore.QRectF(10, 10, 80, 80), QColor(255, 0, 0), 2.0, 5.0
    )
    painter.end()


def test_draw_rounded_rect_border_radiuses(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRoundedRectBorder(
        painter,
        QtCore.QRect(10, 10, 80, 80),
        QColor(255, 0, 0),
        2.0,
        RadiusesF(5.0),
    )
    painter.end()


def test_draw_rect_border(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRectBorder(
        painter, QtCore.QRect(10, 10, 80, 80), QColor(0, 0, 0), 1.0
    )
    painter.end()


def test_draw_rounded_triangle(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRoundedTriangle(painter, QtCore.QRectF(10, 10, 80, 80), 3.0)
    painter.end()


def test_draw_checkerboard(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawCheckerboard(
        painter,
        QtCore.QRectF(0, 0, 100, 100),
        QColor(200, 200, 200),
        QColor(255, 255, 255),
        10.0,
    )
    painter.end()


def test_draw_progress_bar_value_rect(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawProgressBarValueRect(
        painter, QtCore.QRect(0, 0, 100, 20), QColor(0, 128, 255), 0.0, 100.0, 50.0
    )
    painter.end()


def test_draw_color_mark(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawColorMark(
        painter, QtCore.QRect(10, 10, 20, 20), QColor(255, 0, 0), QColor(0, 0, 0)
    )
    painter.end()


def test_draw_debug_rect(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawDebugRect(QtCore.QRect(10, 10, 80, 80), painter)
    painter.end()


def test_get_menu_indicator_path(qapp):
    path = Qlementine.utils.getMenuIndicatorPath(QtCore.QRect(0, 0, 20, 20))
    assert isinstance(path, QtGui.QPainterPath)


def test_draw_combo_box_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawComboBoxIndicator(QtCore.QRect(10, 10, 20, 20), painter)
    painter.end()


def test_draw_check_box_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawCheckBoxIndicator(QtCore.QRect(0, 0, 16, 16), painter)
    painter.end()


def test_draw_radio_button_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRadioButtonIndicator(QtCore.QRect(0, 0, 16, 16), painter)
    painter.end()


def test_draw_arrows(qapp):
    _pixmap, painter = _make_painter()
    rect = QtCore.QRect(10, 10, 20, 20)
    Qlementine.utils.drawArrowRight(rect, painter)
    Qlementine.utils.drawArrowLeft(rect, painter)
    Qlementine.utils.drawArrowDown(rect, painter)
    Qlementine.utils.drawArrowUp(rect, painter)
    painter.end()


def test_draw_close_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawCloseIndicator(QtCore.QRect(0, 0, 16, 16), painter)
    painter.end()


def test_draw_tree_view_indicator(qapp):
    _pixmap, painter = _make_painter()
    rect = QtCore.QRect(0, 0, 16, 16)
    Qlementine.utils.drawTreeViewIndicator(rect, painter, True)
    Qlementine.utils.drawTreeViewIndicator(rect, painter, False)
    painter.end()


def test_draw_calendar_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawCalendarIndicator(
        QtCore.QRect(0, 0, 16, 16), painter, QColor(0, 0, 0)
    )
    painter.end()


def test_draw_grip_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawGripIndicator(
        QtCore.QRect(0, 0, 20, 20),
        painter,
        QColor(128, 128, 128),
        Qt.Orientation.Horizontal,
    )
    painter.end()


def test_get_tick_interval():
    result = Qlementine.utils.getTickInterval(0, 1, 10, 0, 100, 200)
    assert isinstance(result, int)


def test_draw_tab(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawTab(
        painter,
        QtCore.QRect(0, 0, 80, 30),
        RadiusesF(5.0),
        QColor(200, 200, 200),
    )
    painter.end()


def test_draw_tab_shadow(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawTabShadow(
        painter,
        QtCore.QRect(0, 0, 80, 30),
        RadiusesF(5.0),
        QColor(0, 0, 0),
    )
    painter.end()


def test_draw_radio_button(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawRadioButton(
        painter,
        QtCore.QRect(0, 0, 20, 20),
        QColor(255, 255, 255),
        QColor(128, 128, 128),
        QColor(0, 120, 212),
        1.0,
        1.0,
    )
    painter.end()


def test_draw_check_button(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawCheckButton(
        painter,
        QtCore.QRect(0, 0, 20, 20),
        3.0,
        QColor(255, 255, 255),
        QColor(128, 128, 128),
        QColor(0, 120, 212),
        1.0,
        1.0,
        CheckState.Checked,
    )
    painter.end()


def test_draw_menu_separator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.utils.drawMenuSeparator(
        painter, QtCore.QRect(0, 0, 100, 2), QColor(200, 200, 200), 1
    )
    painter.end()


def test_remove_trailing_whitespaces():
    assert Qlementine.utils.removeTrailingWhitespaces("hello   ") == "hello"
    assert Qlementine.utils.removeTrailingWhitespaces("no trailing") == "no trailing"


def test_displayed_shortcut_string():
    ks = QtGui.QKeySequence("Ctrl+S")
    result = Qlementine.utils.displayedShortcutString(ks)
    assert isinstance(result, str)
    assert len(result) > 0


def test_shortcut_size_hint(qapp):
    ks = QtGui.QKeySequence("Ctrl+S")
    size = Qlementine.utils.shortcutSizeHint(ks, Theme())
    assert isinstance(size, QtCore.QSize)
    assert size.width() > 0


def test_make_check_pixmap(qapp):
    result = Qlementine.utils.makeCheckPixmap(QSize(16, 16), QColor(0, 0, 0))
    assert isinstance(result, QtGui.QPixmap)
    assert not result.isNull()


def test_make_arrow_pixmaps(qapp):
    for func in [
        Qlementine.utils.makeArrowLeftPixmap,
        Qlementine.utils.makeArrowRightPixmap,
    ]:
        result = func(QSize(16, 16), QColor(0, 0, 0))
        assert isinstance(result, QtGui.QPixmap)


def test_make_message_box_pixmaps(qapp):
    for func in [
        Qlementine.utils.makeMessageBoxWarningPixmap,
        Qlementine.utils.makeMessageBoxCriticalPixmap,
        Qlementine.utils.makeMessageBoxQuestionPixmap,
        Qlementine.utils.makeMessageBoxInformationPixmap,
    ]:
        result = func(QSize(32, 32), QColor(255, 200, 0), QColor(0, 0, 0))
        assert isinstance(result, QtGui.QPixmap)


def test_get_tab_path(qapp):
    path = Qlementine.utils.getTabPath(QtCore.QRect(0, 0, 80, 30), RadiusesF(5.0))
    assert isinstance(path, QtGui.QPainterPath)


def test_draw_elided_multi_line_text(qapp):
    pixmap, painter = _make_painter()
    Qlementine.utils.drawElidedMultiLineText(
        painter, QtCore.QRect(0, 0, 80, 80), "Hello World", pixmap
    )
    painter.end()


def test_draw_shortcut(qapp):
    _pixmap, painter = _make_painter()
    ks = QtGui.QKeySequence("Ctrl+S")
    Qlementine.utils.drawShortcut(
        painter, ks, QtCore.QRect(0, 0, 80, 20), Theme(), True
    )
    painter.end()


def test_draw_icon(qapp):
    _pixmap, painter = _make_painter()
    icon = QtGui.QIcon()
    w = QWidget()
    Qlementine.utils.drawIcon(
        QtCore.QRect(0, 0, 16, 16),
        painter,
        icon,
        MouseState.Normal,
        CheckState.NotChecked,
        w,
    )
    painter.end()
