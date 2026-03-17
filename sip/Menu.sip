namespace oclero
{
namespace qlementine
{

class Menu : QMenu
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/Menu.hpp>
%End

public:
    Menu(QWidget* parent /TransferThis/ = nullptr);
    Menu(const QString& title, QWidget* parent /TransferThis/ = nullptr);

    void updateEnabled();
    void updateVisible();
    void updateProps();
};

};
};
