"""Tests for QlementineStyle.setIconPathGetter."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from _qt_compat import QIcon, Qlementine, QSize

QlementineStyle = Qlementine.QlementineStyle

# A real SVG file shipped with the qlementine repo (outside Qt resources).
_REPO_ROOT = Path(__file__).resolve().parent.parent
_TEST_SVG = _REPO_ROOT / "qlementine" / "sandbox" / "resources" / "test_image_16x16.svg"


def test_set_icon_path_getter_with_callable(qapp):
    """setIconPathGetter accepts a plain Python callable."""
    style = QlementineStyle()
    getter = MagicMock(return_value=str(_TEST_SVG))
    style.setIconPathGetter(getter)

    icon = style.makeThemedIconFromName("anything")
    assert isinstance(icon, QIcon)
    assert not icon.isNull()
    getter.assert_called_once_with("anything")


def test_set_icon_path_getter_with_lambda(qapp):
    """setIconPathGetter works with a lambda."""
    style = QlementineStyle()
    style.setIconPathGetter(lambda name: str(_TEST_SVG))

    icon = style.makeThemedIconFromName("test")
    assert not icon.isNull()


def test_set_icon_path_getter_accepts_pathlike(qapp):
    """The callback may return a pathlib.Path (or any os.PathLike)."""
    style = QlementineStyle()
    style.setIconPathGetter(lambda name: _TEST_SVG)  # returns Path, not str

    icon = style.makeThemedIconFromName("test")
    assert not icon.isNull()


def test_set_icon_path_getter_none_clears(qapp):
    """Passing None clears a previously set getter (falls back to QIcon.fromTheme)."""
    style = QlementineStyle()
    style.setIconPathGetter(lambda name: str(_TEST_SVG))
    style.setIconPathGetter(None)

    # Without a getter and without an icon theme, fromTheme returns a null icon.
    icon = style.makeThemedIconFromName("nonexistent-icon-name")
    assert icon.isNull()


def test_set_icon_path_getter_rejects_non_callable(qapp):
    """Passing a non-callable raises TypeError."""
    style = QlementineStyle()
    with pytest.raises(TypeError):
        style.setIconPathGetter(42)  # type: ignore[arg-type]


def test_set_icon_path_getter_forwards_name(qapp):
    """The icon name is correctly forwarded to the Python callback."""
    received = []
    style = QlementineStyle()
    style.setIconPathGetter(lambda name: (received.append(name), str(_TEST_SVG))[1])

    style.makeThemedIconFromName("mdi:bell")
    style.makeThemedIconFromName("mdi:check")
    assert received == ["mdi:bell", "mdi:check"]


@pytest.mark.parametrize("size", [QSize(16, 16), QSize(24, 24), QSize(48, 48)])
def test_set_icon_path_getter_with_sizes(qapp, size):
    """Icons created via the getter respect the requested size."""
    style = QlementineStyle()
    style.setIconPathGetter(lambda name: str(_TEST_SVG))

    icon = style.makeThemedIconFromName("test", size)
    assert not icon.isNull()
    # availableSizes confirms the icon was created at the requested logical size.
    assert size in icon.availableSizes()
