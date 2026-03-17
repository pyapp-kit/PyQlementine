"""Pure-Python dataclasses mirroring oclero::qlementine::Theme."""

from __future__ import annotations

import re
import sys
from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import PyQt6Qlementine
    from PyQt6 import QtCore
    from typing_extensions import TypeAlias

    QColorLike: TypeAlias = str


@dataclass
class ThemeMeta:
    """Metadata about a Qlementine Theme."""

    name: str = ""
    version: str = ""
    author: str = ""


@dataclass
class Theme:
    """Color and sizes configuration for a Qlementine Theme."""

    meta: ThemeMeta = field(default_factory=ThemeMeta)

    background_color_main1: QColorLike = "#FFFFFF"
    background_color_main2: QColorLike = "#F3F3F3"
    background_color_main3: QColorLike = "#E3E3E3"
    background_color_main4: QColorLike = "#DCDCDC"
    background_color_workspace: QColorLike = "#B7B7B7"
    background_color_tab_bar: QColorLike = "#B7B7B7"

    neutral_color: QColorLike = "#E1E1E1"
    neutral_color_hovered: QColorLike = "#DADADA"
    neutral_color_pressed: QColorLike = "#D2D2D2"
    neutral_color_disabled: QColorLike = "#EEEEEE"

    focus_color: QColorLike = "#6640A9FF"

    primary_color: QColorLike = "#1890FF"
    primary_color_hovered: QColorLike = "#2C9DFF"
    primary_color_pressed: QColorLike = "#40A9FF"
    primary_color_disabled: QColorLike = "#D1E9FF"

    primary_color_foreground: QColorLike = "#FFFFFF"
    primary_color_foreground_hovered: QColorLike = "#FFFFFF"
    primary_color_foreground_pressed: QColorLike = "#FFFFFF"
    primary_color_foreground_disabled: QColorLike = "#ECF6FF"

    primary_alternative_color: QColorLike = "#106EF9"
    primary_alternative_color_hovered: QColorLike = "#107BFD"
    primary_alternative_color_pressed: QColorLike = "#108BFD"
    primary_alternative_color_disabled: QColorLike = "#A9D6FF"

    secondary_color: QColorLike = "#404040"
    secondary_color_hovered: QColorLike = "#333333"
    secondary_color_pressed: QColorLike = "#262626"
    secondary_color_disabled: QColorLike = "#D4D4D4"

    secondary_color_foreground: QColorLike = "#FFFFFF"
    secondary_color_foreground_hovered: QColorLike = "#FFFFFF"
    secondary_color_foreground_pressed: QColorLike = "#FFFFFF"
    secondary_color_foreground_disabled: QColorLike = "#EDEDED"

    secondary_alternative_color: QColorLike = "#909090"
    secondary_alternative_color_hovered: QColorLike = "#747474"
    secondary_alternative_color_pressed: QColorLike = "#828282"
    secondary_alternative_color_disabled: QColorLike = "#C3C3C3"

    status_color_success: QColorLike = "#2BB5A0"
    status_color_success_hovered: QColorLike = "#3CBFAB"
    status_color_success_pressed: QColorLike = "#4ECDB9"
    status_color_success_disabled: QColorLike = "#D5F0EC"

    status_color_info: QColorLike = "#1BA8D5"
    status_color_info_hovered: QColorLike = "#1EB5E5"
    status_color_info_pressed: QColorLike = "#29C0F0"
    status_color_info_disabled: QColorLike = "#C7EAF5"

    status_color_warning: QColorLike = "#FBC064"
    status_color_warning_hovered: QColorLike = "#FFCF6C"
    status_color_warning_pressed: QColorLike = "#FFD880"
    status_color_warning_disabled: QColorLike = "#FEEFD8"

    status_color_error: QColorLike = "#E96B72"
    status_color_error_hovered: QColorLike = "#F47C83"
    status_color_error_pressed: QColorLike = "#FF9197"
    status_color_error_disabled: QColorLike = "#F9DADC"

    status_color_foreground: QColorLike = "#FFFFFF"
    status_color_foreground_hovered: QColorLike = "#FFFFFF"
    status_color_foreground_pressed: QColorLike = "#FFFFFF"
    status_color_foreground_disabled: QColorLike = "#99FFFFFF"

    shadow_color1: QColorLike = "#20000000"
    shadow_color2: QColorLike = "#40000000"
    shadow_color3: QColorLike = "#60000000"

    border_color: QColorLike = "#D3D3D3"
    border_color_hovered: QColorLike = "#B3B3B3"
    border_color_pressed: QColorLike = "#A3A3A3"
    border_color_disabled: QColorLike = "#E9E9E9"

    semi_transparent_color1: QColorLike = "#00000000"
    semi_transparent_color2: QColorLike = "#19000000"
    semi_transparent_color3: QColorLike = "#21000000"
    semi_transparent_color4: QColorLike = "#28000000"

    use_system_fonts: bool = False

    font_size: int = 12
    font_size_monospace: int = 13
    font_size_h1: int = 34
    font_size_h2: int = 26
    font_size_h3: int = 22
    font_size_h4: int = 18
    font_size_h5: int = 14
    font_size_s1: int = 10

    animation_duration: int = 192
    focus_animation_duration: int = 384
    slider_animation_duration: int = 96

    border_radius: float = 6.0
    check_box_border_radius: float = 4.0
    menu_item_border_radius: float = 4.0
    menu_bar_item_border_radius: float = 2.0
    border_width: int = 1

    control_height_large: int = 28
    control_height_medium: int = 24
    control_height_small: int = 16
    control_default_width: int = 96

    dial_mark_length: int = 8
    dial_mark_thickness: int = 2
    dial_tick_length: int = 4
    dial_tick_spacing: int = 4
    dial_groove_thickness: int = 4

    focus_border_width: int = 2

    icon_extent: int = 16

    slider_tick_size: int = 3
    slider_tick_spacing: int = 2
    slider_tick_thickness: int = 1
    slider_groove_height: int = 4

    progress_bar_groove_height: int = 6
    spacing: int = 8

    scroll_bar_thickness_full: int = 12
    scroll_bar_thickness_small: int = 6
    scroll_bar_margin: int = 0

    tab_bar_padding_top: int = 4
    tab_bar_tab_max_width: int = 0
    tab_bar_tab_min_width: int = 0

    def toJsonDoc(self) -> QtCore.QJsonDocument:
        theme_dict = _to_camel_case_dict(asdict(self))
        return _qt_core().QJsonDocument.fromVariant(theme_dict)

    def toQlementine(self) -> PyQt6Qlementine.Theme:
        import PyQt6Qlementine

        doc = self.toJsonDoc()
        return PyQt6Qlementine.Theme.fromJsonDoc(doc)


def _snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase (e.g. 'font_size_h1' -> 'fontSizeH1')."""
    return re.sub(r"_([a-zA-Z0-9])", lambda m: m.group(1).upper(), name)


def _to_camel_case_dict(d: dict[str, Any]) -> dict[str, Any]:
    """Recursively convert all dict keys from snake_case to camelCase."""
    out: dict[str, Any] = {}
    for key, value in d.items():
        camel_key = _snake_to_camel(key)
        if isinstance(value, dict):
            value = _to_camel_case_dict(value)
        out[camel_key] = value
    return out


# ─── Radix Themes (Indigo accent / Slate gray) ──────────────────────
#
# Colors derived from Radix UI color scales:
#   Slate:  1-12 step neutral gray with slight blue tint
#   Indigo: 1-12 step blue-purple accent
#   Red/Green/Amber/Cyan: status colors from Radix scales

RADIX_INDIGO_LIGHT = Theme(
    meta=ThemeMeta(name="Radix Indigo Light", author="Radix UI"),
    # Backgrounds: slate-1 through slate-4, slate-8 for workspace/tabbar
    background_color_main1="#FCFCFD",  # slate-1
    background_color_main2="#F9F9FB",  # slate-2
    background_color_main3="#F0F0F3",  # slate-3
    background_color_main4="#E8E8EC",  # slate-4
    background_color_workspace="#B9BBC6",  # slate-8
    background_color_tab_bar="#B9BBC6",  # slate-8
    # Neutrals: slate-4/5/6/3
    neutral_color="#E8E8EC",  # slate-4
    neutral_color_hovered="#E0E1E6",  # slate-5
    neutral_color_pressed="#D9D9E0",  # slate-6
    neutral_color_disabled="#F0F0F3",  # slate-3
    # Focus: indigo-7 @ ~40% alpha
    focus_color="#66ABBDF9",
    # Primary: indigo-9/10/11, indigo-6 disabled
    primary_color="#3E63DD",  # indigo-9
    primary_color_hovered="#3358D4",  # indigo-10
    primary_color_pressed="#3A5BC7",  # indigo-11
    primary_color_disabled="#C1D0FF",  # indigo-6
    primary_color_foreground="#FFFFFF",
    primary_color_foreground_hovered="#FFFFFF",
    primary_color_foreground_pressed="#FFFFFF",
    primary_color_foreground_disabled="#E1E9FF",  # indigo-4
    # Primary alternative: deeper indigo shades
    primary_alternative_color="#3358D4",  # indigo-10
    primary_alternative_color_hovered="#3A5BC7",  # indigo-11
    primary_alternative_color_pressed="#1F2D5C",  # indigo-12
    primary_alternative_color_disabled="#D2DEFF",  # indigo-5
    # Secondary: slate-12/11/10, slate-8 disabled
    secondary_color="#1C2024",  # slate-12
    secondary_color_hovered="#60646C",  # slate-11
    secondary_color_pressed="#80838D",  # slate-10
    secondary_color_disabled="#B9BBC6",  # slate-8
    secondary_color_foreground="#FFFFFF",
    secondary_color_foreground_hovered="#FFFFFF",
    secondary_color_foreground_pressed="#FFFFFF",
    secondary_color_foreground_disabled="#E8E8EC",  # slate-4
    # Secondary alternative: slate mid-range
    secondary_alternative_color="#8B8D98",  # slate-9
    secondary_alternative_color_hovered="#80838D",  # slate-10
    secondary_alternative_color_pressed="#60646C",  # slate-11
    secondary_alternative_color_disabled="#CDCED6",  # slate-7
    # Status: Radix green, cyan, amber, red (light scales)
    status_color_success="#30A46C",  # green-9
    status_color_success_hovered="#2B9A66",  # green-10
    status_color_success_pressed="#218358",  # green-11
    status_color_success_disabled="#D6F1DF",  # green-4
    status_color_info="#00A2C7",  # cyan-9
    status_color_info_hovered="#0797B9",  # cyan-10
    status_color_info_pressed="#107D98",  # cyan-11
    status_color_info_disabled="#C7EAF5",  # cyan-4
    status_color_warning="#FFC53D",  # amber-9
    status_color_warning_hovered="#FFBA18",  # amber-10
    status_color_warning_pressed="#AB6400",  # amber-11
    status_color_warning_disabled="#FEEFD8",  # amber-4
    status_color_error="#E5484D",  # red-9
    status_color_error_hovered="#DC3E42",  # red-10
    status_color_error_pressed="#CE2C31",  # red-11
    status_color_error_disabled="#FFDCD9",  # red-4
    status_color_foreground="#FFFFFF",
    status_color_foreground_hovered="#FFFFFF",
    status_color_foreground_pressed="#FFFFFF",
    status_color_foreground_disabled="#99FFFFFF",
    # Shadows
    shadow_color1="#20000000",
    shadow_color2="#40000000",
    shadow_color3="#60000000",
    # Borders: slate-6/7/8/5
    border_color="#D9D9E0",  # slate-6
    border_color_hovered="#CDCED6",  # slate-7
    border_color_pressed="#B9BBC6",  # slate-8
    border_color_disabled="#E0E1E6",  # slate-5
    # Semi-transparent overlays
    semi_transparent_color1="#00000000",
    semi_transparent_color2="#19000000",
    semi_transparent_color3="#21000000",
    semi_transparent_color4="#28000000",
    # Radii: Radix default = 6px medium
    border_radius=6.0,
    check_box_border_radius=4.0,
    menu_item_border_radius=4.0,
    menu_bar_item_border_radius=2.0,
)

RADIX_INDIGO_DARK = Theme(
    meta=ThemeMeta(name="Radix Indigo Dark", author="Radix UI"),
    # Backgrounds: dark slate-1 through slate-4, slate-8 for workspace/tabbar
    background_color_main1="#111113",  # slate-1
    background_color_main2="#18191B",  # slate-2
    background_color_main3="#212225",  # slate-3
    background_color_main4="#272A2D",  # slate-4
    background_color_workspace="#2E3135",  # slate-5
    background_color_tab_bar="#2E3135",  # slate-5
    # Neutrals: slate-4/5/6/3
    neutral_color="#272A2D",  # slate-4
    neutral_color_hovered="#2E3135",  # slate-5
    neutral_color_pressed="#363A3F",  # slate-6
    neutral_color_disabled="#212225",  # slate-3
    # Focus: indigo-7 @ ~40% alpha
    focus_color="#663A4F97",
    # Primary: indigo-9/10/11, indigo-5 disabled
    primary_color="#3E63DD",  # indigo-9
    primary_color_hovered="#5472E4",  # indigo-10
    primary_color_pressed="#849DFF",  # indigo-11
    primary_color_disabled="#253974",  # indigo-5
    primary_color_foreground="#FFFFFF",
    primary_color_foreground_hovered="#FFFFFF",
    primary_color_foreground_pressed="#FFFFFF",
    primary_color_foreground_disabled="#43484E",  # slate-7
    # Primary alternative: indigo deeper/lighter shades
    primary_alternative_color="#435DB1",  # indigo-8
    primary_alternative_color_hovered="#3A4F97",  # indigo-7
    primary_alternative_color_pressed="#304384",  # indigo-6
    primary_alternative_color_disabled="#1D2E62",  # indigo-4
    # Secondary: slate-12/11/10, slate-7 disabled
    secondary_color="#EDEEF0",  # slate-12
    secondary_color_hovered="#B0B4BA",  # slate-11
    secondary_color_pressed="#777B84",  # slate-10
    secondary_color_disabled="#5A6169",  # slate-8
    secondary_color_foreground="#111113",  # slate-1
    secondary_color_foreground_hovered="#111113",
    secondary_color_foreground_pressed="#18191B",  # slate-2
    secondary_color_foreground_disabled="#363A3F",  # slate-6
    # Secondary alternative: slate mid-range
    secondary_alternative_color="#696E77",  # slate-9
    secondary_alternative_color_hovered="#777B84",  # slate-10
    secondary_alternative_color_pressed="#B0B4BA",  # slate-11
    secondary_alternative_color_disabled="#43484E",  # slate-7
    # Status: Radix dark-mode scales
    status_color_success="#30A46C",  # green-9
    status_color_success_hovered="#3CB179",  # green-10
    status_color_success_pressed="#4CC38A",  # green-11
    status_color_success_disabled="#1B3A2D",  # green-4 (dark)
    status_color_info="#00A2C7",  # cyan-9
    status_color_info_hovered="#23AFD0",  # cyan-10
    status_color_info_pressed="#4CCCE6",  # cyan-11
    status_color_info_disabled="#142D37",  # cyan-4 (dark)
    status_color_warning="#FFC53D",  # amber-9
    status_color_warning_hovered="#FFD60A",  # amber-10
    status_color_warning_pressed="#FFCA16",  # amber-11
    status_color_warning_disabled="#3F2200",  # amber-4 (dark)
    status_color_error="#E5484D",  # red-9
    status_color_error_hovered="#EC5D5E",  # red-10
    status_color_error_pressed="#FF9592",  # red-11
    status_color_error_disabled="#3C1618",  # red-4 (dark)
    status_color_foreground="#FFFFFF",
    status_color_foreground_hovered="#FFFFFF",
    status_color_foreground_pressed="#FFFFFF",
    status_color_foreground_disabled="#99FFFFFF",
    # Shadows: stronger in dark mode
    shadow_color1="#30000000",
    shadow_color2="#50000000",
    shadow_color3="#70000000",
    # Borders: slate-6/7/8/5
    border_color="#363A3F",  # slate-6
    border_color_hovered="#43484E",  # slate-7
    border_color_pressed="#5A6169",  # slate-8
    border_color_disabled="#2E3135",  # slate-5
    # Semi-transparent overlays (white-based for dark themes)
    semi_transparent_color1="#00FFFFFF",
    semi_transparent_color2="#19FFFFFF",
    semi_transparent_color3="#21FFFFFF",
    semi_transparent_color4="#28FFFFFF",
    # Radii: same as light
    border_radius=6.0,
    check_box_border_radius=4.0,
    menu_item_border_radius=4.0,
    menu_bar_item_border_radius=2.0,
)


def _qt_core() -> Any:
    for framework in {"PyQt6", "PySide6"}:
        if framework in sys.modules:
            mod = sys.modules[framework]
            return mod.QtCore
    for framework in {"PyQt6", "PySide6"}:
        try:
            mod = __import__(framework)
            return mod.QtCore
        except ImportError:
            continue
    raise ImportError("Neither PyQt6 nor PySide6 is installed.")


if __name__ == "__main__":
    from PyQt6 import QtWidgets
    from PyQt6.QtCore import Qt
    from PyQt6Qlementine import QlementineStyle

    app = QtWidgets.QApplication([])

    style = QlementineStyle(app)
    app.setStyle(style)

    theme = RADIX_INDIGO_DARK
    style.setTheme(theme.toQlementine())

    sample_widget = QtWidgets.QWidget()
    sample_widget.setWindowTitle("Sample Widget")
    layout = QtWidgets.QVBoxLayout(sample_widget)
    button = QtWidgets.QPushButton("Sample Button")
    layout.addWidget(button)
    combo = QtWidgets.QComboBox()
    combo.addItems(["Option 1", "Option 2", "Option 3"])
    layout.addWidget(combo)
    slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
    layout.addWidget(slider)
    check_box = QtWidgets.QCheckBox("Sample Check Box")
    layout.addWidget(check_box)
    int_spin = QtWidgets.QSpinBox()
    layout.addWidget(int_spin)
    float_spin = QtWidgets.QDoubleSpinBox()
    layout.addWidget(float_spin)
    dial = QtWidgets.QDial()
    dial.setNotchesVisible(True)
    layout.addWidget(dial)

    sample_widget.resize(400, 300)
    sample_widget.show()
    app.exec()
