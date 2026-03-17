import sys

import PyQt6Ads as QtAds
from PyQt6.QtCore import qDebug
from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    dock_manager = None

    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        if self.dock_manager is not None:
            self.dock_manager.deleteLater()

    def setDockManager(self, dock_manager: QtAds.CDockManager):
        self.dock_manager = dock_manager


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()

    QtAds.CDockManager.setConfigFlag(
        QtAds.CDockManager.eConfigFlag.FocusHighlighting, True
    )
    QtAds.CDockManager.setConfigFlag(
        QtAds.CDockManager.eConfigFlag.AllTabsHaveCloseButton, True
    )
    dock_manager = QtAds.CDockManager(w)
    w.setDockManager(dock_manager)

    count = 0

    def on_focused_dock_widget_changed(old: QtAds.CDockWidget, now: QtAds.CDockWidget):
        global count
        old_name = old.objectName() if old else "-"
        msg = (
            f"{count:d} CDockManager::focusedDockWidgetChanged old: {old_name} now: "
            f"{now.objectName()} visible: {now.isVisible()}"
        )
        qDebug(msg)
        count += 1
        now.widget().setFocus()

    dock_manager.focusedDockWidgetChanged.connect(on_focused_dock_widget_changed)

    action = QAction("New Delete On Close", w)
    w.menuBar().addAction(action)

    i = 0

    def on_action_triggered():
        global i
        dw = QtAds.CDockWidget(f"test doc {i:d}")
        i += 1
        editor = QTextEdit("lorem ipsum...", dw)
        dw.setWidget(editor)
        dw.setFeature(QtAds.CDockWidget.DockWidgetDeleteOnClose, True)
        area = dock_manager.addDockWidgetTab(
            QtAds.DockWidgetArea.CenterDockWidgetArea, dw
        )
        qDebug(f"doc dock widget created! {dw} {area}")

    action.triggered.connect(on_action_triggered)

    action = QAction("New", w)
    w.menuBar().addAction(action)

    def on_action2_triggered():
        global i
        dw = QtAds.CDockWidget(f"test {i:d}")
        i += 1
        editor = QTextEdit("lorem ipsum...", dw)
        dw.setWidget(editor)
        area = dock_manager.addDockWidgetTab(
            QtAds.DockWidgetArea.CenterDockWidgetArea, dw
        )
        qDebug(f"dock widget created! {dw} {area}")

    action.triggered.connect(on_action2_triggered)

    w.show()
    app.exec()
