namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/GeometryUtils.hpp>
%End

bool isPointInRoundedRect(const QPointF& point, const QRectF& rect, qreal cornerRadius);

};
};
