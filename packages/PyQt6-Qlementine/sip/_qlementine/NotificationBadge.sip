namespace oclero
{
namespace qlementine
{

class NotificationBadge : QWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/NotificationBadge.hpp>
%End

public:
    explicit NotificationBadge(QWidget* parent /TransferThis/ = nullptr);

    void setWidget(QWidget* widget);
    QWidget* widget() const;

    const QString& text() const;

    const QColor& foregroundColor() const;
    const QColor& backgroundColor() const;
    const QPoint& relativePosition() const;
    const QMargins& padding() const;

    QSize minimumSizeHint() const;
    QSize sizeHint() const;

public slots:
    void setText(const QString&);
    void setForegroundColor(const QColor&);
    void setBackgroundColor(const QColor&);
    void setRelativePosition(const QPoint&);
    void setRelativePosition(int x, int y);
    void setPadding(const QMargins&);

signals:
    void textChanged();
    void foregroundColorChanged();
    void backgroundColorChanged();
    void relativePositionChanged();
    void paddingChanged();
};

};
};
