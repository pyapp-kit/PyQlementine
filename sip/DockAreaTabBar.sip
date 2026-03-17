%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CDockAreaTabBar : QScrollArea
{
%TypeHeaderCode
#include <DockAreaTabBar.h>
%End
    
protected:
  virtual void wheelEvent(QWheelEvent* Event);

public:
  CDockAreaTabBar(CDockAreaWidget* parent /TransferThis/);
  virtual ~CDockAreaTabBar();
  void insertTab(int Index, CDockWidgetTab* Tab /Transfer/);
  void removeTab(CDockWidgetTab* Tab) /TransferBack/;
  int count() const;
  int currentIndex() const;
  CDockWidgetTab* currentTab() const;
  CDockWidgetTab* tab(int Index) const;
  int tabAt(const QPoint& Pos) const;
  int tabInsertIndexAt(const QPoint& Pos) const;
  virtual bool eventFilter(QObject *watched, QEvent *event);
  bool isTabOpen(int Index) const;
  virtual QSize minimumSizeHint() const;
  virtual QSize sizeHint() const;
  bool areTabsOverflowing() const;

public slots:
  void setCurrentIndex(int Index);
  void closeTab(int Index);

signals:
  void currentChanging(int Index);
  void currentChanged(int Index);
  void tabBarClicked(int index);
  void tabCloseRequested(int index);
  void tabClosed(int index);
  void tabOpened(int index);
  void tabMoved(int from, int to);
  void removingTab(int index);
  void tabInserted(int index);
  void elidedChanged(bool elided);
};

};
