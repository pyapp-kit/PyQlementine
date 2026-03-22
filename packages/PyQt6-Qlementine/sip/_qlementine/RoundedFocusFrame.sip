namespace oclero
{
namespace qlementine
{

class RoundedFocusFrame : QFocusFrame
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/RoundedFocusFrame.hpp>
%End

public:
    RoundedFocusFrame(QWidget* parent /TransferThis/ = nullptr);

    const RadiusesF& radiuses() const;

public slots:
    void setRadiuses(const RadiusesF&);

signals:
    void radiusesChanged();
};

};
};
