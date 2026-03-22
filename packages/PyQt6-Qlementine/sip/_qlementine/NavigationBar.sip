namespace oclero
{
namespace qlementine
{

class NavigationBar : AbstractItemListWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/NavigationBar.hpp>
%End

public:
    explicit NavigationBar(QWidget* parent /TransferThis/ = nullptr);
};

};
};
