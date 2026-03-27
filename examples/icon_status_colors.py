# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pyconify>=0.2.1",
#     "pyqt6>=6.10.2",
#     "pyqt6-qlementine",
# ]
#
# [tool.uv.sources]
# pyqt6-qlementine = { path = "../packages/PyQt6-Qlementine" }
# ///
"""Demo: per-widget icon status colorization.

Shows how to use QlementineStyle.setIconStatus() to colorize widget icons
with the theme's status colors (Error, Warning, Success, Info).

Uses pyconify + setIconPathGetter to resolve icon names to SVG paths.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pyconify import svg_path
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6Qlementine import AutoIconColor, QlementineStyle, Status


def _icon(name: str) -> QIcon:
    """Create a QIcon from an iconify name via pyconify."""
    return QIcon(str(svg_path(name)))


class StatusIconDemo(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Icon Status Colors")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --- Push buttons with status-colored icons ---
        btn_group = QGroupBox("QPushButtons with iconStatus")
        btn_layout = QHBoxLayout(btn_group)

        statuses = [
            (Status.Default, "Default", "mdi:information-outline"),
            (Status.Info, "Info", "mdi:information"),
            (Status.Success, "Success", "mdi:check-circle"),
            (Status.Warning, "Warning", "mdi:alert"),
            (Status.Error, "Error", "mdi:alert-circle"),
        ]
        for status, label, icon_name in statuses:
            btn = QPushButton(_icon(icon_name), label)
            btn.setIconSize(QSize(20, 20))
            QlementineStyle.setIconStatus(btn, status)
            btn_layout.addWidget(btn)

        layout.addWidget(btn_group)

        # --- Tool buttons with different icons ---
        tool_group = QGroupBox("QToolButtons with iconStatus")
        tool_layout = QHBoxLayout(tool_group)

        tool_icons = [
            (Status.Default, "Default", "mdi:cog"),
            (Status.Info, "Info", "mdi:download"),
            (Status.Success, "Success", "mdi:cloud-check"),
            (Status.Warning, "Warning", "mdi:shield-alert"),
            (Status.Error, "Error", "mdi:trash-can"),
        ]
        for status, label, icon_name in tool_icons:
            tb = QToolButton()
            tb.setIcon(_icon(icon_name))
            tb.setText(label)
            tb.setIconSize(QSize(20, 20))
            tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            QlementineStyle.setIconStatus(tb, status)
            tool_layout.addWidget(tb)

        layout.addWidget(tool_group)

        # --- Same icon, different statuses ---
        same_group = QGroupBox("Same icon (mdi:bell), different statuses")
        same_layout = QHBoxLayout(same_group)
        bell = _icon("mdi:bell")
        for status, label, _ in statuses:
            btn = QPushButton(bell, label)
            btn.setIconSize(QSize(20, 20))
            QlementineStyle.setIconStatus(btn, status)
            same_layout.addWidget(btn)
        layout.addWidget(same_group)

        # --- Parent inheritance demo ---
        inherit_group = QGroupBox("Parent inheritance: set iconStatus on the container")
        inherit_layout = QHBoxLayout(inherit_group)

        folder = _icon("mdi:folder")
        file_icon = _icon("mdi:file-document")
        for status, label in [
            (Status.Error, "Error container"),
            (Status.Success, "Success container"),
        ]:
            container = QWidget()
            QlementineStyle.setIconStatus(container, status)
            clayout = QVBoxLayout(container)
            clayout.addWidget(QLabel(label))
            clayout.addWidget(QPushButton(folder, "Folder"))
            clayout.addWidget(QPushButton(file_icon, "Document"))
            inherit_layout.addWidget(container)

        # No override for comparison
        container = QWidget()
        clayout = QVBoxLayout(container)
        clayout.addWidget(QLabel("No override"))
        clayout.addWidget(QPushButton(folder, "Folder"))
        clayout.addWidget(QPushButton(file_icon, "Document"))
        inherit_layout.addWidget(container)

        layout.addWidget(inherit_group)
        layout.addStretch()
        self.resize(750, 550)


RESOURCE = Path(__file__).resolve().parents[1] / "qlementine" / "showcase" / "resources"


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Icon Status Colors Demo")

    style = QlementineStyle(app)
    style.setAutoIconColor(AutoIconColor.ForegroundColor)
    style.setAnimationsEnabled(True)
    if "--dark" in sys.argv:
        dark_json = RESOURCE / "themes" / "dark.json"
        style.setThemeJsonPath(str(dark_json))
    app.setStyle(style)

    window = StatusIconDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
