from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
    from PySide6.QtCore import QMargins, QPoint, QSize, Qt, QTimer  # type: ignore
    from PySide6.QtGui import QAction, QColor, QIcon  # type: ignore
    from PySide6.QtWidgets import QWidget  # type: ignore

    BACKEND: str
else:
    try:
        from PyQt6 import QtCore, QtGui, QtWidgets  # type: ignore
        from PyQt6.QtCore import QMargins, QPoint, QSize, Qt, QTimer
        from PyQt6.QtGui import QAction, QColor, QIcon
        from PyQt6.QtWidgets import QWidget

        BACKEND = "PyQt6"
    except ImportError:
        from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
        from PySide6.QtCore import QMargins, QPoint, QSize, Qt, QTimer  # type: ignore
        from PySide6.QtGui import QAction, QColor, QIcon  # type: ignore
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
    "QIcon",
    "QMargins",
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
