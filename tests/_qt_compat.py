from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
    from PySide6.QtCore import (  # type: ignore
        QJsonDocument,
        QMargins,
        QModelIndex,
        QPoint,
        QSize,
        Qt,
        QTimer,
    )
    from PySide6.QtGui import (  # type: ignore
        QAction,
        QColor,
        QFont,
        QIcon,
        QImage,
        QPainter,
        QPalette,
        QPixmap,
    )
    from PySide6.QtWidgets import QWidget  # type: ignore

    BACKEND: str
else:
    try:
        from PyQt6 import QtCore, QtGui, QtWidgets  # type: ignore
        from PyQt6.QtCore import (
            QJsonDocument,
            QMargins,
            QModelIndex,
            QPoint,
            QSize,
            Qt,
            QTimer,
        )
        from PyQt6.QtGui import (
            QAction,
            QColor,
            QFont,
            QIcon,
            QImage,
            QPainter,
            QPalette,
            QPixmap,
        )
        from PyQt6.QtWidgets import QWidget

        BACKEND = "PyQt6"
    except ImportError:
        from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
        from PySide6.QtCore import (  # type: ignore
            QJsonDocument,
            QMargins,
            QModelIndex,
            QPoint,
            QSize,
            Qt,
            QTimer,
        )
        from PySide6.QtGui import (  # type: ignore
            QAction,
            QColor,
            QFont,
            QIcon,
            QImage,
            QPainter,
            QPalette,
            QPixmap,
        )
        from PySide6.QtWidgets import QWidget  # type: ignore

    BACKEND = "PySide6"

try:
    import PyQt6Qlementine as Qlementine
except ImportError:
    import PySide6Qlementine as Qlementine  # type: ignore

__all__ = [
    "BACKEND",
    "QAction",
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
    "QSize",
    "QTimer",
    "QWidget",
    "Qlementine",
    "Qt",
    "QtCore",
    "QtGui",
    "QtWidgets",
]
