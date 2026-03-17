%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CDockAreaWidget : QFrame
{
%TypeHeaderCode
#include <DockAreaWidget.h>
%End

protected:
  void insertDockWidget(int index, CDockWidget* DockWidget /Transfer/, bool Activate = true);
  void addDockWidget(CDockWidget* DockWidget /Transfer/);
  void removeDockWidget(CDockWidget* DockWidget) /TransferBack/;
  void toggleDockWidgetView(CDockWidget* DockWidget, bool Open);
  CDockWidget* nextOpenDockWidget(CDockWidget* DockWidget) const;
  int index(CDockWidget* DockWidget);
  void hideAreaWithNoVisibleContent();
  void updateTitleBarVisibility();
  void internalSetCurrentDockWidget(CDockWidget* DockWidget /Transfer/);
  void markTitleBarMenuOutdated();
  void updateTitleBarButtonVisibility(bool IsTopLevel) const;

protected slots:
  void toggleView(bool Open);

public:
  enum eDockAreaFlag
  {
    HideSingleWidgetTitleBar,
    DefaultFlags
  };
  typedef QFlags<ads::CDockAreaWidget::eDockAreaFlag> DockAreaFlags;

  CDockAreaWidget(CDockManager* DockManager /TransferThis/, CDockContainerWidget* parent /TransferThis/);
  virtual ~CDockAreaWidget();
  CDockManager* dockManager() const;
  CDockContainerWidget* dockContainer() const;
  CAutoHideDockContainer* autoHideDockContainer() const;
  CDockSplitter* parentSplitter() const;
  bool isAutoHide() const;
  void setAutoHideDockContainer(CAutoHideDockContainer*);
  virtual QSize minimumSizeHint() const;
  QRect titleBarGeometry() const;
  QRect contentAreaGeometry() const;
  int dockWidgetsCount() const;
  QList<ads::CDockWidget*> dockWidgets() const;
  int openDockWidgetsCount() const;
  QList<ads::CDockWidget*> openedDockWidgets() const;
  CDockWidget* dockWidget(int Index) const;
  int currentIndex() const;
  int indexOfFirstOpenDockWidget() const;
  CDockWidget* currentDockWidget() const;
  void setCurrentDockWidget(CDockWidget* DockWidget);
  void saveState(QXmlStreamWriter& Stream) const;
  static bool restoreState(CDockingStateReader& Stream, CDockAreaWidget*& CreatedWidget, bool Testing, CDockContainerWidget* ParentContainer);
  CDockWidget::DockWidgetFeatures features(eBitwiseOperator Mode = ads::BitwiseAnd) const;
  QAbstractButton* titleBarButton(TitleBarButton which) const;
  virtual void setVisible(bool Visible);

  void setAllowedAreas(DockWidgetAreas areas);
  DockWidgetAreas allowedAreas() const;
  CDockAreaTitleBar* titleBar() const;

  DockAreaFlags dockAreaFlags() const;
  void setDockAreaFlags(DockAreaFlags Flags);
  void setDockAreaFlag(eDockAreaFlag Flag, bool On);

  bool isCentralWidgetArea() const;
  bool containsCentralWidget() const;
  bool isTopLevelArea() const;

public slots:
  void setCurrentIndex(int index);
  void closeArea();
  void setAutoHide(bool Enable, SideBarLocation Location = ads::SideBarNone, int TabIndex = -1);
  void toggleAutoHide(SideBarLocation Location = ads::SideBarNone);
  void closeOtherAreas();
  void setFloating();

signals:
  void tabBarClicked(int index);
  void currentChanging(int index);
  void currentChanged(int index);
  void viewToggled(bool Open);
};

};
