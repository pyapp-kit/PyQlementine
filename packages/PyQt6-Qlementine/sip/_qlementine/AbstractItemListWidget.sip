namespace oclero
{
namespace qlementine
{

class AbstractItemListWidget : QWidget /Abstract/
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/AbstractItemListWidget.hpp>
%End

public:
    explicit AbstractItemListWidget(QWidget* parent /TransferThis/ = nullptr);
    virtual ~AbstractItemListWidget();

    QSize sizeHint() const;

    int itemCount() const;

    int currentIndex() const;
    void setCurrentIndex(int index);

    QVariant currentData() const;
    void setCurrentData(const QVariant& currentData);

    const QSize& iconSize() const;
    void setIconSize(const QSize& size);

    bool itemsShouldExpand() const;
    void setItemsShouldExpand(bool expand);

    int addItem(const QString& text, const QIcon& icon = QIcon(), const QString& badge = QString(), const QVariant& itemData = QVariant());
    void removeItem(int index);
    int findItemIndex(const QVariant& itemData) const;

    void setItemData(int index, const QVariant& text);
    QVariant getItemData(int index) const;

    void setItemText(int index, const QString& text);
    QString getItemText(int index) const;

    void setItemIcon(int index, const QIcon& icon);
    QIcon getItemIcon(int index) const;

    void setItemBadge(int index, const QString& badge);
    QString getItemBadge(int index) const;

    void setItemEnabled(int index, bool enabled);
    bool isItemEnabled(int index) const;

public slots:
    void moveToNextItem();
    void moveToPreviousItem();

signals:
    void itemCountChanged();
    void currentIndexChanged();
    void currentDataChanged();
    void iconSizeChanged();
    void itemsShouldExpandChanged();


protected:
    int itemAtPos(const QPoint& pos) const;
    void setPressedIndex(int index, bool updateAnims = true);

    virtual void mousePressEvent(QMouseEvent* e);
    virtual void mouseMoveEvent(QMouseEvent* e);
    virtual void mouseReleaseEvent(QMouseEvent* e);
    virtual void keyPressEvent(QKeyEvent* e);
    virtual void keyReleaseEvent(QKeyEvent* e);
    virtual void enterEvent(QEnterEvent* e);
    virtual void leaveEvent(QEvent* e);
    virtual void paintEvent(QPaintEvent* e);
    virtual void resizeEvent(QResizeEvent* e);
    virtual void focusInEvent(QFocusEvent* e);
    virtual void showEvent(QShowEvent* e);
    virtual void changeEvent(QEvent* e);
};

};
};
