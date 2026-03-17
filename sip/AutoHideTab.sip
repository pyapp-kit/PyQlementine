%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CAutoHideTab : CPushButton
{

%TypeHeaderCode
#include <AutoHideTab.h>
%End

protected:
  void setSideBar(CAutoHideSideBar *SideTabBar /Transfer/);
  void removeFromSideBar();
  virtual bool event(QEvent* event);
  virtual void contextMenuEvent(QContextMenuEvent* ev);
  virtual void mousePressEvent(QMouseEvent* ev);
  virtual void mouseReleaseEvent(QMouseEvent* ev);
  virtual void mouseMoveEvent(QMouseEvent* ev);
  virtual void dragEnterEvent(QDragEnterEvent* ev);
  virtual void dragLeaveEvent(QDragLeaveEvent* ev);

public:
  CAutoHideTab(QWidget* parent /TransferThis/ = nullptr);
  virtual ~CAutoHideTab();
  void updateStyle();
  SideBarLocation sideBarLocation() const;
  void setOrientation(Qt::Orientation Orientation);
  Qt::Orientation orientation() const;
  bool isActiveTab() const;
  CDockWidget* dockWidget() const;
  void setDockWidget(CDockWidget* DockWidget);
  bool iconOnly() const;
  CAutoHideSideBar* sideBar() const;
  int tabIndex() const;

public slots:
  void setDockWidgetFloating();
  void unpinDockWidget();
  void requestCloseDockWidget();
};

};
