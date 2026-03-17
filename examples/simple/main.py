import os
import sys

import PyQt6Ads as QtAds
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel

UI_FILE = os.path.join(os.path.dirname(__file__), "MainWindow.ui")
MainWindowUI, MainWindowBase = uic.loadUiType(UI_FILE)


class MainWindow(MainWindowUI, MainWindowBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        # Create the dock manager. Because the parent parameter is a QMainWindow
        # the dock manager registers itself as the central widget.
        self.dock_manager = QtAds.CDockManager(self)

        # Create example content label - this can be any application specific
        # widget
        lbl = QLabel()
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        lbl.setText("Lorem ipsum dolor sit amet, consectetuer adipiscing elit. ")

        # Create a dock widget with the title Label 1 and set the created label
        # as the dock widget content
        dock_widget = QtAds.CDockWidget("Label 1")
        dock_widget.setWidget(lbl)

        # Add the toggleViewAction of the dock widget to the menu to give
        # the user the possibility to show the dock widget if it has been closed
        self.menuView.addAction(dock_widget.toggleViewAction())

        # Add the dock widget to the top dock widget area
        self.dock_manager.addDockWidget(
            QtAds.DockWidgetArea.TopDockWidgetArea, dock_widget
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    app.exec()
