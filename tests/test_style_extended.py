"""Tests for extended QStyle methods and theme color accessors (b3d488f)."""

from __future__ import annotations

from _qt_compat import QColor, Qlementine, QSize

try:
    from PyQt6.QtCore import QModelIndex
    from PyQt6.QtGui import QFont, QIcon, QPainter, QPalette, QPixmap
except ImportError:
    from PySide6.QtCore import QModelIndex  # type: ignore
    from PySide6.QtGui import QFont, QIcon, QPainter, QPalette, QPixmap  # type: ignore

QlementineStyle = Qlementine.QlementineStyle
MouseState = Qlementine.MouseState
ColorRole = Qlementine.ColorRole
CheckState = Qlementine.CheckState
FocusState = Qlementine.FocusState
ActiveState = Qlementine.ActiveState
SelectionState = Qlementine.SelectionState
AlternateState = Qlementine.AlternateState
Status = Qlementine.Status
TextRole = Qlementine.TextRole
AutoIconColor = Qlementine.AutoIconColor


# ---- Extended enum members ----


def test_standard_pixmap_ext_members():
    sp = QlementineStyle.StandardPixmapExt
    assert sp.SP_Check is not None
    assert sp.SP_Calendar is not None
    assert sp.SP_Check != sp.SP_Calendar


def test_control_element_ext_members():
    ce = QlementineStyle.ControlElementExt
    assert ce.CE_CommandButtonLabel is not None
    assert ce.CE_CommandButton is not None
    assert ce.CE_CommandButtonLabel != ce.CE_CommandButton


def test_contents_type_ext_members():
    ct = QlementineStyle.ContentsTypeExt
    assert ct.CT_CommandButton is not None


def test_pixel_metric_ext_members():
    pm = QlementineStyle.PixelMetricExt
    assert pm.PM_MediumIconSize is not None


def test_primitive_element_ext_members():
    pe = QlementineStyle.PrimitiveElementExt
    assert pe.PE_CommandButtonPanel is not None
    assert pe.PE_CommandButtonLabel is not None
    assert pe.PE_CommandButtonPanel != pe.PE_CommandButtonLabel


# ---- Extended QStyle methods ----


def test_standard_icon_ext(qapp):
    style = QlementineStyle()
    icon = style.standardIconExt(QlementineStyle.StandardPixmapExt.SP_Check)
    assert isinstance(icon, QIcon)


def test_standard_icon_ext_calendar(qapp):
    style = QlementineStyle()
    icon = style.standardIconExt(QlementineStyle.StandardPixmapExt.SP_Calendar)
    assert isinstance(icon, QIcon)


def test_size_from_contents_ext(qapp):
    """sizeFromContentsExt returns a QSize; without a real QStyleOption it may
    return (-1, -1) which is valid 'no answer' sentinel."""
    style = QlementineStyle()
    size = style.sizeFromContentsExt(
        QlementineStyle.ContentsTypeExt.CT_CommandButton, None, QSize(100, 40)
    )
    assert isinstance(size, QSize)


def test_pixel_metric_ext(qapp):
    style = QlementineStyle()
    val = style.pixelMetricExt(QlementineStyle.PixelMetricExt.PM_MediumIconSize)
    assert isinstance(val, int)
    assert val > 0


def test_draw_primitive_ext_no_crash(qapp):
    """drawPrimitiveExt with a real painter should not crash."""
    style = QlementineStyle()
    pm = QPixmap(100, 40)
    pm.fill(QColor("white"))
    painter = QPainter(pm)
    try:
        style.drawPrimitiveExt(
            QlementineStyle.PrimitiveElementExt.PE_CommandButtonPanel,
            None,
            painter,
        )
    finally:
        painter.end()


def test_draw_control_ext_no_crash(qapp):
    """drawControlExt with a real painter should not crash."""
    style = QlementineStyle()
    pm = QPixmap(100, 40)
    pm.fill(QColor("white"))
    painter = QPainter(pm)
    try:
        style.drawControlExt(
            QlementineStyle.ControlElementExt.CE_CommandButton,
            None,
            painter,
        )
    finally:
        painter.end()


# ---- Theme color methods: basic / frame ----


def test_color(qapp):
    style = QlementineStyle()
    c = style.color(MouseState.Normal, ColorRole.Primary)
    assert isinstance(c, QColor)
    assert c.isValid()


def test_frame_background_color(qapp):
    style = QlementineStyle()
    c = style.frameBackgroundColor(MouseState.Normal)
    assert isinstance(c, QColor) and c.isValid()


# ---- Button colors ----


def test_button_background_color(qapp):
    style = QlementineStyle()
    c = style.buttonBackgroundColor(MouseState.Normal, ColorRole.Primary)
    assert isinstance(c, QColor) and c.isValid()


def test_button_foreground_color(qapp):
    style = QlementineStyle()
    c = style.buttonForegroundColor(MouseState.Normal, ColorRole.Primary)
    assert isinstance(c, QColor) and c.isValid()


def test_button_colors_vary_by_state(qapp):
    style = QlementineStyle()
    normal = style.buttonBackgroundColor(MouseState.Normal, ColorRole.Primary)
    disabled = style.buttonBackgroundColor(MouseState.Disabled, ColorRole.Primary)
    assert normal != disabled


# ---- Tool button colors ----


def test_tool_button_background_color(qapp):
    style = QlementineStyle()
    c = style.toolButtonBackgroundColor(MouseState.Normal, ColorRole.Secondary)
    assert isinstance(c, QColor)


def test_tool_button_foreground_color(qapp):
    style = QlementineStyle()
    c = style.toolButtonForegroundColor(MouseState.Normal, ColorRole.Secondary)
    assert isinstance(c, QColor)


def test_tool_button_separator_color(qapp):
    style = QlementineStyle()
    c = style.toolButtonSeparatorColor(MouseState.Normal, ColorRole.Secondary)
    assert isinstance(c, QColor)


# ---- Command button colors ----


def test_command_button_colors(qapp):
    style = QlementineStyle()
    for method in [
        "commandButtonBackgroundColor",
        "commandButtonTextColor",
        "commandButtonDescriptionColor",
        "commandButtonIconColor",
    ]:
        c = getattr(style, method)(MouseState.Normal, ColorRole.Primary)
        assert isinstance(c, QColor), f"{method} failed"


# ---- Check button colors ----


def test_check_button_background_color(qapp):
    style = QlementineStyle()
    c = style.checkButtonBackgroundColor(MouseState.Normal, CheckState.Checked)
    assert isinstance(c, QColor) and c.isValid()


def test_check_button_foreground_color(qapp):
    style = QlementineStyle()
    c = style.checkButtonForegroundColor(MouseState.Normal, CheckState.Checked)
    assert isinstance(c, QColor) and c.isValid()


def test_check_button_border_color(qapp):
    style = QlementineStyle()
    c = style.checkButtonBorderColor(
        MouseState.Normal, FocusState.NotFocused, CheckState.Checked
    )
    assert isinstance(c, QColor) and c.isValid()


# ---- Radio button colors ----


def test_radio_button_colors(qapp):
    style = QlementineStyle()
    assert style.radioButtonBackgroundColor(
        MouseState.Normal, CheckState.Checked
    ).isValid()
    assert style.radioButtonForegroundColor(
        MouseState.Normal, CheckState.Checked
    ).isValid()
    assert style.radioButtonBorderColor(
        MouseState.Normal, FocusState.NotFocused, CheckState.Checked
    ).isValid()


# ---- ComboBox colors ----


def test_combo_box_colors(qapp):
    style = QlementineStyle()
    assert style.comboBoxBackgroundColor(MouseState.Normal).isValid()
    assert style.comboBoxForegroundColor(MouseState.Normal).isValid()
    assert style.comboBoxTextColor(MouseState.Normal, Status.Default).isValid()


# ---- SpinBox colors ----


def test_spin_box_colors(qapp):
    style = QlementineStyle()
    assert style.spinBoxBackgroundColor(MouseState.Normal).isValid()
    assert style.spinBoxBorderColor(MouseState.Normal, FocusState.NotFocused).isValid()
    assert style.spinBoxButtonBackgroundColor(MouseState.Normal).isValid()
    assert style.spinBoxButtonForegroundColor(MouseState.Normal).isValid()


# ---- List item colors ----


def test_list_item_row_background_color(qapp):
    style = QlementineStyle()
    c = style.listItemRowBackgroundColor(MouseState.Normal, AlternateState.NotAlternate)
    assert isinstance(c, QColor)


def test_list_item_background_color(qapp):
    style = QlementineStyle()
    c = style.listItemBackgroundColor(
        MouseState.Normal,
        SelectionState.NotSelected,
        FocusState.NotFocused,
        ActiveState.Active,
        QModelIndex(),
    )
    assert isinstance(c, QColor)


def test_list_item_foreground_color(qapp):
    style = QlementineStyle()
    c = style.listItemForegroundColor(
        MouseState.Normal,
        SelectionState.NotSelected,
        FocusState.NotFocused,
        ActiveState.Active,
    )
    assert isinstance(c, QColor) and c.isValid()


def test_list_item_auto_icon_color(qapp):
    style = QlementineStyle()
    val = style.listItemAutoIconColor(
        MouseState.Normal,
        SelectionState.NotSelected,
        FocusState.NotFocused,
        ActiveState.Active,
        QModelIndex(),
    )
    assert isinstance(val, AutoIconColor)


def test_list_item_caption_foreground_color(qapp):
    style = QlementineStyle()
    c = style.listItemCaptionForegroundColor(
        MouseState.Normal,
        SelectionState.NotSelected,
        FocusState.NotFocused,
        ActiveState.Active,
    )
    assert isinstance(c, QColor)


def test_list_item_check_button_colors(qapp):
    style = QlementineStyle()
    args = (
        MouseState.Normal,
        CheckState.Checked,
        SelectionState.Selected,
        ActiveState.Active,
    )
    assert style.listItemCheckButtonBackgroundColor(*args).isValid()
    assert style.listItemCheckButtonBorderColor(*args).isValid()
    assert style.listItemCheckButtonForegroundColor(*args).isValid()


def test_cell_item_focus_border_color(qapp):
    style = QlementineStyle()
    c = style.cellItemFocusBorderColor(
        FocusState.Focused, SelectionState.Selected, ActiveState.Active
    )
    assert isinstance(c, QColor)


# ---- Menu colors ----


def test_menu_colors(qapp):
    style = QlementineStyle()
    assert style.menuBackgroundColor().isValid()
    assert style.menuBorderColor().isValid()
    assert style.menuSeparatorColor().isValid()


def test_menu_item_colors(qapp):
    style = QlementineStyle()
    assert style.menuItemBackgroundColor(MouseState.Normal).isValid()
    assert style.menuItemForegroundColor(MouseState.Normal).isValid()
    assert style.menuItemSecondaryForegroundColor(MouseState.Normal).isValid()


def test_menu_bar_colors(qapp):
    style = QlementineStyle()
    assert style.menuBarBackgroundColor().isValid()
    assert style.menuBarBorderColor().isValid()
    assert style.menuBarItemBackgroundColor(
        MouseState.Normal, SelectionState.NotSelected
    ).isValid()
    assert style.menuBarItemForegroundColor(
        MouseState.Normal, SelectionState.NotSelected
    ).isValid()


# ---- Tab colors ----


def test_tab_bar_colors(qapp):
    style = QlementineStyle()
    assert style.tabBarBackgroundColor(MouseState.Normal).isValid()
    assert style.tabBarShadowColor().isValid()
    assert style.tabBarBottomShadowColor().isValid()
    assert style.tabBarScrollButtonBackgroundColor(MouseState.Normal).isValid()


def test_tab_colors(qapp):
    style = QlementineStyle()
    assert style.tabBackgroundColor(
        MouseState.Normal, SelectionState.Selected
    ).isValid()
    assert style.tabForegroundColor(
        MouseState.Normal, SelectionState.Selected
    ).isValid()


def test_tab_close_button_colors(qapp):
    style = QlementineStyle()
    assert style.tabCloseButtonBackgroundColor(
        MouseState.Normal, SelectionState.Selected
    ).isValid()
    assert style.tabCloseButtonForegroundColor(
        MouseState.Normal, SelectionState.Selected
    ).isValid()


# ---- Progress bar colors ----


def test_progress_bar_colors(qapp):
    style = QlementineStyle()
    assert style.progressBarGrooveColor(MouseState.Normal).isValid()
    assert style.progressBarValueColor(MouseState.Normal).isValid()


# ---- Text field colors ----


def test_text_field_colors(qapp):
    style = QlementineStyle()
    assert style.textFieldBackgroundColor(MouseState.Normal, Status.Default).isValid()
    assert style.textFieldBorderColor(
        MouseState.Normal, FocusState.NotFocused, Status.Default
    ).isValid()
    assert style.textFieldForegroundColor(MouseState.Normal).isValid()


# ---- Slider colors ----


def test_slider_colors(qapp):
    style = QlementineStyle()
    assert style.sliderGrooveColor(MouseState.Normal).isValid()
    assert style.sliderValueColor(MouseState.Normal).isValid()
    assert style.sliderHandleColor(MouseState.Normal).isValid()
    assert style.sliderTickColor(MouseState.Normal).isValid()


# ---- Dial colors ----


def test_dial_colors(qapp):
    style = QlementineStyle()
    assert style.dialHandleColor(MouseState.Normal).isValid()
    assert style.dialGrooveColor(MouseState.Normal).isValid()
    assert style.dialValueColor(MouseState.Normal).isValid()
    assert style.dialTickColor(MouseState.Normal).isValid()
    assert style.dialMarkColor(MouseState.Normal).isValid()
    assert style.dialBackgroundColor(MouseState.Normal).isValid()


# ---- Label colors ----


def test_label_colors(qapp):
    style = QlementineStyle()
    assert style.labelForegroundColor(MouseState.Normal).isValid()
    assert style.labelCaptionForegroundColor(MouseState.Normal).isValid()


# ---- Icon foreground color ----


def test_icon_foreground_color(qapp):
    style = QlementineStyle()
    c = style.iconForegroundColor(MouseState.Normal, ColorRole.Primary)
    assert isinstance(c, QColor) and c.isValid()


# ---- Toolbar colors ----


def test_tool_bar_colors(qapp):
    style = QlementineStyle()
    assert style.toolBarBackgroundColor().isValid()
    assert style.toolBarBorderColor().isValid()
    assert style.toolBarSeparatorColor().isValid()


# ---- Tooltip colors ----


def test_tool_tip_colors(qapp):
    style = QlementineStyle()
    assert style.toolTipBackgroundColor().isValid()
    assert style.toolTipBorderColor().isValid()
    assert style.toolTipForegroundColor().isValid()


# ---- Scrollbar ----


def test_scroll_bar_colors(qapp):
    style = QlementineStyle()
    assert style.scrollBarGrooveColor(MouseState.Normal).isValid()
    assert style.scrollBarHandleColor(MouseState.Normal).isValid()


def test_scroll_bar_thickness(qapp):
    style = QlementineStyle()
    t = style.getScrollBarThickness(MouseState.Normal)
    assert isinstance(t, int) and t > 0


# ---- GroupBox colors ----


def test_group_box_colors(qapp):
    style = QlementineStyle()
    assert style.groupBoxTitleColor(MouseState.Normal).isValid()
    assert style.groupBoxBorderColor(MouseState.Normal).isValid()
    assert style.groupBoxBackgroundColor(MouseState.Normal).isValid()


# ---- Status colors ----


def test_status_color(qapp):
    style = QlementineStyle()
    for s in [
        Status.Default,
        Status.Info,
        Status.Success,
        Status.Warning,
        Status.Error,
    ]:
        assert style.statusColor(s, MouseState.Normal).isValid()
        assert style.statusColorForeground(s, MouseState.Normal).isValid()


def test_focus_border_color(qapp):
    style = QlementineStyle()
    c = style.focusBorderColor(Status.Default)
    assert isinstance(c, QColor) and c.isValid()


def test_frame_border_color(qapp):
    style = QlementineStyle()
    assert style.frameBorderColor().isValid()


def test_separator_color(qapp):
    style = QlementineStyle()
    assert style.separatorColor().isValid()


# ---- Text role utilities ----


def test_color_for_text_role(qapp):
    style = QlementineStyle()
    for role in [
        TextRole.Caption,
        TextRole.Default,
        TextRole.H1,
        TextRole.H2,
        TextRole.H3,
        TextRole.H4,
        TextRole.H5,
    ]:
        c = style.colorForTextRole(role, MouseState.Normal)
        assert isinstance(c, QColor) and c.isValid()


def test_pixel_size_for_text_role(qapp):
    style = QlementineStyle()
    for role in [TextRole.Caption, TextRole.Default, TextRole.H1]:
        size = style.pixelSizeForTextRole(role)
        assert isinstance(size, int) and size > 0


def test_font_for_text_role(qapp):
    style = QlementineStyle()
    f = style.fontForTextRole(TextRole.Default)
    assert isinstance(f, QFont)


def test_palette_for_text_role(qapp):
    style = QlementineStyle()
    p = style.paletteForTextRole(TextRole.Default)
    assert isinstance(p, QPalette)


def test_text_role_sizes_hierarchy(qapp):
    """Heading sizes should be larger than default."""
    style = QlementineStyle()
    default = style.pixelSizeForTextRole(TextRole.Default)
    h1 = style.pixelSizeForTextRole(TextRole.H1)
    assert h1 >= default


# ---- Switch colors ----


def test_switch_colors(qapp):
    style = QlementineStyle()
    assert style.switchGrooveColor(MouseState.Normal, CheckState.Checked).isValid()
    assert style.switchGrooveBorderColor(
        MouseState.Normal, FocusState.NotFocused, CheckState.Checked
    ).isValid()
    assert style.switchHandleColor(MouseState.Normal, CheckState.Checked).isValid()


# ---- Table colors ----


def test_table_colors(qapp):
    style = QlementineStyle()
    assert style.tableHeaderBgColor(MouseState.Normal, CheckState.NotChecked).isValid()
    assert style.tableHeaderFgColor(MouseState.Normal, CheckState.NotChecked).isValid()
    assert style.tableLineColor().isValid()


# ---- Status bar colors ----


def test_status_bar_colors(qapp):
    style = QlementineStyle()
    assert style.statusBarBackgroundColor().isValid()
    assert style.statusBarBorderColor().isValid()
    assert style.statusBarSeparatorColor().isValid()


# ---- Splitter color ----


def test_splitter_color(qapp):
    style = QlementineStyle()
    assert style.splitterColor(MouseState.Normal).isValid()
