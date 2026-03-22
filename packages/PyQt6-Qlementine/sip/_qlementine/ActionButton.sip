namespace oclero
{
namespace qlementine
{

class ActionButton : QPushButton
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/ActionButton.hpp>
%End

public:
    explicit ActionButton(QWidget* parent /TransferThis/ = nullptr);
    virtual ~ActionButton();

    void setAction(QAction* action);
    void updateFromAction();
};

};
};
