%Module(name=PyQt6Qlementine._qlementine, call_super_init=True, keyword_arguments="Optional", use_limited_api=True)
%HideNamespace(name=oclero)
%HideNamespace(name=oclero::qlementine)

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip
%DefaultSupertype PyQt6.sip.simplewrapper

%ModuleHeaderCode
#include <QPainterPath>
#include <oclero/qlementine/utils/BadgeUtils.hpp>
#include <oclero/qlementine/utils/ColorUtils.hpp>
#include <oclero/qlementine/utils/FontUtils.hpp>
#include <oclero/qlementine/utils/GeometryUtils.hpp>
#include <oclero/qlementine/utils/IconUtils.hpp>
#include <oclero/qlementine/utils/ImageUtils.hpp>
#include <oclero/qlementine/utils/LayoutUtils.hpp>
#include <oclero/qlementine/utils/MenuUtils.hpp>
#include <oclero/qlementine/utils/PrimitiveUtils.hpp>
#include <oclero/qlementine/utils/StateUtils.hpp>
#include <oclero/qlementine/utils/StyleUtils.hpp>
#include <oclero/qlementine/utils/WidgetUtils.hpp>
%End

// Classes, enums, widgets
%Include Common.sip
%Include RadiusesF.sip
%Include Theme.sip
%Include IconTheme.sip
%Include QlementineStyle.sip
%Include ThemeManager.sip
%Include RoundedFocusFrame.sip
%Include AbstractItemListWidget.sip
%Include NavigationBar.sip
%Include SegmentedControl.sip
%Include Switch.sip
%Include Label.sip
%Include LineEdit.sip
%Include PlainTextEdit.sip
%Include LoadingSpinner.sip
%Include IconWidget.sip
%Include StatusBadgeWidget.sip
%Include Expander.sip
%Include ActionButton.sip
%Include CommandLinkButton.sip
%Include AboutDialog.sip
%Include NotificationBadge.sip
%Include ColorButton.sip
%Include ColorEditor.sip
%Include Popover.sip
%Include PopoverButton.sip
%Include Menu.sip

// Utility free functions
%Include BadgeUtils.sip
%Include ColorUtils.sip
%Include FontUtils.sip
%Include GeometryUtils.sip
%Include IconUtils.sip
%Include ImageUtils.sip
%Include LayoutUtils.sip
%Include MenuUtils.sip
%Include PrimitiveUtils.sip
%Include StateUtils.sip
%Include StyleUtils.sip
%Include WidgetUtils.sip
