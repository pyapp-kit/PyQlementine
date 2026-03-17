"""Pure-Python dataclasses mirroring oclero::qlementine::Theme."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    # QSize accepts a tuple of 2 integers (width, height)
    QSizeLike: TypeAlias = tuple[int, int]

    # QColor accepts:
    # a single integer (0xRRGGBB or 0xAARRGGBB)
    #     however, because it's hard to disambiguate between 0x00RRGGBB and 0xRRGGBB
    #     we will only accept 0xRRGGBB for the integer form, and you must use a tuple
    #     for the 0xAARRGGBB form (e.g. (0xRR, 0xGG, 0xBB, 0xAA))
    # a string (e.g. "#RRGGBB" or "#AARRGGBB" or an svg color name like "red")
    # a tuple of 3 8-bit integers (R, G, B)
    # a tuple of 4 8-bit integers (R, G, B, A)
    QColorLike: TypeAlias = int | str | tuple[int, int, int] | tuple[int, int, int, int]

    # QFont accepts:
    FamilyOrFamilies: TypeAlias = str | list[str]
    PointSize: TypeAlias = int
    Weight: TypeAlias = int
    Italic: TypeAlias = bool
    QFontLike: TypeAlias = (
        FamilyOrFamilies
        | tuple[FamilyOrFamilies]
        | tuple[FamilyOrFamilies, PointSize]
        | tuple[FamilyOrFamilies, PointSize, Weight]
        | tuple[FamilyOrFamilies, PointSize, Weight, Italic]
    )


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
    background_color_main_transparent: QColorLike = "#00FAFAFA"

    background_color_workspace: QColorLike = "#B7B7B7"
    background_color_tab_bar: QColorLike = "#B7B7B7"

    neutral_color: QColorLike = "#E1E1E1"
    neutral_color_hovered: QColorLike = "#DADADA"
    neutral_color_pressed: QColorLike = "#D2D2D2"
    neutral_color_disabled: QColorLike = "#EEEEEE"
    neutral_color_transparent: QColorLike = "#00E1E1E1"

    focus_color: QColorLike = "#6640A9FF"

    primary_color: QColorLike = "#1890FF"
    primary_color_hovered: QColorLike = "#2C9DFF"
    primary_color_pressed: QColorLike = "#40A9FF"
    primary_color_disabled: QColorLike = "#D1E9FF"
    primary_color_transparent: QColorLike = "#001890FF"

    primary_color_foreground: QColorLike = "#FFFFFF"
    primary_color_foreground_hovered: QColorLike = "#FFFFFF"
    primary_color_foreground_pressed: QColorLike = "#FFFFFF"
    primary_color_foreground_disabled: QColorLike = "#ECF6FF"
    primary_color_foreground_transparent: QColorLike = "#00FFFFFF"

    primary_alternative_color: QColorLike = "#106EF9"
    primary_alternative_color_hovered: QColorLike = "#107BFD"
    primary_alternative_color_pressed: QColorLike = "#108BFD"
    primary_alternative_color_disabled: QColorLike = "#A9D6FF"
    primary_alternative_color_transparent: QColorLike = "#001875FF"

    secondary_color: QColorLike = "#404040"
    secondary_color_hovered: QColorLike = "#333333"
    secondary_color_pressed: QColorLike = "#262626"
    secondary_color_disabled: QColorLike = "#D4D4D4"
    secondary_color_transparent: QColorLike = "#00404040"

    secondary_color_foreground: QColorLike = "#FFFFFF"
    secondary_color_foreground_hovered: QColorLike = "#FFFFFF"
    secondary_color_foreground_pressed: QColorLike = "#FFFFFF"
    secondary_color_foreground_disabled: QColorLike = "#EDEDED"
    secondary_color_foreground_transparent: QColorLike = "#00FFFFFF"

    secondary_alternative_color: QColorLike = "#909090"
    secondary_alternative_color_hovered: QColorLike = "#747474"
    secondary_alternative_color_pressed: QColorLike = "#828282"
    secondary_alternative_color_disabled: QColorLike = "#C3C3C3"
    secondary_alternative_color_transparent: QColorLike = "#00909090"

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
    shadow_color_transparent: QColorLike = "#00000000"

    border_color: QColorLike = "#D3D3D3"
    border_color_hovered: QColorLike = "#B3B3B3"
    border_color_pressed: QColorLike = "#A3A3A3"
    border_color_disabled: QColorLike = "#E9E9E9"
    border_color_transparent: QColorLike = "#00D3D3D3"

    semi_transparent_color1: QColorLike = "#00000000"
    semi_transparent_color2: QColorLike = "#19000000"
    semi_transparent_color3: QColorLike = "#21000000"
    semi_transparent_color4: QColorLike = "#28000000"
    semi_transparent_color_transparent: QColorLike = "#00000000"

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

    icon_size: QSizeLike = (16, 16)
    icon_size_medium: QSizeLike = (24, 24)
    icon_size_large: QSizeLike = (24, 24)
    icon_size_extra_small: QSizeLike = (12, 12)

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

    font_regular: QFontLike | None = None
    font_bold: QFontLike | None = None
    font_h1: QFontLike | None = None
    font_h2: QFontLike | None = None
    font_h3: QFontLike | None = None
    font_h4: QFontLike | None = None
    font_h5: QFontLike | None = None
    font_caption: QFontLike | None = None
    font_monospace: QFontLike | None = None

    palette: Any = None  # TODO: QPalette
