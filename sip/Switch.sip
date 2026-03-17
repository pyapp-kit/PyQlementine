namespace oclero
{
namespace qlementine
{

class Switch : QAbstractButton
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/Switch.hpp>
%End

public:
    explicit Switch(QWidget* parent /TransferThis/ = nullptr);

    QSize sizeHint() const;

    void setTristate(bool);
    bool isTristate() const;

    bool showAccessibilitySymbols() const;
    void setShowAccessibilitySymbols(bool showAccessibilitySymbols);

    Qt::CheckState checkState() const;
    void setCheckState(Qt::CheckState state);

signals:
    void checkStateChanged(int);
    void tristateChanged(bool);
    void showAccessibilitySymbolsChanged(bool);
};

};
};
