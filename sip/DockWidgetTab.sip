%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CDockWidgetTab : QFrame
{
%TypeHeaderCode
#include <DockWidgetTab.h>
%End

protected:
  virtual void mousePressEvent(QMouseEvent* ev);
  virtual void mouseReleaseEvent(QMouseEvent* ev);
  virtual void mouseMoveEvent(QMouseEvent* ev);
  virtual void contextMenuEvent(QContextMenuEvent* ev);
  virtual void mouseDoubleClickEvent(QMouseEvent *event);

public:
  CDockWidgetTab(CDockWidget* DockWidget /TransferThis/, QWidget* parent /TransferThis/ = nullptr);
  virtual ~CDockWidgetTab();
  bool isActiveTab() const;
  void setActiveTab(bool active);
  void setDockAreaWidget(CDockAreaWidget* DockArea /Transfer/);
  CDockAreaWidget* dockAreaWidget() const;
  CDockWidget* dockWidget() const;
  void setIcon(const QIcon& Icon);
  const QIcon& icon() const;
  QString text() const;
  void setText(const QString& title);
  bool isTitleElided() const;
  bool isClosable() const;
  virtual bool event(QEvent *e);
  void setElideMode(Qt::TextElideMode mode);
  void updateStyle();
  QSize iconSize() const;
  void setIconSize(const QSize& Size);
  eDragState dragState() const;
  virtual QMenu *buildContextMenu(QMenu* menu /Transfer/ = nullptr);

public slots:
  virtual void setVisible(bool visible);

signals:
  void activeTabChanged();
  void clicked();
  void closeRequested();
  void closeOtherTabsRequested();
  void moved(const QPoint& GlobalPos);
  void elidedChanged(bool elided);
};

};
