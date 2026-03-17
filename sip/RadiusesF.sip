namespace oclero
{
namespace qlementine
{

class RadiusesF
{

%TypeHeaderCode
#include <oclero/qlementine/utils/RadiusesF.hpp>
%End

public:
    double topLeft;
    double topRight;
    double bottomRight;
    double bottomLeft;

    RadiusesF();
    explicit RadiusesF(double radius);
    RadiusesF(double left, double right);
    RadiusesF(double topLeft, double topRight, double bottomRight, double bottomLeft);

    bool hasSameRadius() const;
    bool hasDifferentRadius() const;

    bool operator==(const RadiusesF& rhs) const;
    bool operator!=(const RadiusesF& rhs) const;
};

};
};
