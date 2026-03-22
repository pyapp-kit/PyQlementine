namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/StateUtils.hpp>
%End

MouseState getMouseState(QStyle::State state);
MouseState getMouseState(bool pressed, bool hovered, bool enabled);
MouseState getToolButtonMouseState(QStyle::State state);
MouseState getMenuItemMouseState(QStyle::State state);
MouseState getComboBoxItemMouseState(QStyle::State state);
MouseState getTabItemMouseState(QStyle::State state, bool tabIsHovered);
ColorRole getColorRole(QStyle::State state, bool isDefault);
ColorRole getColorRole(bool checked, bool isDefault);
ColorRole getColorRole(CheckState checked);
MouseState getSliderHandleState(QStyle::State state, QStyle::SubControls activeSubControls);
MouseState getScrollBarHandleState(QStyle::State state, QStyle::SubControls activeSubControls);
FocusState getFocusState(QStyle::State state);
FocusState getFocusState(bool focused);
CheckState getCheckState(QStyle::State state);
CheckState getCheckState(Qt::CheckState state);
CheckState getCheckState(bool checked);
ActiveState getActiveState(QStyle::State state);
SelectionState getSelectionState(QStyle::State state);
AlternateState getAlternateState(QStyleOptionViewItem::ViewItemFeatures state);
QStyle::State getState(bool enabled, bool hover, bool pressed);
QIcon::Mode getIconMode(MouseState mouse);
QIcon::State getIconState(CheckState checked);
QPalette::ColorGroup getPaletteColorGroup(QStyle::State state);
QPalette::ColorGroup getPaletteColorGroup(MouseState mouse);

QString mouseStateToString(MouseState state);
QString focusStateToString(FocusState state);
QString activeStateToString(ActiveState state);
QString selectionStateToString(SelectionState state);
QString checkStateToString(CheckState state);
QString printState(QStyle::State state);

};
};
