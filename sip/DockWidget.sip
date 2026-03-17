%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CDockWidget : QFrame
{
%TypeHeaderCode
#include <DockWidget.h>
%End

protected:
  void setDockManager(CDockManager* DockManager /Transfer/ );
  void setDockArea(CDockAreaWidget* DockArea /Transfer/ );
  void setToggleViewActionChecked(bool Checked);
  void saveState(QXmlStreamWriter& Stream) const;
  void flagAsUnassigned();
  static void emitTopLevelEventForWidget(CDockWidget* TopLevelDockWidget, bool Floating);
  void emitTopLevelChanged(bool Floating);
  void setClosedState(bool Closed);
  void toggleViewInternal(bool Open);
  bool closeDockWidgetInternal(bool ForceClose = false);

public:
  enum DockWidgetFeature
  {
    DockWidgetClosable,
    DockWidgetMovable,
    DockWidgetFloatable,
    DockWidgetDeleteOnClose,
    CustomCloseHandling,
    DockWidgetFocusable,
    DockWidgetForceCloseWithArea,
    NoTab,
    DeleteContentOnClose,
    DockWidgetPinnable,
    DefaultDockWidgetFeatures,
    AllDockWidgetFeatures,
    DockWidgetAlwaysCloseAndDelete,
    GloballyLockableFeatures,
    NoDockWidgetFeatures
  };
  typedef QFlags<ads::CDockWidget::DockWidgetFeature> DockWidgetFeatures;

  enum eState
  {
    StateHidden,
    StateDocked,
    StateFloating
  };

  enum eToolBarStyleSource
  {
    ToolBarStyleFromDockManager,
    ToolBarStyleFromDockWidget
  };

  enum eInsertMode
  {
    AutoScrollArea,
    ForceScrollArea,
    ForceNoScrollArea
  };
  
  enum eMinimumSizeHintMode
  {
    MinimumSizeHintFromDockWidget,
    MinimumSizeHintFromContent,
    MinimumSizeHintFromDockWidgetMinimumSize,
    MinimumSizeHintFromContentMinimumSize,
  };

  enum eToggleViewActionMode
  {
    ActionModeToggle,
    ActionModeShow
  };


  explicit CDockWidget(const QString &title, QWidget* parent /TransferThis/ = nullptr);
  CDockWidget(CDockManager *manager /Transfer/, const QString &title, QWidget* parent /TransferThis/ = nullptr);
  virtual ~CDockWidget();
  virtual QSize minimumSizeHint() const;
  void setWidget(QWidget* widget /Transfer/, CDockWidget::eInsertMode InsertMode = AutoScrollArea);
  QWidget* takeWidget() /TransferBack/;
  QWidget* widget() const;
  CDockWidgetTab* tabWidget() const;
  void setFeatures(CDockWidget::DockWidgetFeatures features);
  void setFeature(CDockWidget::DockWidgetFeature flag, bool on);
  CDockWidget::DockWidgetFeatures features() const;
  CDockManager* dockManager() const;
  CDockContainerWidget* dockContainer() const;
  CFloatingDockContainer* floatingDockContainer() const;
  CDockAreaWidget* dockAreaWidget() const;
  CAutoHideTab* sideTabWidget() const;
  void setSideTabWidget(CAutoHideTab* SideTab /Transfer/) const;
  bool isAutoHide() const;
  CAutoHideDockContainer* autoHideDockContainer() const;
  SideBarLocation autoHideLocation() const;
  bool isFloating() const;
  bool isInFloatingContainer() const;
  bool isClosed() const;
  QAction* toggleViewAction() const;
  void setToggleViewAction(QAction* action /Transfer/);
  void setToggleViewActionMode(CDockWidget::eToggleViewActionMode Mode);
  void setMinimumSizeHintMode(CDockWidget::eMinimumSizeHintMode Mode);
  CDockWidget::eMinimumSizeHintMode minimumSizeHintMode() const;
  bool isCentralWidget() const;
  void setIcon(const QIcon& Icon);
  QIcon icon() const;
  QToolBar* toolBar() const;
  QToolBar* createDefaultToolBar();
  void setToolBar(QToolBar* ToolBar /Transfer/);
  void setToolBarStyleSource(eToolBarStyleSource Source);
  eToolBarStyleSource toolBarStyleSource() const;
  void setToolBarStyle(Qt::ToolButtonStyle Style, CDockWidget::eState State);
  Qt::ToolButtonStyle toolBarStyle(CDockWidget::eState State) const;
  void setToolBarIconSize(const QSize& IconSize, CDockWidget::eState State);
  QSize toolBarIconSize(eState State) const;
  void setTitleBarActions(QList<QAction*> actions);
  virtual QList<QAction*> titleBarActions() const;

  void setTabToolTip(const QString &text);
  bool isFullScreen() const;
  bool isTabbed() const;
  bool isCurrentTab() const;

public:
  virtual bool event(QEvent *e);

public slots:
  void toggleView(bool Open = true);
  void setAsCurrentTab();
  void raise();
  void setFloating();
  void deleteDockWidget();
  void closeDockWidget();
  void requestCloseDockWidget();
  void showFullScreen();
  void showNormal();
  void setAutoHide(bool Enable, SideBarLocation Location = ads::SideBarNone, int TabIndex = -1);
  void toggleAutoHide(SideBarLocation Location = ads::SideBarNone);

signals:
  void viewToggled(bool Open);
  void closed();
  void titleChanged(const QString& Title);
  void topLevelChanged(bool topLevel);
  void closeRequested();
  void visibilityChanged(bool visible);
  void featuresChanged(CDockWidget::DockWidgetFeatures features);
};

};
