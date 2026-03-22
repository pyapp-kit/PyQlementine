namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/FontUtils.hpp>
%End

double pointSizeToPixelSize(double pointSize, double dpi);
double pixelSizeToPointSize(double pixelSize, double dpi);
int textWidth(const QFontMetrics& fm, const QString& text);

};
};
