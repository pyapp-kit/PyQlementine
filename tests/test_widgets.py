"""Tests for all Qlementine widget classes."""

from __future__ import annotations

from _qt_compat import (
    QAction,
    QColor,
    Qlementine,
    QMargins,
    QPoint,
    QSize,
    Qt,
    QWidget,
)

# ============================================================
# Switch
# ============================================================


def test_switch_create(qapp):
    assert Qlementine.Switch() is not None


def test_switch_default_not_tristate(qapp):
    assert Qlementine.Switch().isTristate() is False


def test_switch_set_tristate(qapp):
    sw = Qlementine.Switch()
    sw.setTristate(True)
    assert sw.isTristate() is True


def test_switch_tristate_signal(qtbot):
    sw = Qlementine.Switch()
    with qtbot.waitSignal(sw.tristateChanged):
        sw.setTristate(True)


def test_switch_default_check_state(qapp):
    assert Qlementine.Switch().checkState() == Qt.CheckState.Unchecked


def test_switch_set_check_state_checked(qapp):
    sw = Qlementine.Switch()
    sw.setCheckState(Qt.CheckState.Checked)
    assert sw.checkState() == Qt.CheckState.Checked


def test_switch_set_check_state_indeterminate(qapp):
    sw = Qlementine.Switch()
    sw.setTristate(True)
    sw.setCheckState(Qt.CheckState.PartiallyChecked)
    assert sw.checkState() == Qt.CheckState.PartiallyChecked


def test_switch_check_state_changed_signal(qtbot):
    sw = Qlementine.Switch()
    with qtbot.waitSignal(sw.checkStateChanged):
        sw.setCheckState(Qt.CheckState.Checked)


def test_switch_default_no_accessibility_symbols(qapp):
    assert Qlementine.Switch().showAccessibilitySymbols() is False


def test_switch_set_accessibility_symbols(qapp):
    sw = Qlementine.Switch()
    sw.setShowAccessibilitySymbols(True)
    assert sw.showAccessibilitySymbols() is True


def test_switch_accessibility_symbols_signal(qtbot):
    sw = Qlementine.Switch()
    with qtbot.waitSignal(sw.showAccessibilitySymbolsChanged):
        sw.setShowAccessibilitySymbols(True)


def test_switch_size_hint(qapp):
    sh = Qlementine.Switch().sizeHint()
    assert sh.width() > 0
    assert sh.height() > 0


# ============================================================
# Label
# ============================================================


def test_label_create_empty(qapp):
    assert Qlementine.Label() is not None


def test_label_create_with_text(qapp):
    assert Qlementine.Label("Hello").text() == "Hello"


def test_label_create_with_text_and_role(qapp):
    label = Qlementine.Label("Title", Qlementine.TextRole.H1)
    assert label.text() == "Title"
    assert label.role() == Qlementine.TextRole.H1


def test_label_default_role(qapp):
    assert Qlementine.Label().role() == Qlementine.TextRole.Default


def test_label_set_role(qapp):
    label = Qlementine.Label()
    label.setRole(Qlementine.TextRole.H3)
    assert label.role() == Qlementine.TextRole.H3


def test_label_all_text_roles(qapp):
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


def test_line_edit_create(qapp):
    assert Qlementine.LineEdit() is not None


def test_line_edit_default_status(qapp):
    assert Qlementine.LineEdit().status() == Qlementine.Status.Default


def test_line_edit_set_status(qapp):
    le = Qlementine.LineEdit()
    le.setStatus(Qlementine.Status.Error)
    assert le.status() == Qlementine.Status.Error


def test_line_edit_all_statuses(qapp):
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


def test_line_edit_default_no_monospace(qapp):
    assert Qlementine.LineEdit().useMonoSpaceFont() is False


def test_line_edit_set_monospace(qapp):
    le = Qlementine.LineEdit()
    le.setUseMonoSpaceFont(True)
    assert le.useMonoSpaceFont() is True


# ============================================================
# PlainTextEdit
# ============================================================


def test_plain_text_edit_create(qapp):
    assert Qlementine.PlainTextEdit() is not None


def test_plain_text_edit_default_status(qapp):
    assert Qlementine.PlainTextEdit().status() == Qlementine.Status.Default


def test_plain_text_edit_set_status(qapp):
    pte = Qlementine.PlainTextEdit()
    pte.setStatus(Qlementine.Status.Success)
    assert pte.status() == Qlementine.Status.Success


def test_plain_text_edit_default_no_monospace(qapp):
    assert Qlementine.PlainTextEdit().useMonoSpaceFont() is False


def test_plain_text_edit_set_monospace(qapp):
    pte = Qlementine.PlainTextEdit()
    pte.setUseMonoSpaceFont(True)
    assert pte.useMonoSpaceFont() is True


def test_plain_text_edit_size_hints(qapp):
    pte = Qlementine.PlainTextEdit()
    assert pte.sizeHint().width() > 0
    assert pte.minimumSizeHint().width() > 0


# ============================================================
# ColorButton
# ============================================================


def test_color_button_create(qapp):
    assert Qlementine.ColorButton() is not None


def test_color_button_create_with_color(qapp):
    cb = Qlementine.ColorButton(QColor(255, 0, 0))
    assert cb.color() == QColor(255, 0, 0)


def test_color_button_create_with_color_and_mode(qapp):
    cb = Qlementine.ColorButton(QColor(0, 255, 0), Qlementine.ColorMode.RGB)
    assert cb.color() == QColor(0, 255, 0)
    assert cb.colorMode() == Qlementine.ColorMode.RGB


def test_color_button_default_color_mode_rgba(qapp):
    assert Qlementine.ColorButton().colorMode() == Qlementine.ColorMode.RGBA


def test_color_button_set_color(qapp):
    cb = Qlementine.ColorButton()
    cb.setColor(QColor(0, 0, 255))
    assert cb.color() == QColor(0, 0, 255)


def test_color_button_color_changed_signal(qtbot):
    cb = Qlementine.ColorButton()
    with qtbot.waitSignal(cb.colorChanged):
        cb.setColor(QColor(100, 100, 100))


def test_color_button_set_color_mode(qapp):
    cb = Qlementine.ColorButton()
    cb.setColorMode(Qlementine.ColorMode.RGB)
    assert cb.colorMode() == Qlementine.ColorMode.RGB


def test_color_button_color_mode_changed_signal(qtbot):
    cb = Qlementine.ColorButton()
    with qtbot.waitSignal(cb.colorModeChanged):
        cb.setColorMode(Qlementine.ColorMode.RGB)


def test_color_button_size_hint(qapp):
    sh = Qlementine.ColorButton().sizeHint()
    assert sh.width() > 0
    assert sh.height() > 0


# ============================================================
# ColorEditor
# ============================================================


def test_color_editor_create(qapp):
    assert Qlementine.ColorEditor() is not None


def test_color_editor_create_with_color(qapp):
    ce = Qlementine.ColorEditor(QColor(255, 128, 0))
    assert ce.color() == QColor(255, 128, 0)


def test_color_editor_set_color(qapp):
    ce = Qlementine.ColorEditor()
    ce.setColor(QColor(10, 20, 30))
    assert ce.color() == QColor(10, 20, 30)


def test_color_editor_color_changed_signal(qtbot):
    ce = Qlementine.ColorEditor()
    with qtbot.waitSignal(ce.colorChanged):
        ce.setColor(QColor(50, 50, 50))


def test_color_editor_set_color_mode(qapp):
    ce = Qlementine.ColorEditor()
    ce.setColorMode(Qlementine.ColorMode.RGB)
    assert ce.colorMode() == Qlementine.ColorMode.RGB


def test_color_editor_color_mode_changed_signal(qtbot):
    ce = Qlementine.ColorEditor()
    with qtbot.waitSignal(ce.colorModeChanged):
        ce.setColorMode(Qlementine.ColorMode.RGB)


# ============================================================
# IconWidget
# ============================================================


def test_icon_widget_create(qapp):
    assert Qlementine.IconWidget() is not None


def test_icon_widget_size_hint(qapp):
    sh = Qlementine.IconWidget().sizeHint()
    assert sh.width() >= 0
    assert sh.height() >= 0


def test_icon_widget_set_icon_size(qapp):
    iw = Qlementine.IconWidget()
    iw.setIconSize(QSize(32, 32))
    assert iw.iconSize() == QSize(32, 32)


# ============================================================
# LoadingSpinner
# ============================================================


def test_loading_spinner_create(qapp):
    assert Qlementine.LoadingSpinner() is not None


def test_loading_spinner_default_not_spinning(qapp):
    assert Qlementine.LoadingSpinner().spinning() is False


def test_loading_spinner_set_spinning(qapp):
    sp = Qlementine.LoadingSpinner()
    sp.setSpinning(True)
    assert sp.spinning() is True


def test_loading_spinner_size_hints(qapp):
    sp = Qlementine.LoadingSpinner()
    assert sp.sizeHint().width() > 0
    assert sp.minimumSizeHint().width() > 0


# ============================================================
# NotificationBadge
# ============================================================


def test_notification_badge_create(qapp):
    assert Qlementine.NotificationBadge() is not None


def test_notification_badge_default_text_empty(qapp):
    assert Qlementine.NotificationBadge().text() == ""


def test_notification_badge_set_text(qapp):
    nb = Qlementine.NotificationBadge()
    nb.setText("5")
    assert nb.text() == "5"


def test_notification_badge_set_background_color(qapp):
    nb = Qlementine.NotificationBadge()
    assert nb.backgroundColor() != QColor(0, 0, 255)
    nb.setBackgroundColor(QColor(0, 0, 255))
    assert nb.backgroundColor() == QColor(0, 0, 255)


def test_notification_badge_set_foreground_color(qapp):
    nb = Qlementine.NotificationBadge()
    assert nb.foregroundColor() != QColor(0, 0, 0)
    nb.setForegroundColor(QColor(0, 0, 0))
    assert nb.foregroundColor() == QColor(0, 0, 0)


def test_notification_badge_set_relative_position(qapp):
    nb = Qlementine.NotificationBadge()
    nb.setRelativePosition(QPoint(10, -10))
    assert nb.relativePosition() == QPoint(10, -10)


def test_notification_badge_set_padding(qapp):
    nb = Qlementine.NotificationBadge()
    m = QMargins(8, 4, 8, 4)
    nb.setPadding(m)
    assert nb.padding() == m


def test_notification_badge_size_hints(qapp):
    nb = Qlementine.NotificationBadge()
    nb.setText("99+")
    assert nb.sizeHint().width() > 0
    assert nb.minimumSizeHint().width() > 0


# ============================================================
# Expander
# ============================================================


def test_expander_create(qapp):
    assert Qlementine.Expander() is not None


def test_expander_default_not_expanded(qapp):
    assert Qlementine.Expander().expanded() is False


def test_expander_set_expanded(qapp):
    e = Qlementine.Expander()
    e.setExpanded(True)
    assert e.expanded() is True


def test_expander_toggle_expanded(qapp):
    e = Qlementine.Expander()
    e.toggleExpanded()
    assert e.expanded() is True


def test_expander_default_orientation_vertical(qapp):
    assert Qlementine.Expander().orientation() == Qt.Orientation.Vertical


def test_expander_set_orientation(qapp):
    e = Qlementine.Expander()
    e.setOrientation(Qt.Orientation.Horizontal)
    assert e.orientation() == Qt.Orientation.Horizontal


def test_expander_default_no_content(qapp):
    assert Qlementine.Expander().content() is None


def test_expander_set_content(qapp):
    e = Qlementine.Expander()
    content = QWidget()
    e.setContent(content)
    assert e.content() is content


# ============================================================
# Popover
# ============================================================


def test_popover_create(qapp):
    assert Qlementine.Popover() is not None


def test_popover_default_closed(qapp):
    p = Qlementine.Popover()
    assert p.isOpened() is False
    assert p.isClosed() is True


def test_popover_default_position(qapp):
    assert Qlementine.Popover().preferredPosition() == Qlementine.Popover.Position.Left


def test_popover_set_preferred_position(qapp):
    p = Qlementine.Popover()
    p.setPreferredPosition(Qlementine.Popover.Position.Bottom)
    assert p.preferredPosition() == Qlementine.Popover.Position.Bottom


def test_popover_preferred_position_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.preferredPositionChanged):
        p.setPreferredPosition(Qlementine.Popover.Position.Top)


def test_popover_default_alignment(qapp):
    assert (
        Qlementine.Popover().preferredAlignment() == Qlementine.Popover.Alignment.Begin
    )


def test_popover_set_preferred_alignment(qapp):
    p = Qlementine.Popover()
    p.setPreferredAlignment(Qlementine.Popover.Alignment.Center)
    assert p.preferredAlignment() == Qlementine.Popover.Alignment.Center


def test_popover_preferred_alignment_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.preferredAlignmentChanged):
        p.setPreferredAlignment(Qlementine.Popover.Alignment.End)


def test_popover_default_can_be_over_anchor(qapp):
    assert Qlementine.Popover().canBeOverAnchor() is True


def test_popover_set_can_be_over_anchor(qapp):
    p = Qlementine.Popover()
    p.setCanBeOverAnchor(False)
    assert p.canBeOverAnchor() is False


def test_popover_can_be_over_anchor_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.canBeOverAnchorChanged):
        p.setCanBeOverAnchor(False)


def test_popover_default_manual_positioning(qapp):
    assert Qlementine.Popover().manualPositioning() is False


def test_popover_set_manual_positioning(qapp):
    p = Qlementine.Popover()
    p.setManualPositioning(True)
    assert p.manualPositioning() is True


def test_popover_manual_positioning_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.manualPositioningChanged):
        p.setManualPositioning(True)


def test_popover_default_radius(qapp):
    assert Qlementine.Popover().radius() == 8.0


def test_popover_set_radius(qapp):
    p = Qlementine.Popover()
    p.setRadius(16.0)
    assert p.radius() == 16.0


def test_popover_radius_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.radiusChanged):
        p.setRadius(16.0)


def test_popover_default_border_width(qapp):
    assert Qlementine.Popover().borderWidth() == 1.0


def test_popover_set_border_width(qapp):
    p = Qlementine.Popover()
    p.setBorderWidth(2.0)
    assert p.borderWidth() == 2.0


def test_popover_border_width_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.borderWidthChanged):
        p.setBorderWidth(2.0)


def test_popover_default_drop_shadow_radius(qapp):
    assert Qlementine.Popover().dropShadowRadius() == 12.0


def test_popover_set_drop_shadow_radius(qapp):
    p = Qlementine.Popover()
    p.setDropShadowRadius(24.0)
    assert p.dropShadowRadius() == 24.0


def test_popover_drop_shadow_radius_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.dropShadowRadiusChanged):
        p.setDropShadowRadius(24.0)


def test_popover_set_content_widget(qapp):
    p = Qlementine.Popover()
    content = QWidget()
    p.setContentWidget(content)
    assert p.contentWidget() is content


def test_popover_content_widget_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.contentWidgetChanged):
        p.setContentWidget(QWidget())


def test_popover_set_anchor_widget(qapp):
    p = Qlementine.Popover()
    anchor = QWidget()
    p.setAnchorWidget(anchor)
    assert p.anchorWidget() is anchor


def test_popover_anchor_widget_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.anchorWidgetChanged):
        p.setAnchorWidget(QWidget())


def test_popover_set_background_color(qapp):
    p = Qlementine.Popover()
    p.setBackgroundColor(QColor(255, 0, 0))
    assert p.backgroundColor() == QColor(255, 0, 0)


def test_popover_background_color_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.backgroundColorChanged):
        p.setBackgroundColor(QColor(255, 0, 0))


def test_popover_set_border_color(qapp):
    p = Qlementine.Popover()
    p.setBorderColor(QColor(0, 255, 0))
    assert p.borderColor() == QColor(0, 255, 0)


def test_popover_border_color_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.borderColorChanged):
        p.setBorderColor(QColor(0, 255, 0))


def test_popover_set_vertical_spacing(qapp):
    p = Qlementine.Popover()
    p.setVerticalSpacing(20)
    assert p.verticalSpacing() == 20


def test_popover_vertical_spacing_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.verticalSpacingChanged):
        p.setVerticalSpacing(20)


def test_popover_set_horizontal_spacing(qapp):
    p = Qlementine.Popover()
    p.setHorizontalSpacing(15)
    assert p.horizontalSpacing() == 15


def test_popover_horizontal_spacing_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.horizontalSpacingChanged):
        p.setHorizontalSpacing(15)


def test_popover_position_enum_values():
    pos = Qlementine.Popover.Position
    assert pos.Left is not None
    assert pos.Top is not None
    assert pos.Right is not None
    assert pos.Bottom is not None


def test_popover_alignment_enum_values():
    align = Qlementine.Popover.Alignment
    assert align.Begin is not None
    assert align.Center is not None
    assert align.End is not None


def test_popover_set_content_mask_enabled(qapp):
    p = Qlementine.Popover()
    p.setContentMaskEnabled(True)
    assert p.contentMaskEnabled() is True


def test_popover_content_mask_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.contentMaskEnabledChanged):
        p.setContentMaskEnabled(True)


def test_popover_set_delete_content_after_closing(qapp):
    p = Qlementine.Popover()
    p.setDeleteContentAfterClosing(True)
    assert p.deleteContentAfterClosing() is True


def test_popover_delete_content_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.deleteContentAfterClosingChanged):
        p.setDeleteContentAfterClosing(True)


def test_popover_set_drop_shadow_color(qapp):
    p = Qlementine.Popover()
    p.setDropShadowColor(QColor(0, 0, 0, 128))
    assert p.dropShadowColor() == QColor(0, 0, 0, 128)


def test_popover_drop_shadow_color_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.dropShadowColorChanged):
        p.setDropShadowColor(QColor(0, 0, 0, 128))


def test_popover_set_padding(qapp):
    p = Qlementine.Popover()
    m = QMargins(10, 10, 10, 10)
    p.setPadding(m)
    assert p.padding() == m


def test_popover_padding_signal(qtbot):
    p = Qlementine.Popover()
    with qtbot.waitSignal(p.paddingChanged):
        p.setPadding(QMargins(10, 10, 10, 10))


def test_popover_set_screen_padding(qapp):
    p = Qlementine.Popover()
    m = QMargins(20, 20, 20, 20)
    p.setScreenPadding(m)
    assert p.screenPadding() == m


def test_popover_all_positions(qapp):
    p = Qlementine.Popover()
    for pos in (
        Qlementine.Popover.Position.Left,
        Qlementine.Popover.Position.Top,
        Qlementine.Popover.Position.Right,
        Qlementine.Popover.Position.Bottom,
    ):
        p.setPreferredPosition(pos)
        assert p.preferredPosition() == pos


def test_popover_all_alignments(qapp):
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


def test_popover_button_create(qapp):
    assert Qlementine.PopoverButton() is not None


def test_popover_button_create_with_text(qapp):
    assert Qlementine.PopoverButton("Click me").text() == "Click me"


def test_popover_button_popover_exists(qapp):
    assert Qlementine.PopoverButton().popover() is not None


def test_popover_button_set_content(qapp):
    pb = Qlementine.PopoverButton()
    content = QWidget()
    pb.setPopoverContentWidget(content)
    assert pb.popoverContentWidget() is content


def test_popover_button_content_signal(qtbot):
    pb = Qlementine.PopoverButton()
    with qtbot.waitSignal(pb.popoverContentWidgetChanged):
        pb.setPopoverContentWidget(QWidget())


# ============================================================
# StatusBadgeWidget
# ============================================================


def test_status_badge_widget_create(qapp):
    assert Qlementine.StatusBadgeWidget() is not None


def test_status_badge_widget_create_with_badge(qapp):
    sb = Qlementine.StatusBadgeWidget(Qlementine.StatusBadge.Error)
    assert sb.badge() == Qlementine.StatusBadge.Error


def test_status_badge_widget_create_with_badge_and_size(qapp):
    sb = Qlementine.StatusBadgeWidget(
        Qlementine.StatusBadge.Warning, Qlementine.StatusBadgeSize.Small
    )
    assert sb.badge() == Qlementine.StatusBadge.Warning
    assert sb.badgeSize() == Qlementine.StatusBadgeSize.Small


def test_status_badge_widget_set_badge(qapp):
    sb = Qlementine.StatusBadgeWidget()
    sb.setBadge(Qlementine.StatusBadge.Info)
    assert sb.badge() == Qlementine.StatusBadge.Info


def test_status_badge_widget_set_badge_size(qapp):
    sb = Qlementine.StatusBadgeWidget()
    sb.setBadgeSize(Qlementine.StatusBadgeSize.Small)
    assert sb.badgeSize() == Qlementine.StatusBadgeSize.Small


def test_status_badge_widget_all_badge_types(qapp):
    for badge in (
        Qlementine.StatusBadge.Success,
        Qlementine.StatusBadge.Info,
        Qlementine.StatusBadge.Warning,
        Qlementine.StatusBadge.Error,
    ):
        sb = Qlementine.StatusBadgeWidget(badge)
        assert sb.badge() == badge


def test_status_badge_widget_size_hint(qapp):
    sh = Qlementine.StatusBadgeWidget().sizeHint()
    assert sh.width() > 0
    assert sh.height() > 0


# ============================================================
# RoundedFocusFrame
# ============================================================


def test_rounded_focus_frame_create(qapp):
    assert Qlementine.RoundedFocusFrame() is not None


def test_rounded_focus_frame_set_radiuses(qapp):
    rff = Qlementine.RoundedFocusFrame()
    r = Qlementine.RadiusesF(8.0)
    rff.setRadiuses(r)
    assert rff.radiuses() == r


# ============================================================
# CommandLinkButton
# ============================================================


def test_command_link_button_create(qapp):
    assert Qlementine.CommandLinkButton() is not None


def test_command_link_button_create_with_text(qapp):
    btn = Qlementine.CommandLinkButton("Go Forward")
    assert btn.text() == "Go Forward"


def test_command_link_button_create_with_text_and_description(qapp):
    btn = Qlementine.CommandLinkButton("Title", "Description text here")
    assert btn.text() == "Title"
    assert btn.description() == "Description text here"


def test_command_link_button_height_for_width(qapp):
    btn = Qlementine.CommandLinkButton("Title", "Some description")
    assert btn.heightForWidth(200) > 0


def test_command_link_button_size_hint(qapp):
    sh = Qlementine.CommandLinkButton("Title", "Desc").sizeHint()
    assert sh.width() > 0
    assert sh.height() > 0


# ============================================================
# ActionButton
# ============================================================


def test_action_button_create(qapp):
    assert Qlementine.ActionButton() is not None


def test_action_button_set_action(qapp):
    ab = Qlementine.ActionButton()
    action = QAction("Test Action")
    ab.setAction(action)
    ab.updateFromAction()
    assert ab.text() == "Test Action"


# ============================================================
# AboutDialog
# ============================================================


def test_about_dialog_create(qapp):
    assert Qlementine.AboutDialog() is not None


def test_about_dialog_setters_dont_crash(qapp):
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


def test_menu_create(qapp):
    assert Qlementine.Menu() is not None


def test_menu_update_methods_dont_crash(qapp):
    menu = Qlementine.Menu()
    menu.updateEnabled()
    menu.updateVisible()
    menu.updateProps()


# ============================================================
# SegmentedControl
# ============================================================


def test_segmented_control_create(qapp):
    assert Qlementine.SegmentedControl() is not None


def test_segmented_control_add_items(qapp):
    sc = Qlementine.SegmentedControl()
    assert sc.addItem("Tab 1") == 0
    assert sc.addItem("Tab 2") == 1
    assert sc.addItem("Tab 3") == 2
    assert sc.itemCount() == 3


def test_segmented_control_default_current_index(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A")
    sc.addItem("B")
    assert sc.currentIndex() == 0


def test_segmented_control_set_current_index(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A")
    sc.addItem("B")
    sc.setCurrentIndex(1)
    assert sc.currentIndex() == 1


def test_segmented_control_get_item_text(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("Hello")
    assert sc.getItemText(0) == "Hello"


def test_segmented_control_set_item_text(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("Old")
    sc.setItemText(0, "New")
    assert sc.getItemText(0) == "New"


def test_segmented_control_remove_item(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A")
    sc.addItem("B")
    sc.addItem("C")
    assert sc.itemCount() == 3
    sc.removeItem(1)
    assert sc.itemCount() == 2
    assert sc.getItemText(0) == "A"
    assert sc.getItemText(1) == "C"


def test_segmented_control_item_enabled(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A")
    assert sc.isItemEnabled(0) is True
    sc.setItemEnabled(0, False)
    assert sc.isItemEnabled(0) is False


def test_segmented_control_items_should_expand(qapp):
    sc = Qlementine.SegmentedControl()
    assert sc.itemsShouldExpand() is False
    sc.setItemsShouldExpand(True)
    assert sc.itemsShouldExpand() is True


def test_segmented_control_icon_size(qapp):
    sc = Qlementine.SegmentedControl()
    sc.setIconSize(QSize(24, 24))
    assert sc.iconSize() == QSize(24, 24)


def test_segmented_control_move_to_next(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A")
    sc.addItem("B")
    sc.addItem("C")
    sc.setCurrentIndex(0)
    sc.moveToNextItem()
    assert sc.currentIndex() == 1
    sc.moveToNextItem()
    assert sc.currentIndex() == 2


def test_segmented_control_move_to_previous(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A")
    sc.addItem("B")
    sc.addItem("C")
    sc.setCurrentIndex(2)
    sc.moveToPreviousItem()
    assert sc.currentIndex() == 1
    sc.moveToPreviousItem()
    assert sc.currentIndex() == 0


def test_segmented_control_set_current_data(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A", itemData="data_a")
    sc.addItem("B", itemData="data_b")
    sc.setCurrentData("data_b")
    assert sc.currentIndex() == 1


def test_segmented_control_find_item_index(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("A", itemData="alpha")
    sc.addItem("B", itemData="beta")
    assert sc.findItemIndex("alpha") == 0
    assert sc.findItemIndex("beta") == 1


def test_segmented_control_set_item_badge(qapp):
    sc = Qlementine.SegmentedControl()
    sc.addItem("Tab")
    sc.setItemBadge(0, "3")
    assert sc.getItemBadge(0) == "3"


# ============================================================
# NavigationBar
# ============================================================


def test_navigation_bar_create(qapp):
    assert Qlementine.NavigationBar() is not None


def test_navigation_bar_add_items(qapp):
    nb = Qlementine.NavigationBar()
    nb.addItem("Home")
    nb.addItem("Search")
    nb.addItem("Profile")
    assert nb.itemCount() == 3


def test_navigation_bar_set_current_index(qapp):
    nb = Qlementine.NavigationBar()
    nb.addItem("A")
    nb.addItem("B")
    nb.setCurrentIndex(1)
    assert nb.currentIndex() == 1


def test_navigation_bar_get_set_item_text(qapp):
    nb = Qlementine.NavigationBar()
    nb.addItem("Old")
    nb.setItemText(0, "New")
    assert nb.getItemText(0) == "New"


def test_navigation_bar_remove_item(qapp):
    nb = Qlementine.NavigationBar()
    nb.addItem("A")
    nb.addItem("B")
    nb.removeItem(0)
    assert nb.itemCount() == 1
    assert nb.getItemText(0) == "B"


def test_navigation_bar_item_data(qapp):
    nb = Qlementine.NavigationBar()
    nb.addItem("Home", itemData=42)
    assert nb.getItemData(0) == 42


def test_navigation_bar_move_navigation(qapp):
    nb = Qlementine.NavigationBar()
    nb.addItem("A")
    nb.addItem("B")
    nb.addItem("C")
    nb.setCurrentIndex(0)
    nb.moveToNextItem()
    assert nb.currentIndex() == 1
    nb.moveToPreviousItem()
    assert nb.currentIndex() == 0
