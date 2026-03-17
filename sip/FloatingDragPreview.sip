%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CFloatingDragPreview : QWidget, ads::IFloatingWidget
{
%TypeHeaderCode
#include <FloatingDragPreview.h>
%End

protected:
  virtual void paintEvent(QPaintEvent *e);
  CFloatingDragPreview(QWidget* Content /TransferThis/, QWidget* parent /TransferThis/);

public:
  CFloatingDragPreview(ads::CDockWidget* Content /TransferThis/);
  CFloatingDragPreview(ads::CDockAreaWidget* Content /TransferThis/ );

  virtual ~CFloatingDragPreview();

  virtual bool eventFilter(QObject* watched, QEvent* event);

public: // implements IFloatingWidget
  virtual void startFloating(const QPoint& DragStartMousePos, const QSize& Size, eDragState DragState, QWidget* MouseEventHandler);
  virtual void moveFloating();
  virtual void finishDragging();
  void cleanupAutoHideContainerWidget(ads::DockWidgetArea ContainerDropArea);

signals:
  void draggingCanceled();
};

};
