"""Demo showcasing Qlementine-styled Qt widgets."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt6Qlementine import (
    ActionButton,
    AutoIconColor,
    ColorButton,
    ColorEditor,
    CommandLinkButton,
    Expander,
    Label,
    LineEdit,
    LoadingSpinner,
    NotificationBadge,
    PlainTextEdit,
    QlementineStyle,
    StatusBadgeWidget,
    Switch,
    TextRole,
)


def _make_section(title: str, parent: QWidget | None = None) -> QGroupBox:
    """Create a titled group box with a vertical layout."""
    group = QGroupBox(title, parent)
    group.setLayout(QVBoxLayout())
    return group


def _setup_labels(parent: QVBoxLayout) -> None:
    roles = [
        ("Headline 1", TextRole.H1),
        ("Headline 2", TextRole.H2),
        ("Headline 3", TextRole.H3),
        ("Headline 4", TextRole.H4),
        ("Headline 5", TextRole.H5),
        ("Default body text", TextRole.Default),
        ("Caption text", TextRole.Caption),
    ]
    section = _make_section("Labels")
    for text, role in roles:
        label = Label()
        label.setText(text)
        label.setRole(role)
        section.layout().addWidget(label)
    parent.addWidget(section)


def _setup_buttons(parent: QVBoxLayout) -> None:
    section = _make_section("Buttons")
    layout = section.layout()

    row = QHBoxLayout()
    btn = QPushButton("Default Button")
    btn.setDefault(True)
    row.addWidget(btn)

    btn_flat = QPushButton("Flat Button")
    btn_flat.setFlat(True)
    row.addWidget(btn_flat)

    btn_menu = QPushButton("With Menu")
    menu = QMenu(btn_menu)
    for i in range(3):
        menu.addAction(QAction(f"Action {i + 1}", menu))
    btn_menu.setMenu(menu)
    row.addWidget(btn_menu)
    layout.addLayout(row)

    row2 = QHBoxLayout()
    action_btn = ActionButton()
    action_btn.setText("Action Button")
    row2.addWidget(action_btn)

    cmd_btn = CommandLinkButton()
    cmd_btn.setText("Command Link")
    cmd_btn.setDescription("With a description line underneath")
    row2.addWidget(cmd_btn)
    layout.addLayout(row2)

    parent.addWidget(section)


def _setup_inputs(parent: QVBoxLayout) -> None:
    section = _make_section("Input Widgets")
    layout = section.layout()

    line_edit = LineEdit()
    line_edit.setPlaceholderText("Type something here...")
    line_edit.setClearButtonEnabled(True)
    layout.addWidget(line_edit)

    plain_text = PlainTextEdit()
    plain_text.setPlaceholderText("Multi-line text editor")
    plain_text.setFixedHeight(80)
    layout.addWidget(plain_text)

    row = QHBoxLayout()
    spin = QSpinBox()
    spin.setRange(0, 100)
    spin.setValue(42)
    spin.setSuffix(" units")
    row.addWidget(spin)

    combo = QComboBox()
    combo.setEditable(True)
    for i in range(5):
        combo.addItem(f"Option {i + 1}")
    row.addWidget(combo)
    layout.addLayout(row)

    parent.addWidget(section)


def _setup_toggles(parent: QVBoxLayout) -> None:
    section = _make_section("Toggles & Checks")
    layout = section.layout()

    row = QHBoxLayout()
    switch = Switch()
    switch.setText("Switch toggle")
    switch.setChecked(True)
    row.addWidget(switch)

    switch_tri = Switch()
    switch_tri.setText("Tristate switch")
    switch_tri.setTristate(True)
    switch_tri.setCheckState(Qt.CheckState.PartiallyChecked)
    row.addWidget(switch_tri)
    layout.addLayout(row)

    row2 = QHBoxLayout()
    for i, label in enumerate(["Check A", "Check B", "Check C"]):
        cb = QCheckBox(label)
        cb.setChecked(i % 2 == 0)
        row2.addWidget(cb)
    layout.addLayout(row2)

    row3 = QHBoxLayout()
    for i, label in enumerate(["Radio 1", "Radio 2", "Radio 3"]):
        rb = QRadioButton(label)
        rb.setChecked(i == 0)
        row3.addWidget(rb)
    layout.addLayout(row3)

    parent.addWidget(section)


def _setup_sliders(parent: QVBoxLayout) -> None:
    section = _make_section("Sliders & Progress")
    layout = section.layout()

    progress = QProgressBar()
    progress.setRange(0, 100)
    progress.setValue(35)
    layout.addWidget(progress)

    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(0, 100)
    slider.setValue(35)
    slider.valueChanged.connect(progress.setValue)
    layout.addWidget(slider)

    row = QHBoxLayout()
    dial = QDial()
    dial.setRange(0, 100)
    dial.setValue(50)
    dial.setNotchesVisible(True)
    dial.setFixedSize(64, 64)
    row.addWidget(dial)

    spinner = LoadingSpinner()
    spinner.setFixedSize(48, 48)
    row.addWidget(spinner)
    row.addStretch()
    layout.addLayout(row)

    parent.addWidget(section)


def _setup_qlementine_widgets(parent: QVBoxLayout) -> None:
    section = _make_section("Qlementine Widgets")
    layout = section.layout()

    expand_btn = QPushButton("Toggle Expander")
    layout.addWidget(expand_btn)
    expander = Expander()
    inner = QWidget()
    inner_layout = QVBoxLayout(inner)
    inner_layout.setContentsMargins(0, 0, 0, 0)
    inner_layout.addWidget(Label("Hidden content revealed!"))
    inner_line = LineEdit()
    inner_line.setPlaceholderText("An input inside the expander")
    inner_layout.addWidget(inner_line)
    expander.setContent(inner)
    expand_btn.clicked.connect(expander.toggleExpanded)
    layout.addWidget(expander)

    row = QHBoxLayout()
    color_btn = ColorButton()
    row.addWidget(Label("Color:"))
    row.addWidget(color_btn)

    color_editor = ColorEditor()
    row.addWidget(color_editor)
    row.addStretch()
    layout.addLayout(row)

    row2 = QHBoxLayout()
    badge = StatusBadgeWidget()
    row2.addWidget(Label("Status badge:"))
    row2.addWidget(badge)

    notif = NotificationBadge()
    notif.setText("3")
    row2.addWidget(Label("Notification:"))
    row2.addWidget(notif)
    row2.addStretch()
    layout.addLayout(row2)

    parent.addWidget(section)


class DemoWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQt6-Qlementine Demo")
        self.setMinimumSize(600, 400)
        self.resize(700, 800)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # --- Tab 1: Widget Gallery ---
        gallery = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(gallery)

        gallery_layout = QVBoxLayout(gallery)
        gallery.setSizePolicy(
            gallery.sizePolicy().horizontalPolicy(),
            gallery.sizePolicy().verticalPolicy(),
        )

        _setup_labels(gallery_layout)
        _setup_buttons(gallery_layout)
        _setup_inputs(gallery_layout)
        _setup_toggles(gallery_layout)
        _setup_sliders(gallery_layout)
        _setup_qlementine_widgets(gallery_layout)
        gallery_layout.addStretch()

        tabs.addTab(scroll, "Widget Gallery")

        # --- Tab 2: Form Example ---
        form = QWidget()
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setWidget(form)
        form_layout = QVBoxLayout(form)

        title = Label()
        title.setText("Settings")
        title.setRole(TextRole.H2)
        form_layout.addWidget(title)

        general = _make_section("General")
        gl = general.layout()
        name_edit = LineEdit()
        name_edit.setPlaceholderText("Project name")
        gl.addWidget(name_edit)
        desc_edit = PlainTextEdit()
        desc_edit.setPlaceholderText("Description")
        desc_edit.setFixedHeight(60)
        gl.addWidget(desc_edit)
        form_layout.addWidget(general)

        appearance = _make_section("Appearance")
        al = appearance.layout()
        dark_switch = Switch()
        dark_switch.setText("Dark mode")
        al.addWidget(dark_switch)
        anim_switch = Switch()
        anim_switch.setText("Enable animations")
        anim_switch.setChecked(True)
        al.addWidget(anim_switch)
        form_layout.addWidget(appearance)

        form_layout.addStretch()

        row = QHBoxLayout()
        row.addStretch()
        save_btn = QPushButton("Save")
        save_btn.setDefault(True)
        row.addWidget(save_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFlat(True)
        row.addWidget(cancel_btn)
        form_layout.addLayout(row)

        tabs.addTab(form_scroll, "Form Example")


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Qlementine Demo")

    style = QlementineStyle(app)
    style.setAutoIconColor(AutoIconColor.TextColor)
    style.setAnimationsEnabled(True)
    app.setStyle(style)

    window = DemoWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
