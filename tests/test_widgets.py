"""Tests for all Qlementine widget classes."""

from __future__ import annotations

import pytest

from _qt_compat import (
    QAction,
    QColor,
    QMargins,
    QPoint,
    Qlementine,
    QSize,
    Qt,
    QWidget,
)


# ============================================================
# Switch
# ============================================================


class TestSwitch:
    def test_create(self, qapp):
        assert Qlementine.Switch() is not None

    def test_default_not_tristate(self, qapp):
        assert Qlementine.Switch().isTristate() is False

    def test_set_tristate(self, qapp):
        sw = Qlementine.Switch()
        sw.setTristate(True)
        assert sw.isTristate() is True

    def test_tristate_signal(self, qtbot):
        sw = Qlementine.Switch()
        with qtbot.waitSignal(sw.tristateChanged):
            sw.setTristate(True)

    def test_default_check_state(self, qapp):
        assert Qlementine.Switch().checkState() == Qt.CheckState.Unchecked

    def test_set_check_state_checked(self, qapp):
        sw = Qlementine.Switch()
        sw.setCheckState(Qt.CheckState.Checked)
        assert sw.checkState() == Qt.CheckState.Checked

    def test_set_check_state_indeterminate(self, qapp):
        sw = Qlementine.Switch()
        sw.setTristate(True)
        sw.setCheckState(Qt.CheckState.PartiallyChecked)
        assert sw.checkState() == Qt.CheckState.PartiallyChecked

    def test_check_state_changed_signal(self, qtbot):
        sw = Qlementine.Switch()
        with qtbot.waitSignal(sw.checkStateChanged):
            sw.setCheckState(Qt.CheckState.Checked)

    def test_default_no_accessibility_symbols(self, qapp):
        assert Qlementine.Switch().showAccessibilitySymbols() is False

    def test_set_accessibility_symbols(self, qapp):
        sw = Qlementine.Switch()
        sw.setShowAccessibilitySymbols(True)
        assert sw.showAccessibilitySymbols() is True

    def test_accessibility_symbols_signal(self, qtbot):
        sw = Qlementine.Switch()
        with qtbot.waitSignal(sw.showAccessibilitySymbolsChanged):
            sw.setShowAccessibilitySymbols(True)

    def test_size_hint(self, qapp):
        sh = Qlementine.Switch().sizeHint()
        assert sh.width() > 0
        assert sh.height() > 0


# ============================================================
# Label
# ============================================================


class TestLabel:
    def test_create_empty(self, qapp):
        assert Qlementine.Label() is not None

    def test_create_with_text(self, qapp):
        assert Qlementine.Label("Hello").text() == "Hello"

    def test_create_with_text_and_role(self, qapp):
        label = Qlementine.Label("Title", Qlementine.TextRole.H1)
        assert label.text() == "Title"
        assert label.role() == Qlementine.TextRole.H1

    def test_default_role(self, qapp):
        assert Qlementine.Label().role() == Qlementine.TextRole.Default

    def test_set_role(self, qapp):
        label = Qlementine.Label()
        label.setRole(Qlementine.TextRole.H3)
        assert label.role() == Qlementine.TextRole.H3

    def test_all_text_roles(self, qapp):
        for role in (
            Qlementine.TextRole.Caption,
            Qlementine.TextRole.Default,
            Qlementine.TextRole.H1,
            Qlementine.TextRole.H2,
            Qlementine.TextRole.H3,
            Qlementine.TextRole.H4,
            Qlementine.TextRole.H5,
        ):
            label = Qlementine.Label()
            label.setRole(role)
            assert label.role() == role


# ============================================================
# LineEdit
# ============================================================


class TestLineEdit:
    def test_create(self, qapp):
        assert Qlementine.LineEdit() is not None

    def test_default_status(self, qapp):
        assert Qlementine.LineEdit().status() == Qlementine.Status.Default

    def test_set_status(self, qapp):
        le = Qlementine.LineEdit()
        le.setStatus(Qlementine.Status.Error)
        assert le.status() == Qlementine.Status.Error

    def test_all_statuses(self, qapp):
        le = Qlementine.LineEdit()
        for status in (
            Qlementine.Status.Default,
            Qlementine.Status.Info,
            Qlementine.Status.Success,
            Qlementine.Status.Warning,
            Qlementine.Status.Error,
        ):
            le.setStatus(status)
            assert le.status() == status

    def test_default_no_monospace(self, qapp):
        assert Qlementine.LineEdit().useMonoSpaceFont() is False

    def test_set_monospace(self, qapp):
        le = Qlementine.LineEdit()
        le.setUseMonoSpaceFont(True)
        assert le.useMonoSpaceFont() is True


# ============================================================
# PlainTextEdit
# ============================================================


class TestPlainTextEdit:
    def test_create(self, qapp):
        assert Qlementine.PlainTextEdit() is not None

    def test_default_status(self, qapp):
        assert Qlementine.PlainTextEdit().status() == Qlementine.Status.Default

    def test_set_status(self, qapp):
        pte = Qlementine.PlainTextEdit()
        pte.setStatus(Qlementine.Status.Success)
        assert pte.status() == Qlementine.Status.Success

    def test_default_no_monospace(self, qapp):
        assert Qlementine.PlainTextEdit().useMonoSpaceFont() is False

    def test_set_monospace(self, qapp):
        pte = Qlementine.PlainTextEdit()
        pte.setUseMonoSpaceFont(True)
        assert pte.useMonoSpaceFont() is True

    def test_size_hints(self, qapp):
        pte = Qlementine.PlainTextEdit()
        assert pte.sizeHint().width() > 0
        assert pte.minimumSizeHint().width() > 0


# ============================================================
# ColorButton
# ============================================================


class TestColorButton:
    def test_create_default(self, qapp):
        assert Qlementine.ColorButton() is not None

    def test_create_with_color(self, qapp):
        cb = Qlementine.ColorButton(QColor(255, 0, 0))
        assert cb.color() == QColor(255, 0, 0)

    def test_create_with_color_and_mode(self, qapp):
        cb = Qlementine.ColorButton(QColor(0, 255, 0), Qlementine.ColorMode.RGB)
        assert cb.color() == QColor(0, 255, 0)
        assert cb.colorMode() == Qlementine.ColorMode.RGB

    def test_default_color_mode_rgba(self, qapp):
        assert Qlementine.ColorButton().colorMode() == Qlementine.ColorMode.RGBA

    def test_set_color(self, qapp):
        cb = Qlementine.ColorButton()
        cb.setColor(QColor(0, 0, 255))
        assert cb.color() == QColor(0, 0, 255)

    def test_color_changed_signal(self, qtbot):
        cb = Qlementine.ColorButton()
        with qtbot.waitSignal(cb.colorChanged):
            cb.setColor(QColor(100, 100, 100))

    def test_set_color_mode(self, qapp):
        cb = Qlementine.ColorButton()
        cb.setColorMode(Qlementine.ColorMode.RGB)
        assert cb.colorMode() == Qlementine.ColorMode.RGB

    def test_color_mode_changed_signal(self, qtbot):
        cb = Qlementine.ColorButton()
        with qtbot.waitSignal(cb.colorModeChanged):
            cb.setColorMode(Qlementine.ColorMode.RGB)

    def test_size_hint(self, qapp):
        sh = Qlementine.ColorButton().sizeHint()
        assert sh.width() > 0
        assert sh.height() > 0


# ============================================================
# ColorEditor
# ============================================================


class TestColorEditor:
    def test_create_default(self, qapp):
        assert Qlementine.ColorEditor() is not None

    def test_create_with_color(self, qapp):
        ce = Qlementine.ColorEditor(QColor(255, 128, 0))
        assert ce.color() == QColor(255, 128, 0)

    def test_set_color(self, qapp):
        ce = Qlementine.ColorEditor()
        ce.setColor(QColor(10, 20, 30))
        assert ce.color() == QColor(10, 20, 30)

    def test_color_changed_signal(self, qtbot):
        ce = Qlementine.ColorEditor()
        with qtbot.waitSignal(ce.colorChanged):
            ce.setColor(QColor(50, 50, 50))

    def test_set_color_mode(self, qapp):
        ce = Qlementine.ColorEditor()
        ce.setColorMode(Qlementine.ColorMode.RGB)
        assert ce.colorMode() == Qlementine.ColorMode.RGB

    def test_color_mode_changed_signal(self, qtbot):
        ce = Qlementine.ColorEditor()
        with qtbot.waitSignal(ce.colorModeChanged):
            ce.setColorMode(Qlementine.ColorMode.RGB)


# ============================================================
# IconWidget
# ============================================================


class TestIconWidget:
    def test_create_default(self, qapp):
        assert Qlementine.IconWidget() is not None

    def test_size_hint(self, qapp):
        sh = Qlementine.IconWidget().sizeHint()
        assert sh.width() >= 0
        assert sh.height() >= 0

    def test_set_icon_size(self, qapp):
        iw = Qlementine.IconWidget()
        iw.setIconSize(QSize(32, 32))
        assert iw.iconSize() == QSize(32, 32)


# ============================================================
# LoadingSpinner
# ============================================================


class TestLoadingSpinner:
    def test_create(self, qapp):
        assert Qlementine.LoadingSpinner() is not None

    def test_default_not_spinning(self, qapp):
        assert Qlementine.LoadingSpinner().spinning() is False

    def test_set_spinning(self, qapp):
        sp = Qlementine.LoadingSpinner()
        sp.setSpinning(True)
        assert sp.spinning() is True

    def test_size_hints(self, qapp):
        sp = Qlementine.LoadingSpinner()
        assert sp.sizeHint().width() > 0
        assert sp.minimumSizeHint().width() > 0


# ============================================================
# NotificationBadge
# ============================================================


class TestNotificationBadge:
    def test_create(self, qapp):
        assert Qlementine.NotificationBadge() is not None

    def test_default_text_empty(self, qapp):
        assert Qlementine.NotificationBadge().text() == ""

    def test_set_text(self, qapp):
        nb = Qlementine.NotificationBadge()
        nb.setText("5")
        assert nb.text() == "5"

    def test_default_background_color_red(self, qapp):
        nb = Qlementine.NotificationBadge()
        assert nb.backgroundColor() == QColor(Qt.GlobalColor.red)

    def test_set_background_color(self, qapp):
        nb = Qlementine.NotificationBadge()
        nb.setBackgroundColor(QColor(0, 0, 255))
        assert nb.backgroundColor() == QColor(0, 0, 255)

    def test_set_foreground_color(self, qapp):
        nb = Qlementine.NotificationBadge()
        nb.setForegroundColor(QColor(0, 0, 0))
        assert nb.foregroundColor() == QColor(0, 0, 0)

    def test_set_relative_position(self, qapp):
        nb = Qlementine.NotificationBadge()
        nb.setRelativePosition(QPoint(10, -10))
        assert nb.relativePosition() == QPoint(10, -10)

    def test_set_padding(self, qapp):
        nb = Qlementine.NotificationBadge()
        m = QMargins(8, 4, 8, 4)
        nb.setPadding(m)
        assert nb.padding() == m

    def test_size_hints(self, qapp):
        nb = Qlementine.NotificationBadge()
        nb.setText("99+")
        assert nb.sizeHint().width() > 0
        assert nb.minimumSizeHint().width() > 0


# ============================================================
# Expander
# ============================================================


class TestExpander:
    def test_create(self, qapp):
        assert Qlementine.Expander() is not None

    def test_default_not_expanded(self, qapp):
        assert Qlementine.Expander().expanded() is False

    @pytest.mark.skip(reason="setExpanded(True) segfaults — binding bug")
    def test_set_expanded(self, qapp):
        e = Qlementine.Expander()
        e.setExpanded(True)
        assert e.expanded() is True

    @pytest.mark.skip(reason="toggleExpanded segfaults — binding bug")
    def test_toggle_expanded(self, qapp):
        e = Qlementine.Expander()
        e.toggleExpanded()
        assert e.expanded() is True

    def test_default_orientation_vertical(self, qapp):
        assert Qlementine.Expander().orientation() == Qt.Orientation.Vertical

    def test_set_orientation(self, qapp):
        e = Qlementine.Expander()
        e.setOrientation(Qt.Orientation.Horizontal)
        assert e.orientation() == Qt.Orientation.Horizontal

    def test_default_no_content(self, qapp):
        assert Qlementine.Expander().content() is None

    def test_set_content(self, qapp):
        e = Qlementine.Expander()
        content = QWidget()
        e.setContent(content)
        assert e.content() is content


# ============================================================
# Popover
# ============================================================


class TestPopover:
    def test_create(self, qapp):
        assert Qlementine.Popover() is not None

    def test_default_closed(self, qapp):
        p = Qlementine.Popover()
        assert p.isOpened() is False
        assert p.isClosed() is True

    def test_default_position(self, qapp):
        p = Qlementine.Popover()
        assert p.preferredPosition() == Qlementine.Popover.Position.Left

    def test_set_preferred_position(self, qapp):
        p = Qlementine.Popover()
        p.setPreferredPosition(Qlementine.Popover.Position.Bottom)
        assert p.preferredPosition() == Qlementine.Popover.Position.Bottom

    def test_preferred_position_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.preferredPositionChanged):
            p.setPreferredPosition(Qlementine.Popover.Position.Top)

    def test_default_alignment(self, qapp):
        p = Qlementine.Popover()
        assert p.preferredAlignment() == Qlementine.Popover.Alignment.Begin

    def test_set_preferred_alignment(self, qapp):
        p = Qlementine.Popover()
        p.setPreferredAlignment(Qlementine.Popover.Alignment.Center)
        assert p.preferredAlignment() == Qlementine.Popover.Alignment.Center

    def test_preferred_alignment_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.preferredAlignmentChanged):
            p.setPreferredAlignment(Qlementine.Popover.Alignment.End)

    def test_default_can_be_over_anchor(self, qapp):
        assert Qlementine.Popover().canBeOverAnchor() is True

    def test_set_can_be_over_anchor(self, qapp):
        p = Qlementine.Popover()
        p.setCanBeOverAnchor(False)
        assert p.canBeOverAnchor() is False

    def test_can_be_over_anchor_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.canBeOverAnchorChanged):
            p.setCanBeOverAnchor(False)

    def test_default_manual_positioning(self, qapp):
        assert Qlementine.Popover().manualPositioning() is False

    def test_set_manual_positioning(self, qapp):
        p = Qlementine.Popover()
        p.setManualPositioning(True)
        assert p.manualPositioning() is True

    def test_manual_positioning_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.manualPositioningChanged):
            p.setManualPositioning(True)

    def test_default_radius(self, qapp):
        assert Qlementine.Popover().radius() == 8.0

    def test_set_radius(self, qapp):
        p = Qlementine.Popover()
        p.setRadius(16.0)
        assert p.radius() == 16.0

    def test_radius_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.radiusChanged):
            p.setRadius(16.0)

    def test_default_border_width(self, qapp):
        assert Qlementine.Popover().borderWidth() == 1.0

    def test_set_border_width(self, qapp):
        p = Qlementine.Popover()
        p.setBorderWidth(2.0)
        assert p.borderWidth() == 2.0

    def test_border_width_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.borderWidthChanged):
            p.setBorderWidth(2.0)

    def test_default_drop_shadow_radius(self, qapp):
        assert Qlementine.Popover().dropShadowRadius() == 12.0

    def test_set_drop_shadow_radius(self, qapp):
        p = Qlementine.Popover()
        p.setDropShadowRadius(24.0)
        assert p.dropShadowRadius() == 24.0

    def test_drop_shadow_radius_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.dropShadowRadiusChanged):
            p.setDropShadowRadius(24.0)

    def test_set_content_widget(self, qapp):
        p = Qlementine.Popover()
        content = QWidget()
        p.setContentWidget(content)
        assert p.contentWidget() is content

    def test_content_widget_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.contentWidgetChanged):
            p.setContentWidget(QWidget())

    def test_set_anchor_widget(self, qapp):
        p = Qlementine.Popover()
        anchor = QWidget()
        p.setAnchorWidget(anchor)
        assert p.anchorWidget() is anchor

    def test_anchor_widget_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.anchorWidgetChanged):
            p.setAnchorWidget(QWidget())

    def test_set_background_color(self, qapp):
        p = Qlementine.Popover()
        p.setBackgroundColor(QColor(255, 0, 0))
        assert p.backgroundColor() == QColor(255, 0, 0)

    def test_background_color_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.backgroundColorChanged):
            p.setBackgroundColor(QColor(255, 0, 0))

    def test_set_border_color(self, qapp):
        p = Qlementine.Popover()
        p.setBorderColor(QColor(0, 255, 0))
        assert p.borderColor() == QColor(0, 255, 0)

    def test_border_color_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.borderColorChanged):
            p.setBorderColor(QColor(0, 255, 0))

    def test_set_vertical_spacing(self, qapp):
        p = Qlementine.Popover()
        p.setVerticalSpacing(20)
        assert p.verticalSpacing() == 20

    def test_vertical_spacing_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.verticalSpacingChanged):
            p.setVerticalSpacing(20)

    def test_set_horizontal_spacing(self, qapp):
        p = Qlementine.Popover()
        p.setHorizontalSpacing(15)
        assert p.horizontalSpacing() == 15

    def test_horizontal_spacing_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.horizontalSpacingChanged):
            p.setHorizontalSpacing(15)

    def test_position_enum_values(self):
        pos = Qlementine.Popover.Position
        assert pos.Left is not None
        assert pos.Top is not None
        assert pos.Right is not None
        assert pos.Bottom is not None

    def test_alignment_enum_values(self):
        align = Qlementine.Popover.Alignment
        assert align.Begin is not None
        assert align.Center is not None
        assert align.End is not None

    def test_set_content_mask_enabled(self, qapp):
        p = Qlementine.Popover()
        p.setContentMaskEnabled(True)
        assert p.contentMaskEnabled() is True

    def test_content_mask_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.contentMaskEnabledChanged):
            p.setContentMaskEnabled(True)

    def test_set_delete_content_after_closing(self, qapp):
        p = Qlementine.Popover()
        p.setDeleteContentAfterClosing(True)
        assert p.deleteContentAfterClosing() is True

    def test_delete_content_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.deleteContentAfterClosingChanged):
            p.setDeleteContentAfterClosing(True)

    def test_set_drop_shadow_color(self, qapp):
        p = Qlementine.Popover()
        p.setDropShadowColor(QColor(0, 0, 0, 128))
        assert p.dropShadowColor() == QColor(0, 0, 0, 128)

    def test_drop_shadow_color_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.dropShadowColorChanged):
            p.setDropShadowColor(QColor(0, 0, 0, 128))

    def test_set_padding(self, qapp):
        p = Qlementine.Popover()
        m = QMargins(10, 10, 10, 10)
        p.setPadding(m)
        assert p.padding() == m

    def test_padding_signal(self, qtbot):
        p = Qlementine.Popover()
        with qtbot.waitSignal(p.paddingChanged):
            p.setPadding(QMargins(10, 10, 10, 10))

    def test_set_screen_padding(self, qapp):
        p = Qlementine.Popover()
        m = QMargins(20, 20, 20, 20)
        p.setScreenPadding(m)
        assert p.screenPadding() == m

    def test_all_positions(self, qapp):
        p = Qlementine.Popover()
        for pos in (
            Qlementine.Popover.Position.Left,
            Qlementine.Popover.Position.Top,
            Qlementine.Popover.Position.Right,
            Qlementine.Popover.Position.Bottom,
        ):
            p.setPreferredPosition(pos)
            assert p.preferredPosition() == pos

    def test_all_alignments(self, qapp):
        p = Qlementine.Popover()
        for align in (
            Qlementine.Popover.Alignment.Begin,
            Qlementine.Popover.Alignment.Center,
            Qlementine.Popover.Alignment.End,
        ):
            p.setPreferredAlignment(align)
            assert p.preferredAlignment() == align


# ============================================================
# PopoverButton
# ============================================================


class TestPopoverButton:
    def test_create_default(self, qapp):
        assert Qlementine.PopoverButton() is not None

    def test_create_with_text(self, qapp):
        assert Qlementine.PopoverButton("Click me").text() == "Click me"

    def test_popover_exists(self, qapp):
        assert Qlementine.PopoverButton().popover() is not None

    def test_set_popover_content(self, qapp):
        pb = Qlementine.PopoverButton()
        content = QWidget()
        pb.setPopoverContentWidget(content)
        assert pb.popoverContentWidget() is content

    def test_popover_content_signal(self, qtbot):
        pb = Qlementine.PopoverButton()
        with qtbot.waitSignal(pb.popoverContentWidgetChanged):
            pb.setPopoverContentWidget(QWidget())


# ============================================================
# StatusBadgeWidget
# ============================================================


class TestStatusBadgeWidget:
    def test_create_default(self, qapp):
        assert Qlementine.StatusBadgeWidget() is not None

    def test_create_with_badge(self, qapp):
        sb = Qlementine.StatusBadgeWidget(Qlementine.StatusBadge.Error)
        assert sb.badge() == Qlementine.StatusBadge.Error

    def test_create_with_badge_and_size(self, qapp):
        sb = Qlementine.StatusBadgeWidget(
            Qlementine.StatusBadge.Warning, Qlementine.StatusBadgeSize.Small
        )
        assert sb.badge() == Qlementine.StatusBadge.Warning
        assert sb.badgeSize() == Qlementine.StatusBadgeSize.Small

    def test_set_badge(self, qapp):
        sb = Qlementine.StatusBadgeWidget()
        sb.setBadge(Qlementine.StatusBadge.Info)
        assert sb.badge() == Qlementine.StatusBadge.Info

    def test_set_badge_size(self, qapp):
        sb = Qlementine.StatusBadgeWidget()
        sb.setBadgeSize(Qlementine.StatusBadgeSize.Small)
        assert sb.badgeSize() == Qlementine.StatusBadgeSize.Small

    def test_all_badge_types(self, qapp):
        for badge in (
            Qlementine.StatusBadge.Success,
            Qlementine.StatusBadge.Info,
            Qlementine.StatusBadge.Warning,
            Qlementine.StatusBadge.Error,
        ):
            sb = Qlementine.StatusBadgeWidget(badge)
            assert sb.badge() == badge

    def test_size_hint(self, qapp):
        sh = Qlementine.StatusBadgeWidget().sizeHint()
        assert sh.width() > 0
        assert sh.height() > 0


# ============================================================
# RoundedFocusFrame
# ============================================================


class TestRoundedFocusFrame:
    def test_create(self, qapp):
        assert Qlementine.RoundedFocusFrame() is not None

    def test_set_radiuses(self, qapp):
        rff = Qlementine.RoundedFocusFrame()
        r = Qlementine.RadiusesF(8.0)
        rff.setRadiuses(r)
        assert rff.radiuses() == r


# ============================================================
# CommandLinkButton
# ============================================================


class TestCommandLinkButton:
    def test_create_default(self, qapp):
        assert Qlementine.CommandLinkButton() is not None

    def test_create_with_text(self, qapp):
        btn = Qlementine.CommandLinkButton("Go Forward")
        assert btn.text() == "Go Forward"

    def test_create_with_text_and_description(self, qapp):
        btn = Qlementine.CommandLinkButton("Title", "Description text here")
        assert btn.text() == "Title"
        assert btn.description() == "Description text here"

    def test_height_for_width(self, qapp):
        btn = Qlementine.CommandLinkButton("Title", "Some description")
        assert btn.heightForWidth(200) > 0

    def test_size_hint(self, qapp):
        sh = Qlementine.CommandLinkButton("Title", "Desc").sizeHint()
        assert sh.width() > 0
        assert sh.height() > 0


# ============================================================
# ActionButton
# ============================================================


class TestActionButton:
    def test_create(self, qapp):
        assert Qlementine.ActionButton() is not None

    def test_set_action(self, qapp):
        ab = Qlementine.ActionButton()
        action = QAction("Test Action")
        ab.setAction(action)
        ab.updateFromAction()
        assert ab.text() == "Test Action"


# ============================================================
# AboutDialog
# ============================================================


class TestAboutDialog:
    def test_create(self, qapp):
        assert Qlementine.AboutDialog() is not None

    def test_setters_dont_crash(self, qapp):
        """Verify all setters run without error."""
        dlg = Qlementine.AboutDialog()
        dlg.setApplicationName("TestApp")
        dlg.setApplicationVersion("1.0.0")
        dlg.setDescription("A test application")
        dlg.setWebsiteUrl("https://example.com")
        dlg.setLicense("MIT")
        dlg.setCopyright("Copyright 2024")
        dlg.addSocialMediaLink("GitHub", "https://github.com")


# ============================================================
# Menu
# ============================================================


class TestMenu:
    def test_create(self, qapp):
        assert Qlementine.Menu() is not None

    def test_update_methods_dont_crash(self, qapp):
        menu = Qlementine.Menu()
        menu.updateEnabled()
        menu.updateVisible()
        menu.updateProps()


# ============================================================
# SegmentedControl
# ============================================================


class TestSegmentedControl:
    def test_create(self, qapp):
        assert Qlementine.SegmentedControl() is not None

    def test_add_items(self, qapp):
        sc = Qlementine.SegmentedControl()
        assert sc.addItem("Tab 1") == 0
        assert sc.addItem("Tab 2") == 1
        assert sc.addItem("Tab 3") == 2
        assert sc.itemCount() == 3

    def test_default_current_index(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A")
        sc.addItem("B")
        assert sc.currentIndex() == 0

    def test_set_current_index(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A")
        sc.addItem("B")
        sc.setCurrentIndex(1)
        assert sc.currentIndex() == 1

    def test_get_item_text(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("Hello")
        assert sc.getItemText(0) == "Hello"

    def test_set_item_text(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("Old")
        sc.setItemText(0, "New")
        assert sc.getItemText(0) == "New"

    def test_remove_item(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A")
        sc.addItem("B")
        sc.addItem("C")
        assert sc.itemCount() == 3
        sc.removeItem(1)
        assert sc.itemCount() == 2
        assert sc.getItemText(0) == "A"
        assert sc.getItemText(1) == "C"

    def test_item_enabled(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A")
        assert sc.isItemEnabled(0) is True
        sc.setItemEnabled(0, False)
        assert sc.isItemEnabled(0) is False

    def test_items_should_expand(self, qapp):
        sc = Qlementine.SegmentedControl()
        assert sc.itemsShouldExpand() is False
        sc.setItemsShouldExpand(True)
        assert sc.itemsShouldExpand() is True

    def test_icon_size(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.setIconSize(QSize(24, 24))
        assert sc.iconSize() == QSize(24, 24)

    def test_move_to_next(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A")
        sc.addItem("B")
        sc.addItem("C")
        sc.setCurrentIndex(0)
        sc.moveToNextItem()
        assert sc.currentIndex() == 1
        sc.moveToNextItem()
        assert sc.currentIndex() == 2

    def test_move_to_previous(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A")
        sc.addItem("B")
        sc.addItem("C")
        sc.setCurrentIndex(2)
        sc.moveToPreviousItem()
        assert sc.currentIndex() == 1
        sc.moveToPreviousItem()
        assert sc.currentIndex() == 0

    def test_set_current_data(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A", itemData="data_a")
        sc.addItem("B", itemData="data_b")
        sc.setCurrentData("data_b")
        assert sc.currentIndex() == 1

    def test_find_item_index(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("A", itemData="alpha")
        sc.addItem("B", itemData="beta")
        assert sc.findItemIndex("alpha") == 0
        assert sc.findItemIndex("beta") == 1

    def test_set_item_badge(self, qapp):
        sc = Qlementine.SegmentedControl()
        sc.addItem("Tab")
        sc.setItemBadge(0, "3")
        assert sc.getItemBadge(0) == "3"


# ============================================================
# NavigationBar
# ============================================================


class TestNavigationBar:
    def test_create(self, qapp):
        assert Qlementine.NavigationBar() is not None

    def test_add_items(self, qapp):
        nb = Qlementine.NavigationBar()
        nb.addItem("Home")
        nb.addItem("Search")
        nb.addItem("Profile")
        assert nb.itemCount() == 3

    def test_set_current_index(self, qapp):
        nb = Qlementine.NavigationBar()
        nb.addItem("A")
        nb.addItem("B")
        nb.setCurrentIndex(1)
        assert nb.currentIndex() == 1

    def test_get_set_item_text(self, qapp):
        nb = Qlementine.NavigationBar()
        nb.addItem("Old")
        nb.setItemText(0, "New")
        assert nb.getItemText(0) == "New"

    def test_remove_item(self, qapp):
        nb = Qlementine.NavigationBar()
        nb.addItem("A")
        nb.addItem("B")
        nb.removeItem(0)
        assert nb.itemCount() == 1
        assert nb.getItemText(0) == "B"

    def test_item_data(self, qapp):
        nb = Qlementine.NavigationBar()
        nb.addItem("Home", itemData=42)
        assert nb.getItemData(0) == 42

    def test_move_navigation(self, qapp):
        nb = Qlementine.NavigationBar()
        nb.addItem("A")
        nb.addItem("B")
        nb.addItem("C")
        nb.setCurrentIndex(0)
        nb.moveToNextItem()
        assert nb.currentIndex() == 1
        nb.moveToPreviousItem()
        assert nb.currentIndex() == 0
