from __future__ import annotations

try:
    import PyQt6Qlementine as Qlementine
    from PyQt6.QtCore import QMargins, QPoint, QSize, Qt
    from PyQt6.QtGui import QAction, QColor, QIcon
    from PyQt6.QtWidgets import QWidget

    BACKEND = "PyQt6"
except ImportError:
    import PySide6Qlementine as Qlementine  # type: ignore
    from PySide6.QtCore import QMargins, QPoint, QSize, Qt  # type: ignore
    from PySide6.QtGui import QAction, QColor, QIcon  # type: ignore
    from PySide6.QtWidgets import QWidget  # type: ignore

    BACKEND = "PySide6"

__all__ = [
    "BACKEND",
    "QAction",
    "QColor",
    "QIcon",
    "QMargins",
    "QPoint",
    "QSize",
    "QWidget",
    "Qlementine",
    "Qt",
]
