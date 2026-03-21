#ifndef PYSIDE6_QLEMENTINE_BINDINGS_H
#define PYSIDE6_QLEMENTINE_BINDINGS_H

// Qt types needed by shiboken to resolve all QStyle virtual overload signatures
#include <QApplication>

// Used by setIconPathGetter glue code
#include <functional>
#include <memory>

// Core types
#include <oclero/qlementine/Common.hpp>
#include <oclero/qlementine/utils/RadiusesF.hpp>
#include <oclero/qlementine/utils/IconUtils.hpp>
#include <oclero/qlementine/utils/ImageUtils.hpp>

// Style
#include <oclero/qlementine/style/Theme.hpp>
#include <oclero/qlementine/style/QlementineStyle.hpp>
#include <oclero/qlementine/style/ThemeManager.hpp>

// Widgets
#include <oclero/qlementine/widgets/AbstractItemListWidget.hpp>
#include <oclero/qlementine/widgets/AboutDialog.hpp>
#include <oclero/qlementine/widgets/ActionButton.hpp>
#include <oclero/qlementine/widgets/ColorButton.hpp>
#include <oclero/qlementine/widgets/ColorEditor.hpp>
#include <oclero/qlementine/widgets/CommandLinkButton.hpp>
#include <oclero/qlementine/widgets/Expander.hpp>
#include <oclero/qlementine/widgets/IconWidget.hpp>
#include <oclero/qlementine/widgets/Label.hpp>
#include <oclero/qlementine/widgets/LineEdit.hpp>
#include <oclero/qlementine/widgets/LoadingSpinner.hpp>
#include <oclero/qlementine/widgets/Menu.hpp>
#include <oclero/qlementine/widgets/NavigationBar.hpp>
#include <oclero/qlementine/widgets/NotificationBadge.hpp>
#include <oclero/qlementine/widgets/PlainTextEdit.hpp>
#include <oclero/qlementine/widgets/Popover.hpp>
#include <oclero/qlementine/widgets/PopoverButton.hpp>
#include <oclero/qlementine/widgets/RoundedFocusFrame.hpp>
#include <oclero/qlementine/widgets/SegmentedControl.hpp>
#include <oclero/qlementine/widgets/StatusBadgeWidget.hpp>
#include <oclero/qlementine/widgets/Switch.hpp>

#endif
