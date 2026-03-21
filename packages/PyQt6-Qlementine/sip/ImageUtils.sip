namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/ImageUtils.hpp>
%End

QPixmap colorizePixmap(const QPixmap& input, const QColor& color);
QPixmap tintPixmap(const QPixmap& input, const QColor& color);
QPixmap getColorizedPixmap(const QPixmap& input, const QColor& color);
QPixmap getTintedPixmap(const QPixmap& input, const QColor& color);
QPixmap getCachedPixmap(const QPixmap& input, const QColor& color, ColorizeMode mode);
QPixmap makePixmapFromSvg(const QString& svgPath, const QSize& size);
QPixmap makePixmapFromSvg(const QString& backgroundSvgPath, const QColor& backgroundSvgColor,
    const QString& foregroundSvgPath, const QColor& foregroundSvgColor, const QSize& size);

};
};
