// NOTE: there is a separate sip/linux/FloatingDockContainer.sip as the base
// class for CFloatingDockContainer changes for Linux.

%Import QtWidgets/QtWidgetsmod.sip

%If (Linux)
	typedef QDockWidget tFloatingWidgetBase;
%End
%If (!Linux)
	typedef QWidget tFloatingWidgetBase;
%End

namespace ads
{

class IFloatingWidget
{
%TypeHeaderCode
#include <FloatingDockContainer.h>
%End

public:
	virtual void startFloating(const QPoint& DragStartMousePos, const QSize& Size, eDragState DragState, QWidget* MouseEventHandler) = 0;
	virtual void moveFloating() = 0;
	virtual void finishDragging() = 0;
	virtual ~IFloatingWidget();
};

class CFloatingDockContainer : tFloatingWidgetBase, IFloatingWidget
{
%TypeHeaderCode
#include <FloatingDockContainer.h>
%End

protected:
	virtual void startFloating(const QPoint& DragStartMousePos, const QSize& Size, eDragState DragState, QWidget* MouseEventHandler);
	virtual void finishDragging();
	void deleteContent();
	void initFloatingGeometry(const QPoint& DragStartMousePos, const QSize& Size);
	void moveFloating();
	bool restoreState(CDockingStateReader& Stream, bool Testing);
	void updateWindowTitle();

protected:
	virtual void changeEvent(QEvent *event);
	virtual void closeEvent(QCloseEvent *event);
	virtual void hideEvent(QHideEvent *event);
	virtual void showEvent(QShowEvent *event);

%If (macOS)
	virtual bool event(QEvent *e);
	virtual void moveEvent(QMoveEvent *event);
%End
	
%If (Linux)
	virtual void moveEvent(QMoveEvent *event);
	virtual void resizeEvent(QResizeEvent *event);
	virtual bool event(QEvent *e);
%End
	
%If (Windows)
	virtual bool nativeEvent(const QByteArray &eventType, void *message, qintptr *result);
%End

public:
	CFloatingDockContainer(CDockManager* DockManager /TransferThis/);
	CFloatingDockContainer(CDockAreaWidget* DockArea /TransferThis/);
	CFloatingDockContainer(CDockWidget* DockWidget /TransferThis/);
	virtual ~CFloatingDockContainer();
	CDockContainerWidget* dockContainer() const;
	void startDragging(const QPoint& DragStartMousePos, const QSize& Size, QWidget* MouseEventHandler);
	bool isClosable() const;
	bool hasTopLevelDockWidget() const;
	CDockWidget* topLevelDockWidget() const;
	QList<ads::CDockWidget*> dockWidgets() const;
	void finishDropOperation();
	
%If (Linux)
	void onMaximizeRequest();
	void showNormal(bool fixGeometry);
	void showMaximized();
	bool isMaximized() const;
	void show();
	bool hasNativeTitleBar();
%End
};

};
