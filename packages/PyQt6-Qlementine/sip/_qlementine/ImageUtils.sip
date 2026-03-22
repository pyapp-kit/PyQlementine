namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/ImageUtils.hpp>
%End

QImage colorizeImage(const QPixmap& input, const QColor& color);
QPixmap colorizePixmap(const QPixmap& input, const QColor& color);
QPixmap tintPixmap(const QPixmap& input, const QColor& color);
QPixmap getColorizedPixmap(const QPixmap& input, const QColor& color);
QPixmap getTintedPixmap(const QPixmap& input, const QColor& color);
QPixmap getCachedPixmap(const QPixmap& input, const QColor& color, ColorizeMode mode);
QPixmap makePixmapFromSvg(const QString& svgPath, const QSize& size);
QPixmap makePixmapFromSvg(const QString& backgroundSvgPath, const QColor& backgroundSvgColor,
    const QString& foregroundSvgPath, const QColor& foregroundSvgColor, const QSize& size);
QPixmap makeRoundedPixmap(const QPixmap& input, double radius);
QPixmap makeRoundedPixmap(const QPixmap& input, const RadiusesF& radiuses);
QPixmap makeRoundedPixmap(const QPixmap& input, double topLeft, double topRight, double bottomRight, double bottomLeft);
QPixmap makeFitPixmap(const QPixmap& input, const QSize& size);
double getImageAspectRatio(const QString& path);
QImage getExtendedImage(const QPixmap& input, int padding);
QImage getExtendedImage(const QImage& input, int padding);
QPixmap getBlurredPixmap(const QPixmap& input, double blurRadius);
QPixmap getDropShadowPixmap(const QPixmap& input, double blurRadius, const QColor& color = QColor(0, 0, 0));
QPixmap getDropShadowPixmap(const QSize& size, double borderRadius, double blurRadius, const QColor& color = QColor(0, 0, 0));
int blurRadiusNecessarySpace(double blurRadius);

};
};
