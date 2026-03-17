%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CTitleBarButton : QToolButton
{
%TypeHeaderCode
#include <DockAreaTitleBar.h>
%End

public:
  CTitleBarButton(bool ShowInTitleBar, bool HideWhenDisabled, TitleBarButton ButtonId, QWidget* parent /TransferThis/ = nullptr);
  virtual void setVisible(bool);
  void setShowInTitleBar(bool);
  TitleBarButton buttonId() const;
  CDockAreaTitleBar* titleBar() const;
  bool isInAutoHideArea() const;

protected:
  bool event(QEvent *ev);
};

class CDockAreaTitleBar : QFrame
{
%TypeHeaderCode
#include <DockAreaTitleBar.h>
%End

protected:
  virtual void mousePressEvent(QMouseEvent* ev);
  virtual void mouseReleaseEvent(QMouseEvent* ev);
  virtual void mouseMoveEvent(QMouseEvent* ev);
  virtual void mouseDoubleClickEvent(QMouseEvent *event);
  virtual void contextMenuEvent(QContextMenuEvent *event);
  virtual void resizeEvent(QResizeEvent *event);

public slots:
  void markTabsMenuOutdated();

public:
  CDockAreaTitleBar(CDockAreaWidget* parent /TransferThis/);
  virtual ~CDockAreaTitleBar();
  CDockAreaTabBar* tabBar() const;
  CTitleBarButton* button(TitleBarButton which) const;
  CElidingLabel* autoHideTitleLabel() const;
  CDockAreaWidget* dockAreaWidget() const;
  void updateDockWidgetActionsButtons();
  virtual void setVisible(bool Visible);
  void insertWidget(int index, QWidget *widget /Transfer/);
  int indexOf(QWidget *widget) const;
  QString titleBarButtonToolTip(TitleBarButton Button) const;
  void setAreaFloating();
  void showAutoHideControls(bool Show);
  bool isAutoHide() const;
  virtual QMenu *buildContextMenu(QMenu *menu /Transfer/ = nullptr);

signals:
  void tabBarClicked(int index);
};

};
