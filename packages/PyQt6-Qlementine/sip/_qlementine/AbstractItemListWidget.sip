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

    // ---- protected helpers (exposed via sip public:) ------------------
    // These are declared protected: in AbstractItemListWidget.hpp but
    // are useful from Python for hit-testing, programmatic state control,
    // and custom drawing. Sip generates a friend shim regardless of the
    // C++ access modifier; we put them in `public:` here so the
    // generated Python API matches what callers actually want.

    int itemAtPos(const QPoint& pos) const;
    bool hitTestItemRect(const QPoint& pos, const QRect& itemRect, int leftPadding, int rightPadding) const;
    void updateItemsSizeHints();
    void updateItemRects();
    const QColor& getCurrentItemIndicatorColor() const;
    QRect getCurrentItemRect() const;
    QRect getFocusedItemRect() const;
    QRect getAnimatedCurrentItemRect() const;
    void updateCurrentIndexAnimation(bool immediate = false);
    void updateItemsAnimations();
    void setFocusedIndex(int index);
    void setHoveredIndex(int index, bool updateAnims = true);
    void setPressedIndex(int index, bool updateAnims = true);
    const QFont& badgeFont() const;
    const QRect& actualRect() const;

    // ---- color hooks exposed as non-virtual ---------------------------
    const QColor& getItemFgColor(MouseState mouse, bool selected, const Theme& theme) const;
    const QColor& getItemBgColor(MouseState mouse, const Theme& theme) const;
    const QColor& getBgColor(const Theme& theme) const;
    const QColor& getItemBadgeBgColor(MouseState mouse, bool selected, const Theme& theme) const;
    const QColor& getItemBadgeFgColor(MouseState mouse, bool selected, const Theme& theme) const;

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
    // ---- protected virtual style hooks --------------------------------
    // Customization points concrete subclasses (NavigationBar,
    // SegmentedControl, …) override in C++ to define spacing, colors, and
    // drawing for their specific look. Exposed so Python subclasses can
    // override them — useful for theming experiments and writing custom
    // bar widgets in pure Python.

    virtual QMargins getItemPadding() const;
    virtual int getItemMinimumHeight() const;
    virtual int getItemSpacing() const;
    virtual double getItemRadius() const;

    virtual QMargins getPadding() const;
    virtual int getSpacing() const;
    virtual double getRadius() const;

    virtual QMargins getBadgePadding() const;

    virtual void drawBackground(QPainter& p) const;
    virtual void drawCurrentItemIndicator(QPainter& p) const;
    virtual bool shouldDrawItemBgForCurrent() const;

    virtual QFont labelFont() const;
};

};
};
