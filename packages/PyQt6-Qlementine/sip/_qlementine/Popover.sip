namespace oclero
{
namespace qlementine
{

class Popover : QWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/Popover.hpp>
%End

public:
    enum class Position
    {
        Left,
        Top,
        Right,
        Bottom,
    };

    enum class Alignment
    {
        Begin,
        Center,
        End,
    };

    explicit Popover(QWidget* parent /TransferThis/ = nullptr);
    virtual ~Popover();

    bool manualPositioning() const;
    void setManualPositioning(bool manual);

    QSize popoverFrameSize() const;

    Popover::Position preferredPosition() const;
    void setPreferredPosition(Popover::Position position);

    Popover::Alignment preferredAlignment() const;
    void setPreferredAlignment(Popover::Alignment alignment);

    QWidget* contentWidget() const;
    void setContentWidget(QWidget* widget /Transfer/);

    bool isOpened() const;
    void setOpened(bool opened);

    bool isClosed() const;
    void setClosed(bool closed);

    QMargins padding() const;
    void setPadding(const QMargins& padding);

    QMargins screenPadding() const;
    void setScreenPadding(const QMargins& padding);

    QWidget* anchorWidget() const;
    void setAnchorWidget(QWidget* widget);

    int verticalSpacing() const;
    void setVerticalSpacing(int spacing);

    int horizontalSpacing() const;
    void setHorizontalSpacing(int spacing);

    const QColor& dropShadowColor() const;
    void setDropShadowColor(const QColor&);

    qreal radius() const;
    void setRadius(qreal radius);

    qreal borderWidth() const;
    void setBorderWidth(qreal width);

    qreal dropShadowRadius() const;
    void setDropShadowRadius(qreal radius);

    const QPointF& dropShadowOffset() const;
    void setDropShadowOffset(const QPointF& offset);

    bool canBeOverAnchor() const;
    void setCanBeOverAnchor(bool value);

    bool deleteContentAfterClosing() const;
    void setDeleteContentAfterClosing(bool);

    const QColor& backgroundColor() const;
    void setBackgroundColor(const QColor&);

    const QColor& borderColor() const;
    void setBorderColor(const QColor&);

    bool contentMaskEnabled() const;
    void setContentMaskEnabled(bool);

public slots:
    void openPopover();
    void closePopover();
    void togglePopover();

signals:
    void manualPositioningChanged();
    void preferredPositionChanged();
    void preferredAlignmentChanged();
    void contentWidgetChanged();
    void openedChanged();
    void paddingChanged();
    void screenPaddingChanged();
    void anchorWidgetChanged();
    void verticalSpacingChanged();
    void horizontalSpacingChanged();
    void dropShadowColorChanged();
    void radiusChanged();
    void borderWidthChanged();
    void dropShadowRadiusChanged();
    void dropShadowOffsetChanged();
    void canBeOverAnchorChanged();
    void deleteContentAfterClosingChanged();
    void backgroundColorChanged();
    void borderColorChanged();
    void contentMaskEnabledChanged();
    void aboutToOpen();
    void aboutToClose();
    void opened();
    void closed();
    void pressed();
    void released();
    void manualPositionRequested();
};

};
};
