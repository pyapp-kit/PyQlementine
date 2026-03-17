namespace oclero
{
namespace qlementine
{

class PopoverButton : QPushButton
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/PopoverButton.hpp>
%End

public:
    explicit PopoverButton(QWidget* parent /TransferThis/ = nullptr);
    PopoverButton(const QString& text, QWidget* parent /TransferThis/ = nullptr);
    PopoverButton(const QString& text, const QIcon& icon, QWidget* parent /TransferThis/ = nullptr);

    QWidget* popoverContentWidget() const;
    void setPopoverContentWidget(QWidget* widget /Transfer/);

    Popover* popover() const;

public slots:
    void setPopoverOpened(bool opened);

signals:
    void popoverContentWidgetChanged();
    void popoverOpenedChanged(bool opened);
};

};
};
