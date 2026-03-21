namespace oclero
{
namespace qlementine
{

struct IconTheme
{

%TypeHeaderCode
#include <oclero/qlementine/utils/IconUtils.hpp>
%End

public:
    QColor normal;
    QColor disabled;
    QColor checkedNormal;
    QColor checkedDisabled;

    explicit IconTheme(const QColor& normal);
    IconTheme(const QColor& normal, const QColor& disabled);
    IconTheme(const QColor& normal, const QColor& disabled, const QColor& checkedNormal, QColor checkedDisabled);

    const QColor& color(QIcon::Mode mode, QIcon::State state) const;
};

};
};
