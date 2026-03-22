"""Theme tester and editor for Qlementine themes."""

from __future__ import annotations

import sys

from PySide6.QtCore import QJsonDocument, QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDockWidget,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PySide6Qlementine import (
    AutoIconColor,
    ColorEditor,
    ColorMode,
    CommandLinkButton,
    Label,
    LineEdit,
    QlementineStyle,
    Status,
    StatusBadge,
    StatusBadgeWidget,
    Switch,
    TextRole,
    Theme,
)

# ---------------------------------------------------------------------------
# Color / geometry data definitions
# ---------------------------------------------------------------------------

# Stateful color groups: (section_label, base_attr, has_transparent)
# Pattern: base, baseHovered, basePressed, baseDisabled[, baseTransparent]
_STATEFUL_COLORS: list[tuple[str, str, bool]] = [
    ("Neutral", "neutralColor", True),
    ("Primary", "primaryColor", True),
    ("Primary Foreground", "primaryColorForeground", True),
    ("Primary Alternative", "primaryAlternativeColor", True),
    ("Secondary", "secondaryColor", True),
    ("Secondary Foreground", "secondaryColorForeground", True),
    ("Secondary Alternative", "secondaryAlternativeColor", True),
    ("Border", "borderColor", True),
]

# Status color groups: (section_label, base_attr)
# Pattern: base, baseHovered, basePressed, baseDisabled (no Transparent)
_STATUS_COLORS: list[tuple[str, str]] = [
    ("Status Success", "statusColorSuccess"),
    ("Status Info", "statusColorInfo"),
    ("Status Warning", "statusColorWarning"),
    ("Status Error", "statusColorError"),
    ("Status Foreground", "statusColorForeground"),
]

# Standalone colors (Active tab only): (section_label, [(attr, label), ...])
_STANDALONE_COLORS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "Background",
        [
            ("backgroundColorMain1", "Main 1"),
            ("backgroundColorMain2", "Main 2"),
            ("backgroundColorMain3", "Main 3"),
            ("backgroundColorMain4", "Main 4"),
            ("backgroundColorMainTransparent", "Main Transparent"),
            ("backgroundColorWorkspace", "Workspace"),
            ("backgroundColorTabBar", "Tab Bar"),
        ],
    ),
    ("Focus", [("focusColor", "Focus")]),
    (
        "Shadow",
        [
            ("shadowColor1", "Shadow 1"),
            ("shadowColor2", "Shadow 2"),
            ("shadowColor3", "Shadow 3"),
            ("shadowColorTransparent", "Shadow Transparent"),
        ],
    ),
    (
        "Semi-transparent",
        [
            ("semiTransparentColor1", "Level 1"),
            ("semiTransparentColor2", "Level 2"),
            ("semiTransparentColor3", "Level 3"),
            ("semiTransparentColor4", "Level 4"),
            ("semiTransparentColorTransparent", "Transparent"),
        ],
    ),
]

# Geometry properties: (section, [(attr, label, type, min, max), ...])
_GEOMETRY_PROPS: list[tuple[str, list[tuple[str, str, str, int, int]]]] = [
    (
        "Border & Radius",
        [
            ("borderRadius", "Border Radius", "float", 0, 30),
            ("checkBoxBorderRadius", "Checkbox Radius", "float", 0, 20),
            ("menuItemBorderRadius", "Menu Item Radius", "float", 0, 20),
            ("menuBarItemBorderRadius", "MenuBar Item Radius", "float", 0, 20),
            ("borderWidth", "Border Width", "int", 0, 10),
            ("focusBorderWidth", "Focus Border Width", "int", 0, 10),
        ],
    ),
    (
        "Control Sizes",
        [
            ("controlHeightLarge", "Height Large", "int", 8, 64),
            ("controlHeightMedium", "Height Medium", "int", 8, 64),
            ("controlHeightSmall", "Height Small", "int", 4, 32),
            ("controlDefaultWidth", "Default Width", "int", 32, 256),
        ],
    ),
    (
        "Spacing",
        [
            ("spacing", "Spacing", "int", 0, 32),
            ("scrollBarMargin", "Scrollbar Margin", "int", 0, 16),
        ],
    ),
    (
        "Slider",
        [
            ("sliderTickSize", "Tick Size", "int", 0, 16),
            ("sliderTickSpacing", "Tick Spacing", "int", 0, 16),
            ("sliderTickThickness", "Tick Thickness", "int", 0, 8),
            ("sliderGrooveHeight", "Groove Height", "int", 1, 16),
        ],
    ),
    (
        "Dial",
        [
            ("dialMarkLength", "Mark Length", "int", 0, 20),
            ("dialMarkThickness", "Mark Thickness", "int", 0, 10),
            ("dialTickLength", "Tick Length", "int", 0, 16),
            ("dialTickSpacing", "Tick Spacing", "int", 0, 16),
            ("dialGrooveThickness", "Groove Thickness", "int", 1, 16),
        ],
    ),
    ("Progress Bar", [("progressBarGrooveHeight", "Groove Height", "int", 1, 16)]),
    (
        "Scroll Bar",
        [
            ("scrollBarThicknessFull", "Thickness Full", "int", 4, 32),
            ("scrollBarThicknessSmall", "Thickness Small", "int", 2, 16),
        ],
    ),
    (
        "Tab Bar",
        [
            ("tabBarPaddingTop", "Padding Top", "int", 0, 20),
            ("tabBarTabMaxWidth", "Tab Max Width", "int", 0, 500),
            ("tabBarTabMinWidth", "Tab Min Width", "int", 0, 200),
        ],
    ),
    (
        "Icon Sizes",
        [
            ("iconSize", "Default", "size", 4, 64),
            ("iconSizeMedium", "Medium", "size", 4, 64),
            ("iconSizeLarge", "Large", "size", 4, 64),
            ("iconSizeExtraSmall", "Extra Small", "size", 4, 64),
        ],
    ),
    (
        "Animation",
        [
            ("animationDuration", "Duration (ms)", "int", 0, 1000),
            ("focusAnimationDuration", "Focus (ms)", "int", 0, 1000),
            ("sliderAnimationDuration", "Slider (ms)", "int", 0, 1000),
        ],
    ),
]


# ---------------------------------------------------------------------------
# ThemeTester
# ---------------------------------------------------------------------------


class ThemeTester(QWidget):
    """Minimal set of QWidgets that exercises every theme color."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        tabs = QTabWidget()
        tabs.setTabsClosable(True)
        tabs.setMovable(True)
        layout.addWidget(tabs)

        tabs.addTab(self._build_controls_tab(), "Controls")
        tabs.addTab(self._build_data_tab(), "Data Views")

    # -- Controls tab -------------------------------------------------------

    def _build_controls_tab(self) -> QWidget:
        page = QScrollArea()
        page.setWidgetResizable(True)
        widget = QWidget()
        columns = QHBoxLayout(widget)
        left = QVBoxLayout()
        right = QVBoxLayout()
        columns.addLayout(left, 1)
        columns.addLayout(right, 1)

        left.addWidget(self._build_buttons())
        left.addWidget(self._build_inputs())
        left.addStretch()

        right.addWidget(self._build_toggles())
        right.addWidget(self._build_range())
        right.addWidget(self._build_status())
        right.addWidget(self._build_labels())
        right.addWidget(self._build_group_boxes())
        right.addStretch()

        page.setWidget(widget)
        return page

    def _build_buttons(self) -> QGroupBox:
        box = QGroupBox("Buttons")
        lay = QVBoxLayout(box)

        row1 = QHBoxLayout()
        primary = QPushButton("Primary")
        primary.setDefault(True)
        row1.addWidget(primary)
        dis = QPushButton("Primary Disabled")
        dis.setDefault(True)
        dis.setEnabled(False)
        row1.addWidget(dis)
        lay.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QPushButton("Secondary"))
        sec_dis = QPushButton("Sec. Disabled")
        sec_dis.setEnabled(False)
        row2.addWidget(sec_dis)
        lay.addLayout(row2)

        row3 = QHBoxLayout()
        flat = QPushButton("Flat")
        flat.setFlat(True)
        row3.addWidget(flat)
        menu_btn = QPushButton("With Menu")
        menu = QMenu(menu_btn)
        menu.addAction(QAction("Action 1", menu))
        menu.addAction(QAction("Action 2", menu))
        menu.addSeparator()
        menu.addAction(QAction("Action 3", menu))
        menu_btn.setMenu(menu)
        row3.addWidget(menu_btn)
        lay.addLayout(row3)

        row4 = QHBoxLayout()
        cmd = CommandLinkButton(box)
        cmd.setText("Command Link")
        cmd.setDescription("Description text underneath")
        row4.addWidget(cmd)
        cmd_dis = CommandLinkButton(box)
        cmd_dis.setText("Disabled")
        cmd_dis.setDescription("Disabled description")
        cmd_dis.setEnabled(False)
        row4.addWidget(cmd_dis)
        lay.addLayout(row4)

        return box

    def _build_toggles(self) -> QGroupBox:
        box = QGroupBox("Toggles")
        lay = QVBoxLayout(box)

        row1 = QHBoxLayout()
        cb_on = QCheckBox("Checked")
        cb_on.setChecked(True)
        row1.addWidget(cb_on)
        row1.addWidget(QCheckBox("Unchecked"))
        cb_dis = QCheckBox("Disabled")
        cb_dis.setChecked(True)
        cb_dis.setEnabled(False)
        row1.addWidget(cb_dis)
        lay.addLayout(row1)

        row2 = QHBoxLayout()
        rb1 = QRadioButton("Selected")
        rb1.setChecked(True)
        row2.addWidget(rb1)
        row2.addWidget(QRadioButton("Unselected"))
        rb_dis = QRadioButton("Disabled")
        rb_dis.setEnabled(False)
        row2.addWidget(rb_dis)
        lay.addLayout(row2)

        row3 = QHBoxLayout()
        sw_on = Switch(box)
        sw_on.setText("On")
        sw_on.setChecked(True)
        row3.addWidget(sw_on)
        sw_off = Switch(box)
        sw_off.setText("Off")
        row3.addWidget(sw_off)
        sw_dis = Switch(box)
        sw_dis.setText("Disabled")
        sw_dis.setChecked(True)
        sw_dis.setEnabled(False)
        row3.addWidget(sw_dis)
        lay.addLayout(row3)

        return box

    def _build_inputs(self) -> QGroupBox:
        box = QGroupBox("Inputs")
        lay = QVBoxLayout(box)

        le = LineEdit(box)
        le.setPlaceholderText("Normal input")
        le.setClearButtonEnabled(True)
        lay.addWidget(le)

        for status, text in [
            (Status.Error, "Error status"),
            (Status.Warning, "Warning status"),
            (Status.Success, "Success status"),
        ]:
            sle = LineEdit(box)
            sle.setPlaceholderText(text)
            sle.setStatus(status)
            lay.addWidget(sle)

        le_dis = LineEdit(box)
        le_dis.setPlaceholderText("Disabled input")
        le_dis.setEnabled(False)
        lay.addWidget(le_dis)

        row = QHBoxLayout()
        spin = QSpinBox(box)
        spin.setRange(0, 100)
        spin.setValue(42)
        row.addWidget(spin)
        spin_dis = QSpinBox(box)
        spin_dis.setEnabled(False)
        row.addWidget(spin_dis)
        lay.addLayout(row)

        row2 = QHBoxLayout()
        combo = QComboBox(box)
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        row2.addWidget(combo)
        combo_dis = QComboBox(box)
        combo_dis.addItems(["Disabled"])
        combo_dis.setEnabled(False)
        row2.addWidget(combo_dis)
        lay.addLayout(row2)

        return box

    def _build_range(self) -> QGroupBox:
        box = QGroupBox("Range")
        lay = QVBoxLayout(box)

        slider = QSlider(Qt.Orientation.Horizontal, box)
        slider.setRange(0, 100)
        slider.setValue(40)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(10)
        lay.addWidget(slider)

        slider_dis = QSlider(Qt.Orientation.Horizontal, box)
        slider_dis.setRange(0, 100)
        slider_dis.setValue(40)
        slider_dis.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider_dis.setTickInterval(10)
        slider_dis.setEnabled(False)
        lay.addWidget(slider_dis)

        progress = QProgressBar(box)
        progress.setRange(0, 100)
        progress.setValue(60)
        lay.addWidget(progress)

        prog_dis = QProgressBar(box)
        prog_dis.setRange(0, 100)
        prog_dis.setValue(60)
        prog_dis.setEnabled(False)
        lay.addWidget(prog_dis)

        dial_row = QHBoxLayout()
        dial = QDial(box)
        dial.setRange(0, 100)
        dial.setValue(50)
        dial.setNotchesVisible(True)
        dial.setFixedSize(64, 64)
        dial_row.addWidget(dial)
        dial_dis = QDial(box)
        dial_dis.setRange(0, 100)
        dial_dis.setValue(50)
        dial_dis.setNotchesVisible(True)
        dial_dis.setFixedSize(64, 64)
        dial_dis.setEnabled(False)
        dial_row.addWidget(dial_dis)
        dial_row.addStretch()
        lay.addLayout(dial_row)

        return box

    def _build_status(self) -> QGroupBox:
        box = QGroupBox("Status Badges")
        lay = QHBoxLayout(box)
        for badge in (
            StatusBadge.Success,
            StatusBadge.Info,
            StatusBadge.Warning,
            StatusBadge.Error,
        ):
            w = StatusBadgeWidget(badge, box)
            lay.addWidget(w)
            lay.addWidget(QLabel(badge.name))
        lay.addStretch()
        return box

    def _build_labels(self) -> QGroupBox:
        box = QGroupBox("Labels")
        grid = QHBoxLayout(box)

        left = QVBoxLayout()
        lbl = Label(box)
        lbl.setText("Normal label")
        left.addWidget(lbl)
        cap = Label(box)
        cap.setText("Caption text")
        cap.setRole(TextRole.Caption)
        left.addWidget(cap)

        right = QVBoxLayout()
        lbl_dis = Label(box)
        lbl_dis.setText("Disabled label")
        lbl_dis.setEnabled(False)
        right.addWidget(lbl_dis)
        cap_dis = Label(box)
        cap_dis.setText("Disabled caption")
        cap_dis.setRole(TextRole.Caption)
        cap_dis.setEnabled(False)
        right.addWidget(cap_dis)

        grid.addLayout(left)
        grid.addLayout(right)
        grid.addStretch()
        return box

    def _build_group_boxes(self) -> QWidget:
        outer = QWidget()
        lay = QHBoxLayout(outer)
        lay.setContentsMargins(0, 0, 0, 0)

        active = QGroupBox("Active GroupBox")
        al = QVBoxLayout(active)
        al.addWidget(QLabel("Content inside"))
        lay.addWidget(active)

        disabled = QGroupBox("Disabled GroupBox")
        dl = QVBoxLayout(disabled)
        dl.addWidget(QLabel("Content inside"))
        disabled.setEnabled(False)
        lay.addWidget(disabled)

        return outer

    # -- Data Views tab -----------------------------------------------------

    def _build_data_tab(self) -> QWidget:
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # List with checkable items  →  primaryAlternativeColor, scrollbar colors
        list_w = QListWidget()
        list_w.setAlternatingRowColors(True)
        for i in range(20):
            item = QListWidgetItem(f"Item {i + 1}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if i % 3 == 0 else Qt.CheckState.Unchecked
            )
            list_w.addItem(item)
        list_w.setCurrentRow(0)
        splitter.addWidget(list_w)

        # Table  →  header bg/fg, grid lines
        table = QTableWidget(8, 3)
        table.setHorizontalHeaderLabels(["Name", "Value", "Type"])
        for r in range(8):
            for c in range(3):
                table.setItem(r, c, QTableWidgetItem(f"Cell {r},{c}"))
        table.horizontalHeader().setStretchLastSection(True)
        splitter.addWidget(table)

        return splitter


# ---------------------------------------------------------------------------
# ThemeEditor
# ---------------------------------------------------------------------------


class ThemeEditor(QWidget):
    """Editor for all theme color and geometry properties."""

    def __init__(self, style: QlementineStyle, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._style = style
        self._editors: dict[str, ColorEditor | QSpinBox | QDoubleSpinBox | tuple] = {}
        self._updating = False

        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        layout.addWidget(tabs)
        tabs.addTab(self._build_color_tab("Active"), "Active")
        tabs.addTab(self._build_color_tab("Hovered"), "Hovered")
        tabs.addTab(self._build_color_tab("Pressed"), "Pressed")
        tabs.addTab(self._build_color_tab("Disabled"), "Disabled")
        tabs.addTab(self._build_geometry_tab(), "Geometry")

        dump_btn = QPushButton("Dump JSON to stdout")
        dump_btn.clicked.connect(self._dump_json)
        layout.addWidget(dump_btn)

    # -- color tabs ---------------------------------------------------------

    def _build_color_tab(self, state: str) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        lay = QVBoxLayout(content)

        colors = self._colors_for_state(state)
        theme = self._style.theme()
        current_section: str | None = None
        form: QFormLayout | None = None

        for section, attr, label in colors:
            if section != current_section:
                box = QGroupBox(section)
                form = QFormLayout(box)
                lay.addWidget(box)
                current_section = section

            color = getattr(theme, attr)
            editor = ColorEditor(color, content)
            # ColorEditor locks its internal LineEdit to
            # setFixedWidth(minimumSizeHint().width()) at construction,
            # before the style polishes it (12px instead of ~119px).
            # Fix by resetting to the post-polish sizeHint.
            for le in editor.findChildren(LineEdit):
                le.setFixedWidth(le.sizeHint().width())
            if color.alpha() < 255:
                editor.setColorMode(ColorMode.RGBA)
            editor.colorChanged.connect(
                lambda *, a=attr, e=editor: self._on_color_changed(a, e)
            )
            self._editors[attr] = editor
            assert form is not None
            form.addRow(label, editor)

        lay.addStretch()
        scroll.setWidget(content)
        return scroll

    @staticmethod
    def _colors_for_state(
        state: str,
    ) -> list[tuple[str, str, str]]:
        """Return (section, attr_name, label) triples for *state* tab."""
        result: list[tuple[str, str, str]] = []

        if state == "Active":
            # Standalone colors
            for section, attrs in _STANDALONE_COLORS:
                for attr, label in attrs:
                    result.append((section, attr, label))
            # Stateful groups: normal + transparent
            for section, base, has_trans in _STATEFUL_COLORS:
                result.append((section, base, "Normal"))
                if has_trans:
                    result.append((section, f"{base}Transparent", "Transparent"))
            # Status groups: normal only
            for section, base in _STATUS_COLORS:
                result.append((section, base, "Normal"))
        else:
            suffix = state  # "Hovered", "Pressed", or "Disabled"
            for section, base, _ in _STATEFUL_COLORS:
                result.append((section, f"{base}{suffix}", suffix))
            for section, base in _STATUS_COLORS:
                result.append((section, f"{base}{suffix}", suffix))

        return result

    def _on_color_changed(self, attr: str, editor: ColorEditor) -> None:
        if self._updating:
            return
        self._updating = True
        try:
            theme = Theme(self._style.theme())
            setattr(theme, attr, editor.color())
            self._style.setTheme(theme)
        finally:
            self._updating = False

    # -- geometry tab -------------------------------------------------------

    def _build_geometry_tab(self) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        lay = QVBoxLayout(content)
        theme = self._style.theme()

        for section, props in _GEOMETRY_PROPS:
            box = QGroupBox(section)
            form = QFormLayout(box)
            lay.addWidget(box)

            for attr, label, ptype, pmin, pmax in props:
                if ptype == "float":
                    editor = QDoubleSpinBox(content)
                    editor.setRange(pmin, pmax)
                    editor.setSingleStep(0.5)
                    editor.setValue(getattr(theme, attr))
                    editor.valueChanged.connect(
                        lambda v, a=attr: self._on_geom_changed(a, v)
                    )
                    self._editors[attr] = editor
                    form.addRow(label, editor)

                elif ptype == "int":
                    editor = QSpinBox(content)
                    editor.setRange(pmin, pmax)
                    editor.setValue(getattr(theme, attr))
                    editor.valueChanged.connect(
                        lambda v, a=attr: self._on_geom_changed(a, v)
                    )
                    self._editors[attr] = editor
                    form.addRow(label, editor)

                elif ptype == "size":
                    size_val: QSize = getattr(theme, attr)
                    w_spin = QSpinBox(content)
                    w_spin.setRange(pmin, pmax)
                    w_spin.setValue(size_val.width())
                    w_spin.setPrefix("W:")
                    h_spin = QSpinBox(content)
                    h_spin.setRange(pmin, pmax)
                    h_spin.setValue(size_val.height())
                    h_spin.setPrefix("H:")

                    def _on_size(_, a=attr, ws=w_spin, hs=h_spin):
                        self._on_geom_changed(a, QSize(ws.value(), hs.value()))

                    w_spin.valueChanged.connect(_on_size)
                    h_spin.valueChanged.connect(_on_size)
                    self._editors[attr] = (w_spin, h_spin)

                    row_w = QWidget(content)
                    row_lay = QHBoxLayout(row_w)
                    row_lay.setContentsMargins(0, 0, 0, 0)
                    row_lay.addWidget(w_spin)
                    row_lay.addWidget(h_spin)
                    form.addRow(label, row_w)

        lay.addStretch()
        scroll.setWidget(content)
        return scroll

    def _on_geom_changed(self, attr: str, value: object) -> None:
        if self._updating:
            return
        self._updating = True
        try:
            theme = Theme(self._style.theme())
            setattr(theme, attr, value)
            self._style.setTheme(theme)
        finally:
            self._updating = False

    # -- refresh / dump -----------------------------------------------------

    def _refresh_all(self) -> None:
        if self._updating:
            return
        self._updating = True
        try:
            theme = self._style.theme()
            for attr, editor in self._editors.items():
                if isinstance(editor, ColorEditor):
                    editor.setColor(getattr(theme, attr))
                elif isinstance(editor, QDoubleSpinBox):
                    editor.setValue(getattr(theme, attr))
                elif isinstance(editor, QSpinBox):
                    editor.setValue(getattr(theme, attr))
                elif isinstance(editor, tuple):
                    size_val: QSize = getattr(theme, attr)
                    editor[0].setValue(size_val.width())
                    editor[1].setValue(size_val.height())
        finally:
            self._updating = False

    def _dump_json(self) -> None:
        doc = self._style.theme().toJson()
        print(bytes(doc.toJson(QJsonDocument.JsonFormat.Indented)).decode())


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------


class ThemeToolsWindow(QMainWindow):
    """Main window with ThemeTester as central widget and ThemeEditor in dock."""

    def __init__(self, style: QlementineStyle) -> None:
        super().__init__()
        self.setWindowTitle("Qlementine Theme Tools")

        # Menu bar
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(QAction("Open", self))
        file_menu.addAction(QAction("Save", self))
        file_menu.addSeparator()
        quit_act = QAction("Quit", self)
        quit_act.triggered.connect(self.close)
        file_menu.addAction(quit_act)

        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(QAction("Undo", self))
        edit_menu.addAction(QAction("Redo", self))

        # Tool bar
        toolbar = QToolBar("Main", self)
        toolbar.addAction(QAction("New", self))
        toolbar.addAction(QAction("Open", self))
        toolbar.addSeparator()
        toolbar.addAction(QAction("Save", self))
        self.addToolBar(toolbar)

        # Status bar with tooltip
        tip_label = QLabel("Hover here for tooltip")
        tip_label.setToolTip("This is a tooltip \u2014 demonstrates tooltip colors")
        self.statusBar().addWidget(tip_label)

        # Central widget
        self.setCentralWidget(ThemeTester(self))

        # Dock: ThemeEditor
        dock = QDockWidget("Theme Editor", self)
        dock.setWidget(ThemeEditor(style, dock))
        dock.setMinimumWidth(380)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        self.resize(1250, 850)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Qlementine Theme Tools")

    style = QlementineStyle(app)
    style.setAutoIconColor(AutoIconColor.TextColor)
    style.setAnimationsEnabled(True)
    app.setStyle(style)

    window = ThemeToolsWindow(style)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
