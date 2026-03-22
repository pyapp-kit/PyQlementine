namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/BadgeUtils.hpp>
%End

void drawStatusBadge(QPainter* p, const QRect& rect, StatusBadge statusBadge, StatusBadgeSize size, const Theme& theme);

};
};
