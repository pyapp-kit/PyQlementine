%Import QtWidgets/QtWidgetsmod.sip

%MappedType QList<QPointer<ads::CDockAreaWidget>> /TypeHint="List[CDockAreaWidget*]", TypeHintValue="[]"/
{
%TypeHeaderCode
#include <qpointer.h>
#include <DockAreaWidget.h>
%End

%ConvertFromTypeCode
	PyObject *l = PyList_New(sipCpp->size());;
	if (l == NULL)
		return NULL;
	
	for (int i = 0; i < sipCpp->size(); ++i) {
		ads::CDockAreaWidget *t = sipCpp->at(i).data();
		PyObject *tobj = sipConvertFromType(t, sipType_ads_CDockAreaWidget, sipTransferObj);
		if (tobj == NULL) {
			Py_DECREF(l);
			return NULL;
		}
		PyList_SetItem(l, i, tobj);
	}
	
	return l;
%End
};

namespace ads
{

/**
 * Container that manages a number of dock areas with single dock widgets
 * or tabyfied dock widgets in each area.
 * Each window that support docking has a DockContainerWidget. That means
 * the main application window and all floating windows contain a
 * DockContainerWidget.
 */
class CDockContainerWidget : QFrame
{
	%TypeHeaderCode
	#include <DockContainerWidget.h>
	%End

protected:
	virtual bool event(QEvent *e);
	CDockSplitter* rootSplitter() const;
	CAutoHideDockContainer* createAndSetupAutoHideContainer(SideBarLocation area, CDockWidget* DockWidget /Transfer/, int TabIndex = -1);
	void createRootSplitter();
	void dropFloatingWidget(CFloatingDockContainer* FloatingWidget, const QPoint& TargetPos);
	void dropWidget(QWidget* Widget, DockWidgetArea DropArea, CDockAreaWidget* TargetAreaWidget, int TabIndex = -1);
	void addDockArea(CDockAreaWidget* DockAreaWidget /Transfer/, DockWidgetArea area = ads::CenterDockWidgetArea);
	void removeDockArea(CDockAreaWidget* area /TransferBack/);
	QList<QPointer<ads::CDockAreaWidget>> removeAllDockAreas();
	void saveState(QXmlStreamWriter& Stream) const;
	bool restoreState(CDockingStateReader& Stream, bool Testing);
	CDockAreaWidget* lastAddedDockAreaWidget(DockWidgetArea area) const;
	CDockWidget* topLevelDockWidget() const;
	CDockAreaWidget* topLevelDockArea() const;
	QList<ads::CDockWidget*> dockWidgets() const;
	void updateSplitterHandles(QSplitter* splitter);
	void registerAutoHideWidget(CAutoHideDockContainer* AutoHideWidget /Transfer/);
	void removeAutoHideWidget(CAutoHideDockContainer* AutoHideWidget /TransferBack/);
	void handleAutoHideWidgetEvent(QEvent* e, QWidget* w);

public:
	CDockContainerWidget(CDockManager* DockManager /TransferThis/, QWidget* parent /TransferThis/ = 0);
	virtual ~CDockContainerWidget();
	CDockAreaWidget* addDockWidget(DockWidgetArea area, CDockWidget* Dockwidget /Transfer/,
	CDockAreaWidget* DockAreaWidget /Transfer/ = 0, int Index = -1);
	void removeDockWidget(CDockWidget* Dockwidget) /TransferBack/;
	virtual unsigned int zOrderIndex() const;
	bool isInFrontOf(CDockContainerWidget* Other) const;
	CDockAreaWidget* dockAreaAt(const QPoint& GlobalPos) const;
	CDockAreaWidget* dockArea(int Index) const;
	QList<ads::CDockAreaWidget*> openedDockAreas() const;
	QList<ads::CDockWidget*> openedDockWidgets() const;
	bool hasTopLevelDockWidget() const;
	int dockAreaCount() const;
	int visibleDockAreaCount() const;
	bool isFloating() const;
	void dumpLayout();
	CDockWidget::DockWidgetFeatures features() const;
	CFloatingDockContainer* floatingWidget() const;
	void closeOtherAreas(CDockAreaWidget* KeepOpenArea);
	CAutoHideSideBar* autoHideSideBar(SideBarLocation area) const;
	QList<ads::CAutoHideDockContainer*> autoHideWidgets() const;
	QRect contentRect() const;
	QRect contentRectGlobal() const;
	CDockManager* dockManager() const;

signals:
	void dockAreasAdded();
	void autoHideWidgetCreated(CAutoHideDockContainer* AutoHideWidget);
	void dockAreasRemoved();
	void dockAreaViewToggled(CDockAreaWidget* DockArea, bool Open);
};

};
