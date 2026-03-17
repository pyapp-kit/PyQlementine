%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CAutoHideDockContainer : QFrame
{
%TypeHeaderCode
#include <AutoHideDockContainer.h>
%End

protected:
	virtual bool eventFilter(QObject* watched, QEvent* event);
	virtual void resizeEvent(QResizeEvent* event);
	virtual void leaveEvent(QEvent *event);
	virtual bool event(QEvent* event);
	void updateSize();
	void saveState(QXmlStreamWriter& Stream);

public:
	CAutoHideDockContainer(CDockWidget* DockWidget /Transfer/, ads::SideBarLocation area, CDockContainerWidget* parent /TransferThis/);
	virtual ~CAutoHideDockContainer();
	CAutoHideSideBar* autoHideSideBar() const;
	CAutoHideTab* autoHideTab() const;
	CDockWidget* dockWidget() const;
	int tabIndex() const;
	void addDockWidget(CDockWidget* DockWidget /Transfer/);
	SideBarLocation sideBarLocation() const;
	void setSideBarLocation(SideBarLocation SideBarLocation);
	CDockAreaWidget* dockAreaWidget() const;
	CDockContainerWidget* dockContainer() const;
	void moveContentsToParent();
	void cleanupAndDelete();
	void toggleView(bool Enable);
	void collapseView(bool Enable);
	void toggleCollapseState();
	void setSize(int Size);
	void resetToInitialDockWidgetSize();
	Qt::Orientation orientation() const;
	void moveToNewSideBarLocation(SideBarLocation);
};

};
