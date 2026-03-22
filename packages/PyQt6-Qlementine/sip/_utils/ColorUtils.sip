namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/ColorUtils.hpp>
%End

double getContrastRatio(const QColor& c1, const QColor& c2);
QColor colorWithAlphaF(const QColor& color, qreal alpha);
QColor colorWithAlpha(const QColor& color, int alpha);
QColor getColorSourceOver(const QColor& bg, const QColor& fg);
QString toHexRGB(const QColor& color);
QString toHexRGBA(const QColor& color);

};
};
