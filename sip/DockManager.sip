%Import QtWidgets/QtWidgetsmod.sip

%MappedType QMap<QString, ads::CDockWidget*> /TypeHint="Dict[QString, CDockWidget*]", TypeHintValue="{}"/
{
%TypeHeaderCode
#include <qmap.h>
%End

%ConvertFromTypeCode
  PyObject *d = PyDict_New();

  if (!d)
    return 0;
  
  QMap<QString, ads::CDockWidget*>::const_iterator it = sipCpp->constBegin();
  QMap<QString, ads::CDockWidget*>::const_iterator end = sipCpp->constEnd();

  while (it != end)
  {
    QString *k = new QString(it.key());
    PyObject *kobj = sipConvertFromType(k, sipType_QString, sipTransferObj);

    if (!kobj)
    {
      delete k;
      Py_DECREF(d);

      return 0;
    }

    PyObject *vobj = sipConvertFromType(it.value(), sipType_ads_CDockWidget, sipTransferObj);

    if (!vobj)
    {
      Py_DECREF(kobj);
      Py_DECREF(d);

      return 0;
    }

    int rc = PyDict_SetItem(d, kobj, vobj);

    Py_DECREF(vobj);
    Py_DECREF(kobj);

    if (rc < 0)
    {
      Py_DECREF(d);

      return 0;
    }

    ++it;
  }
  
  return d;
%End

%ConvertToTypeCode
  if (!sipIsErr)
    return PyDict_Check(sipPy);

  QMap<QString, ads::CDockWidget*> *qm = new QMap<QString, ads::CDockWidget*>;
  
  Py_ssize_t pos = 0;
  PyObject *kobj, *vobj;
  while (PyDict_Next(sipPy, &pos, &kobj, &vobj))
  {
    int kstate;
    QString *k = reinterpret_cast<QString *>(sipForceConvertToType(kobj, sipType_QString, sipTransferObj, SIP_NOT_NONE, &kstate, sipIsErr));

    if (*sipIsErr)
    {
        PyErr_Format(PyExc_TypeError, "a dict key has type '%s' but '_TYPE1_' is expected", sipPyTypeName(Py_TYPE(kobj)));
        delete qm;
        return 0;
    }

    int vstate;
    ads::CDockWidget *v = reinterpret_cast<ads::CDockWidget *>(sipForceConvertToType(vobj, sipType_ads_CDockWidget, sipTransferObj, SIP_NOT_NONE, &vstate, sipIsErr));

    if (*sipIsErr)
    {
        PyErr_Format(PyExc_TypeError, "a dict value has type '%s' but '_TYPE2_' is expected", sipPyTypeName(Py_TYPE(vobj)));
        sipReleaseType(k, sipType_QString, kstate);
        delete qm;

        return 0;
    }

    qm->insert(*k, v);

    sipReleaseType(v, sipType_ads_CDockWidget, vstate);
    sipReleaseType(k, sipType_QString, kstate);
  }

  *sipCppPtr = qm;

  return sipGetState(sipTransferObj);
%End
};

namespace ads
{

class CDockManager : CDockContainerWidget
{

%TypeHeaderCode
#include <DockManager.h>
%End

protected:
  void registerFloatingWidget(CFloatingDockContainer* FloatingWidget /Transfer/);
  void removeFloatingWidget(CFloatingDockContainer* FloatingWidget) /TransferBack/;
  void registerDockContainer(CDockContainerWidget* DockContainer /Transfer/);
  void removeDockContainer(CDockContainerWidget* DockContainer /TransferBack/);
  CDockOverlay* containerOverlay() const;
  CDockOverlay* dockAreaOverlay() const;
  void notifyWidgetOrAreaRelocation(QWidget* RelocatedWidget);
  void notifyFloatingWidgetDrop(CFloatingDockContainer* FloatingWidget);

  virtual void showEvent(QShowEvent *event);

public:
  enum eViewMenuInsertionOrder
  {
    MenuSortedByInsertion,
    MenuAlphabeticallySorted
  };

  enum eConfigFlag
  {
    ActiveTabHasCloseButton,
    DockAreaHasCloseButton,
    DockAreaCloseButtonClosesTab,
    OpaqueSplitterResize,
    XmlAutoFormattingEnabled,
    XmlCompressionEnabled,
    TabCloseButtonIsToolButton,
    AllTabsHaveCloseButton,
    RetainTabSizeWhenCloseButtonHidden,
    DragPreviewIsDynamic,
    DragPreviewShowsContentPixmap,
    DragPreviewHasWindowFrame,
    AlwaysShowTabs,
    DockAreaHasUndockButton,
    DockAreaHasTabsMenuButton,
    DockAreaHideDisabledButtons,
    DockAreaDynamicTabsMenuButtonVisibility,
    FloatingContainerHasWidgetTitle,
    FloatingContainerHasWidgetIcon,
    HideSingleCentralWidgetTitleBar,
    FocusHighlighting,
    EqualSplitOnInsertion,
    FloatingContainerForceNativeTitleBar,
    FloatingContainerForceQWidgetTitleBar,
    MiddleMouseButtonClosesTab,
    DisableTabTextEliding,
    ShowTabTextOnlyForActiveTab,
    DoubleClickUndocksWidget,
    TabsAtBottom,
    DefaultDockAreaButtons,
    DefaultBaseConfig,
    DefaultOpaqueConfig,
    DefaultNonOpaqueConfig,
    NonOpaqueWithWindowFrame,
  };
  typedef QFlags<ads::CDockManager::eConfigFlag> ConfigFlags;

  enum eAutoHideFlag
  {
    AutoHideFeatureEnabled,
    DockAreaHasAutoHideButton,
    AutoHideButtonTogglesArea,
    AutoHideButtonCheckable,
    AutoHideSideBarsIconOnly,
    AutoHideShowOnMouseOver,
    AutoHideCloseButtonCollapsesDock,
    AutoHideHasCloseButton,
    AutoHideHasMinimizeButton,
    AutoHideOpenOnDragHover,
    AutoHideCloseOnOutsideMouseClick,
    DefaultAutoHideConfig,
  };
  typedef QFlags<ads::CDockManager::eAutoHideFlag> AutoHideFlags;

  enum eConfigParam
	{
    AutoHideOpenOnDragHoverDelay_ms,
    ConfigParamCount,
	};

  CDockManager(QWidget* parent /TransferThis/ = nullptr);
  virtual ~CDockManager();
  CDockWidget* createDockWidget(const QString& title, QWidget* parent /TransferThis/ = nullptr) /Factory/;
  CDockComponentsFactory* componentsFactory() const;
%MethodCode
    sipRes = sipCpp->componentsFactory().data();
%End
  void setComponentsFactory(CDockComponentsFactory* Factory /Transfer/);
  // void setComponentsFactory(QSharedPointer<CDockComponentsFactory>); // not necessary
  static CDockManager::ConfigFlags configFlags();
  static void setConfigFlags(const CDockManager::ConfigFlags Flags);
  static void setConfigFlag(CDockManager::eConfigFlag Flag, bool On = true);
  static bool testConfigFlag(eConfigFlag Flag);
  static CDockManager::AutoHideFlags autoHideConfigFlags();
  static void setAutoHideConfigFlags(const CDockManager::AutoHideFlags Flags);
  static void setAutoHideConfigFlag(CDockManager::eAutoHideFlag Flag, bool On = true);
  static bool testAutoHideConfigFlag(eAutoHideFlag Flag);
  static void setConfigParam(eConfigParam Param, QVariant Value);
  static QVariant configParam(eConfigParam Param, QVariant Default);
  static CIconProvider& iconProvider();
  CDockAreaWidget* addDockWidget(DockWidgetArea area, CDockWidget* Dockwidget /Transfer/, CDockAreaWidget* DockAreaWidget /Transfer/ = nullptr, int Index = -1);
  CDockAreaWidget* addDockWidgetToContainer(DockWidgetArea area, CDockWidget* Dockwidget /Transfer/, CDockContainerWidget* DockContainerWidget /Transfer/ = nullptr);
  CAutoHideDockContainer* addAutoHideDockWidget(SideBarLocation Location, CDockWidget* Dockwidget /Transfer/);
  CAutoHideDockContainer* addAutoHideDockWidgetToContainer(SideBarLocation Location,
  CDockWidget* Dockwidget /Transfer/, CDockContainerWidget* DockContainerWidget);
  CDockAreaWidget* addDockWidgetTab(DockWidgetArea area,
  CDockWidget* Dockwidget /Transfer/);
  CDockAreaWidget* addDockWidgetTabToArea(CDockWidget* Dockwidget /Transfer/, CDockAreaWidget* DockAreaWidget /Transfer/, int Index = -1);
  CFloatingDockContainer* addDockWidgetFloating(CDockWidget* DockWidget /Transfer/);
  CDockWidget* findDockWidget(const QString& ObjectName) const;
  void removeDockWidget(CDockWidget* Dockwidget) /TransferBack/;
  QMap<QString, ads::CDockWidget*> dockWidgetsMap() const;
  const QList<ads::CDockContainerWidget*> dockContainers() const;
  const QList<ads::CFloatingDockContainer*> floatingWidgets() const;
  unsigned int zOrderIndex() const;
  QByteArray saveState(int version = 0) const;
  bool restoreState(const QByteArray &state, int version = 0);
  void addPerspective(const QString& UniquePrespectiveName);
  void removePerspective(const QString& Name);
  void removePerspectives(const QStringList& Names);
  QStringList perspectiveNames() const;
  void savePerspectives(QSettings& Settings) const;
  void loadPerspectives(QSettings& Settings);
  CDockWidget* centralWidget() const;
  CDockAreaWidget* setCentralWidget(CDockWidget* widget /Transfer/);
  QAction* addToggleViewActionToMenu(QAction* ToggleViewAction /Transfer/,
  const QString& Group = QString(), const QIcon& GroupIcon = QIcon());
  QMenu* viewMenu() const;
  void setViewMenuInsertionOrder(CDockManager::eViewMenuInsertionOrder Order);
  bool isRestoringState() const;
  bool isLeavingMinimizedState() const;
  static int startDragDistance();
  CDockWidget* focusedDockWidget() const;
  QList<int> splitterSizes(CDockAreaWidget *ContainedArea) const;
  void setSplitterSizes(CDockAreaWidget *ContainedArea, const QList<int>& sizes);
  static void setFloatingContainersTitle(const QString& Title);
  static QString floatingContainersTitle();
  void setDockWidgetToolBarStyle(Qt::ToolButtonStyle Style, CDockWidget::eState State);
  Qt::ToolButtonStyle dockWidgetToolBarStyle(CDockWidget::eState State) const;
  void setDockWidgetToolBarIconSize(const QSize& IconSize, CDockWidget::eState State);
  QSize dockWidgetToolBarIconSize(CDockWidget::eState State) const;
  CDockWidget::DockWidgetFeatures globallyLockedDockWidgetFeatures() const;
  void lockDockWidgetFeaturesGlobally(CDockWidget::DockWidgetFeatures Features = ads::CDockWidget::GloballyLockableFeatures);

public slots:
  void endLeavingMinimizedState();
  void openPerspective(const QString& PerspectiveName);
  void setDockWidgetFocused(CDockWidget* DockWidget);
  void hideManagerAndFloatingWidgets();
  void raise();

signals:
  void perspectiveListChanged();
  void perspectiveListLoaded();
  void perspectivesRemoved();
  void restoringState();
  void stateRestored();
  void openingPerspective(const QString& PerspectiveName);
  void perspectiveOpened(const QString& PerspectiveName);
  void floatingWidgetCreated(CFloatingDockContainer*);
  void dockAreaCreated(CDockAreaWidget*);
  void dockWidgetAdded(CDockWidget* DockWidget);
  void dockWidgetAboutToBeRemoved(CDockWidget*);
  void dockWidgetRemoved(CDockWidget*);
  void focusedDockWidgetChanged(CDockWidget*, CDockWidget*);
};

};
