namespace oclero
{
namespace qlementine
{

class LoadingSpinner : QWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/LoadingSpinner.hpp>
%End

public:
    explicit LoadingSpinner(QWidget* parent /TransferThis/ = nullptr);

    bool spinning() const;

    QSize minimumSizeHint() const;
    QSize sizeHint() const;

public slots:
    void setSpinning(bool);

signals:
    void spinningChanged();
};

};
};
