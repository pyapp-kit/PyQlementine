namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/StyleUtils.hpp>
%End

bool shouldHaveHoverEvents(const QWidget* w);
bool shouldHaveMouseTracking(const QWidget* w);
bool shouldHaveBoldFont(const QWidget* w);
bool shouldHaveExternalFocusFrame(const QWidget* w);
bool shouldHaveTabFocus(const QWidget* w);
bool shouldNotBeVerticallyCompressed(const QWidget* w);
bool shouldNotHaveWheelEvents(const QWidget* w);
int getTabIndex(const QStyleOptionTab* optTab, const QWidget* parentWidget);
int getTabCount(const QWidget* parentWidget);

};
};
