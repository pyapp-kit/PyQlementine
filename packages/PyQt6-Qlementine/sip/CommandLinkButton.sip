namespace oclero
{
namespace qlementine
{

class CommandLinkButton : QCommandLinkButton
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/CommandLinkButton.hpp>
%End

public:
    explicit CommandLinkButton(QWidget* parent /TransferThis/ = nullptr);
    explicit CommandLinkButton(const QString& text, QWidget* parent /TransferThis/ = nullptr);
    explicit CommandLinkButton(const QString& text, const QString& description, QWidget* parent /TransferThis/ = nullptr);
    explicit CommandLinkButton(const QIcon& icon, const QString& text, const QString& description, QWidget* parent /TransferThis/ = nullptr);
    virtual ~CommandLinkButton();

    QSize sizeHint() const;
    int heightForWidth(int) const;
    bool hasHeightForWidth() const;
};

};
};
