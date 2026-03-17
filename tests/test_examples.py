import runpy
from pathlib import Path
from unittest.mock import patch

import PyQt6Ads  # noqa  # import here to ensure that it works regardless of order
import pytest
from PyQt6.QtWidgets import QApplication

HERE = Path(__file__)
EXAMPLES = HERE.parent.parent / "examples"
MAINS = EXAMPLES.rglob("main.py")

app = QApplication.instance() or QApplication([])


@pytest.mark.parametrize(
    "main", MAINS, ids=lambda path: str(path.parent.relative_to(EXAMPLES))
)
def test_example(main: Path) -> None:
    with patch("PyQt6.QtWidgets.QApplication"):
        runpy.run_path(str(main), run_name="__main__")
        for widget in QApplication.topLevelWidgets():
            widget.close()
            widget.deleteLater()
        QApplication.processEvents()
