%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CDockFocusController : QObject
{
%TypeHeaderCode
#include <DockFocusController.h>
%End
    
public:
  CDockFocusController(CDockManager* DockManager);
  virtual ~CDockFocusController();

  void notifyWidgetOrAreaRelocation(QWidget* RelocatedWidget);
  void notifyFloatingWidgetDrop(CFloatingDockContainer* FloatingWidget);
  CDockWidget* focusedDockWidget() const;
  CDockAreaWidget* focusedDockArea() const;
  void setDockWidgetTabFocused(CDockWidgetTab* Tab);
  void clearDockWidgetFocus(CDockWidget* dockWidget);
  void setDockWidgetTabPressed(bool Value);

public slots:
  void setDockWidgetFocused(CDockWidget* focusedNow);    
};

};
