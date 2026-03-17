namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/Common.hpp>
#include <oclero/qlementine/utils/ImageUtils.hpp>
#include <oclero/qlementine/utils/BadgeUtils.hpp>
%End

enum class ColorRole
{
    Primary,
    Secondary,
};

enum class MouseState
{
    Transparent,
    Normal,
    Hovered,
    Pressed,
    Disabled,
};

enum class CheckState
{
    NotChecked,
    Checked,
    Indeterminate,
};

enum class FocusState
{
    NotFocused,
    Focused,
};

enum class ActiveState
{
    NotActive,
    Active,
};

enum class SelectionState
{
    NotSelected,
    Selected,
};

enum class AlternateState
{
    NotAlternate,
    Alternate,
};

enum class DefaultState
{
    NotDefault,
    Default,
};

enum class Status
{
    Default,
    Info,
    Success,
    Warning,
    Error,
};

enum class TextRole
{
    Caption,
    Default,
    H1,
    H2,
    H3,
    H4,
    H5,
};

enum class ColorMode
{
    RGB,
    RGBA,
};

enum class AutoIconColor
{
    None,
    ForegroundColor,
    TextColor,
};

enum class StatusBadge
{
    Success,
    Info,
    Warning,
    Error,
};

enum class StatusBadgeSize
{
    Small,
    Medium,
};

};
};
