namespace oclero
{
namespace qlementine
{

class IconWidget : QWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/IconWidget.hpp>
%End

public:
    explicit IconWidget(QWidget* parent /TransferThis/ = nullptr);
    IconWidget(const QIcon& icon, QWidget* parent /TransferThis/ = nullptr);
    IconWidget(const QIcon& icon, const QSize& size, QWidget* parent /TransferThis/ = nullptr);

    const QIcon& icon() const;
    const QSize& iconSize() const;

    QSize sizeHint() const;

public slots:
    void setIcon(const QIcon& icon);
    void setIconSize(const QSize& iconSize);

signals:
    void iconChanged();
    void iconSizeChanged();
};

};
};
