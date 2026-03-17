%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CAutoHideSideBar : QScrollArea
{

%TypeHeaderCode
#include <AutoHideSideBar.h>
%End

protected:
	virtual bool eventFilter(QObject *watched, QEvent *event);
	void saveState(QXmlStreamWriter& Stream) const;
	void insertTab(int Index, CAutoHideTab* SideTab /Transfer/);

public:
	CAutoHideSideBar(CDockContainerWidget* parent /TransferThis/, SideBarLocation area);
	virtual ~CAutoHideSideBar();
	void removeTab(CAutoHideTab* SideTab) /TransferBack/;
	CAutoHideDockContainer* insertDockWidget(int Index, CDockWidget* DockWidget /Transfer/);
	void removeAutoHideWidget(CAutoHideDockContainer* AutoHideWidget) /TransferBack/;
	void addAutoHideWidget(CAutoHideDockContainer* AutoHideWidget, int Index);
	Qt::Orientation orientation() const;
	CAutoHideTab* tab(int index) const;
	int tabAt(const QPoint& Pos) const;
	int tabInsertIndexAt(const QPoint& Pos) const;
	int indexOfTab(const CAutoHideTab& Tab) const;
	int count() const;
	int visibleTabCount() const;
	bool hasVisibleTabs() const;
	SideBarLocation sideBarLocation() const;
	virtual QSize minimumSizeHint() const;
	virtual QSize sizeHint() const;
	int spacing() const;
	void setSpacing(int Spacing);
	CDockContainerWidget* dockContainer() const;
};

};
