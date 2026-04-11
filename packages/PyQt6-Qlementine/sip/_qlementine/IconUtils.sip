namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/IconUtils.hpp>
%End

QIcon makeIconFromSvg(const QString& svgPath, const QSize& size);
QIcon makeIconFromSvg(const QString& svgPath, const IconTheme& iconTheme, const QSize& size = QSize(16, 16));

QIcon makeIconFromSvgData(const QByteArray& svgData, const QSize& size);
QIcon makeIconFromSvgData(const QByteArray& svgData, const IconTheme& iconTheme, const QSize& size = QSize(16, 16));

};
};
