namespace oclero
{
namespace qlementine
{

class StatusBadgeWidget : QWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/StatusBadgeWidget.hpp>
%End

public:
    explicit StatusBadgeWidget(QWidget* parent /TransferThis/ = nullptr);
    StatusBadgeWidget(StatusBadge badge, QWidget* parent /TransferThis/ = nullptr);
    StatusBadgeWidget(StatusBadge badge, StatusBadgeSize badgeSize, QWidget* parent /TransferThis/ = nullptr);

    StatusBadge badge() const;
    StatusBadgeSize badgeSize() const;

    QSize sizeHint() const;

public slots:
    void setBadge(StatusBadge badge);
    void setBadgeSize(StatusBadgeSize size);

signals:
    void badgeChanged();
    void badgeSizeChanged();
};

};
};
