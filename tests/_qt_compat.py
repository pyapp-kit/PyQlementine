from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore

    BACKEND: str
else:
    try:
        from PyQt6 import QtCore, QtGui, QtWidgets  # type: ignore

        BACKEND = "PyQt6"
    except ImportError:
        from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore

        BACKEND = "PySide6"

try:
    import PyQt6Qlementine as Qlementine
except ImportError:
    import PySide6Qlementine as Qlementine  # type: ignore

QJsonDocument = QtCore.QJsonDocument
QMargins = QtCore.QMargins
QModelIndex = QtCore.QModelIndex
QPoint = QtCore.QPoint
QPointF = QtCore.QPointF
QSize = QtCore.QSize
Qt = QtCore.Qt
QTimer = QtCore.QTimer

QAction = QtGui.QAction
QColor = QtGui.QColor
QFont = QtGui.QFont
QIcon = QtGui.QIcon
QImage = QtGui.QImage
QPainter = QtGui.QPainter
QPalette = QtGui.QPalette
QPixmap = QtGui.QPixmap

QWidget = QtWidgets.QWidget
QApplication = QtWidgets.QApplication


__all__ = [
    "BACKEND",
    "QAction",
    "QApplication",
    "QColor",
    "QFont",
    "QIcon",
    "QImage",
    "QJsonDocument",
    "QMargins",
    "QModelIndex",
    "QPainter",
    "QPalette",
    "QPixmap",
    "QPoint",
    "QPointF",
    "QSize",
    "QTimer",
    "QWidget",
    "Qlementine",
    "Qt",
    "QtCore",
    "QtGui",
    "QtWidgets",
]
