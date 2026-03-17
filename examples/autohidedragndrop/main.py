import os
import sys

import PyQt6Ads as QtAds
from PyQt6 import uic
from PyQt6.QtCore import QSignalBlocker, Qt
from PyQt6.QtGui import (
    QAction,
    QCloseEvent,
    QDragEnterEvent,
    QDragLeaveEvent,
    QDropEvent,
)
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QInputDialog,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QWidgetAction,
)

UI_FILE = os.path.join(os.path.dirname(__file__), "mainwindow.ui")
MainWindowUI, MainWindowBase = uic.loadUiType(UI_FILE)


class DroppableItem(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.setCursor(Qt.CursorShape.DragMoveCursor)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.unsetCursor()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.setText(event.mimeData().text())


class MainWindow(MainWindowUI, MainWindowBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        QtAds.CDockManager.setConfigFlag(
            QtAds.CDockManager.eConfigFlag.OpaqueSplitterResize, True
        )
        QtAds.CDockManager.setConfigFlag(
            QtAds.CDockManager.eConfigFlag.XmlCompressionEnabled, False
        )
        QtAds.CDockManager.setConfigFlag(
            QtAds.CDockManager.eConfigFlag.FocusHighlighting, True
        )
        # QtAds.CDockManager.setAutoHideConfigFlag(
        #     QtAds.CDockManager.eAutoHideFlag.AutoHideOpenOnDragHover, True
        # )
        self.dock_manager = QtAds.CDockManager(self)

        # Set central widget
        text_edit = QPlainTextEdit()
        text_edit.setPlaceholderText(
            "This is the central editor. Enter your text here."
        )
        central_dock_widget = QtAds.CDockWidget("CentralWidget")
        central_dock_widget.setWidget(text_edit)
        central_dock_area = self.dock_manager.setCentralWidget(central_dock_widget)
        central_dock_area.setAllowedAreas(QtAds.DockWidgetArea.OuterDockAreas)

        droppable_item = DroppableItem("Drop text here.")
        drop_dock_widget = QtAds.CDockWidget("Tab")
        drop_dock_widget.setWidget(droppable_item)
        drop_dock_widget.setMinimumSizeHintMode(
            QtAds.CDockWidget.eMinimumSizeHintMode.MinimumSizeHintFromDockWidget
        )
        drop_dock_widget.setMinimumSize(200, 150)
        drop_dock_widget.setAcceptDrops(True)
        drop_area = self.dock_manager.addDockWidget(
            QtAds.DockWidgetArea.LeftDockWidgetArea, drop_dock_widget
        )
        drop_area.setAcceptDrops(True)
        self.menuView.addAction(drop_dock_widget.toggleViewAction())

        self.create_perspective_ui()

    def create_perspective_ui(self):
        save_perspective_action = QAction("Create Perspective", self)
        save_perspective_action.triggered.connect(self.save_perspective)
        perspective_list_action = QWidgetAction(self)
        self.perspective_combobox = QComboBox(self)
        self.perspective_combobox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.perspective_combobox.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.perspective_combobox.currentTextChanged.connect(
            self.dock_manager.openPerspective
        )
        perspective_list_action.setDefaultWidget(self.perspective_combobox)
        self.toolBar.addSeparator()
        self.toolBar.addAction(perspective_list_action)
        self.toolBar.addAction(save_perspective_action)

    def save_perspective(self):
        perspective_name, ok = QInputDialog.getText(
            self, "Save Perspective", "Enter Unique name:"
        )
        if not ok or not perspective_name:
            return

        self.dock_manager.addPerspective(perspective_name)
        QSignalBlocker(self.perspective_combobox)
        self.perspective_combobox.clear()
        self.perspective_combobox.addItems(self.dock_manager.perspectiveNames())
        self.perspective_combobox.setCurrentText(perspective_name)

    def closeEvent(self, event: QCloseEvent):
        self.dock_manager.deleteLater()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    app.exec()
