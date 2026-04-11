"""Tests for IconUtils free functions and IconTheme struct."""

from __future__ import annotations

from _qt_compat import QColor, QIcon, Qlementine, QSize, QtCore

IconTheme = Qlementine.IconTheme
QlementineStyle = Qlementine.QlementineStyle
ColorRole = Qlementine.ColorRole


SVG_CONTENT = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'
    "<circle cx='8' cy='8' r='6'/></svg>"
)
SVG_BYTES = QtCore.QByteArray(SVG_CONTENT.encode("utf-8"))


def test_icon_theme_single_color():
    theme = IconTheme(QColor(255, 0, 0))
    assert theme.normal == QColor(255, 0, 0)


def test_icon_theme_two_colors():
    theme = IconTheme(QColor(255, 0, 0), QColor(128, 128, 128))
    assert theme.normal == QColor(255, 0, 0)
    assert theme.disabled == QColor(128, 128, 128)


def test_icon_theme_four_colors():
    theme = IconTheme(
        QColor(255, 0, 0),
        QColor(128, 128, 128),
        QColor(0, 255, 0),
        QColor(64, 64, 64),
    )
    assert theme.checkedNormal == QColor(0, 255, 0)
    assert theme.checkedDisabled == QColor(64, 64, 64)


def test_icon_theme_color_method():
    theme = IconTheme(QColor(255, 0, 0), QColor(128, 128, 128))
    color = theme.color(QIcon.Mode.Normal, QIcon.State.Off)
    assert color == QColor(255, 0, 0)
    color = theme.color(QIcon.Mode.Disabled, QIcon.State.Off)
    assert color == QColor(128, 128, 128)


def test_make_icon_from_svg(qapp, tmp_path):
    svg_file = tmp_path / "icon.svg"
    svg_file.write_text(SVG_CONTENT)
    icon = Qlementine.utils.makeIconFromSvg(str(svg_file), QSize(16, 16))
    assert isinstance(icon, QIcon)


def test_make_icon_from_svg_with_theme(qapp, tmp_path):
    svg_file = tmp_path / "icon.svg"
    svg_file.write_text(SVG_CONTENT)
    theme = IconTheme(QColor(255, 0, 0))
    icon = Qlementine.utils.makeIconFromSvg(str(svg_file), theme, QSize(16, 16))
    assert isinstance(icon, QIcon)


def test_make_icon_from_svg_data(qapp):
    """makeIconFromSvgData takes in-memory SVG bytes (no filesystem hit)."""
    icon = Qlementine.utils.makeIconFromSvgData(SVG_BYTES, QSize(16, 16))
    assert isinstance(icon, QIcon)
    assert not icon.isNull()
    # Pixmap should actually render (non-null) at the requested logical size.
    # Raw size may be scaled by devicePixelRatio on HiDPI, so compare
    # device-independent size instead.
    pm = icon.pixmap(QSize(16, 16))
    assert not pm.isNull()
    assert pm.deviceIndependentSize().toSize() == QSize(16, 16)


def test_make_icon_from_svg_data_with_theme(qapp):
    theme = IconTheme(QColor(255, 0, 0))
    icon = Qlementine.utils.makeIconFromSvgData(SVG_BYTES, theme, QSize(24, 24))
    assert isinstance(icon, QIcon)
    assert not icon.isNull()


def test_make_icon_from_svg_data_default_size(qapp):
    """The (data, theme) overload defaults size to 16x16."""
    theme = IconTheme(QColor(0, 0, 255))
    icon = Qlementine.utils.makeIconFromSvgData(SVG_BYTES, theme)
    assert isinstance(icon, QIcon)
    assert not icon.isNull()


def test_make_themed_icon_from_data(qapp):
    """QlementineStyle.makeThemedIconFromData works with only the SVG bytes."""
    style = QlementineStyle()
    icon = style.makeThemedIconFromData(SVG_BYTES)
    assert isinstance(icon, QIcon)
    assert not icon.isNull()


def test_make_themed_icon_from_data_with_size(qapp):
    style = QlementineStyle()
    icon = style.makeThemedIconFromData(SVG_BYTES, QSize(32, 32))
    assert isinstance(icon, QIcon)
    assert not icon.isNull()
    pm = icon.pixmap(QSize(32, 32))
    assert pm.deviceIndependentSize().toSize() == QSize(32, 32)


def test_make_themed_icon_from_data_with_role(qapp):
    """Both Primary and Secondary roles produce valid (non-null) icons."""
    style = QlementineStyle()
    primary = style.makeThemedIconFromData(
        SVG_BYTES, QSize(16, 16), ColorRole.Primary
    )
    secondary = style.makeThemedIconFromData(
        SVG_BYTES, QSize(16, 16), ColorRole.Secondary
    )
    assert not primary.isNull()
    assert not secondary.isNull()
