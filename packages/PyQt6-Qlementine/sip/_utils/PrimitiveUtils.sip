namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <QPainterPath>
#include <oclero/qlementine/utils/PrimitiveUtils.hpp>
%End

double getPixelRatio(const QWidget* w);

void drawEllipseBorder(QPainter* p, const QRectF& rect, const QColor& color, qreal borderWidth);
QPainterPath getMultipleRadiusesRectPath(const QRectF& rect, const RadiusesF& radiuses);

void drawRoundedRect(QPainter* p, const QRectF& rect, const QBrush& brush, qreal radius = 0.);
void drawRoundedRect(QPainter* p, const QRectF& rect, const QBrush& brush, const RadiusesF& radiuses);
void drawRoundedRect(QPainter* p, const QRect& rect, const QBrush& brush, qreal radius = 0.);
void drawRoundedRect(QPainter* p, const QRect& rect, const QBrush& brush, const RadiusesF& radiuses);

void drawRoundedRectBorder(QPainter* p, const QRectF& rect, const QColor& color, qreal borderWidth, qreal radius = 0.);
void drawRoundedRectBorder(QPainter* p, const QRect& rect, const QColor& color, qreal borderWidth, qreal radius = 0.);
void drawRoundedRectBorder(QPainter* p, const QRectF& rect, const QColor& color, qreal borderWidth, const RadiusesF& radiuses);
void drawRoundedRectBorder(QPainter* p, const QRect& rect, const QColor& color, qreal borderWidth, const RadiusesF& radiuses);

void drawRectBorder(QPainter* p, const QRect& rect, const QColor& color, qreal borderWidth);
void drawRectBorder(QPainter* p, const QRectF& rect, const QColor& color, qreal borderWidth);

void drawRoundedTriangle(QPainter* p, const QRectF& rect, qreal radius = 0.);

void drawCheckerboard(QPainter* p, const QRectF& rect, const QColor& darkColor, const QColor& lightColor, qreal cellWidth);

void drawProgressBarValueRect(QPainter* p, const QRect& rect, const QColor& color, qreal min, qreal max, qreal value,
    qreal radius = 0., bool inverted = false);

void drawColorMark(QPainter* p, const QRect& rect, const QColor& color, const QColor& borderColor, int borderWidth = 1);
void drawColorMarkBorder(QPainter* p, const QRect& rect, const QColor& borderColor, int borderWidth);

void drawDebugRect(const QRect& rect, QPainter* p);

QPainterPath getMenuIndicatorPath(const QRect& rect);
void drawComboBoxIndicator(const QRect& rect, QPainter* p);
void drawCheckBoxIndicator(const QRect& rect, QPainter* p, qreal progress = 1.);
void drawPartiallyCheckedCheckBoxIndicator(const QRect& rect, QPainter* p, qreal progress = 1.);
void drawRadioButtonIndicator(const QRect& rect, QPainter* p, qreal progress = 1.);
void drawSpinBoxArrowIndicator(const QRect& rect, QPainter* p,
    QAbstractSpinBox::ButtonSymbols buttonSymbol, QStyle::SubControl subControl, const QSize& iconSize);

void drawArrowRight(const QRect& rect, QPainter* p);
void drawArrowLeft(const QRect& rect, QPainter* p);
void drawArrowDown(const QRect& rect, QPainter* p);
void drawArrowUp(const QRect& rect, QPainter* p);

void drawSubMenuIndicator(const QRect& rect, QPainter* p);
void drawDoubleArrowRightIndicator(const QRect& rect, QPainter* p);
void drawToolBarExtensionIndicator(const QRect& rect, QPainter* p);
void drawCloseIndicator(const QRect& rect, QPainter* p);
void drawTreeViewIndicator(const QRect& rect, QPainter* p, bool open);
void drawCalendarIndicator(const QRect& rect, QPainter* p, const QColor& color);
void drawGripIndicator(const QRect& rect, QPainter* p, const QColor& color, Qt::Orientation orientation);

int getTickInterval(int tickInterval, int singleStep, int pageStep, int min, int max, int sliderLength);

void drawSliderTickMarks(QPainter* p, const QRect& tickmarksRect, const QColor& tickColor,
    int min, int max, int interval, int tickThickness, int singleStep, int pageStep);

void drawDialTickMarks(QPainter* p, const QRect& tickmarksRect, const QColor& tickColor,
    int min, int max, int tickThickness, int tickLength, int singleStep, int pageStep, int minArcLength);

void drawDial(QPainter* p, const QRect& rect, int min, int max, double value,
    const QColor& bgColor, const QColor& handleColor, const QColor& grooveColor,
    const QColor& valueColor, const QColor& markColor,
    int grooveThickness, int markLength, int markThickness);

QPainterPath getTabPath(const QRect& rect, const RadiusesF& radiuses);
void drawTab(QPainter* p, const QRect& rect, const RadiusesF& radiuses, const QColor& bgColor,
    bool drawShadow = false, const QColor& shadowColor = QColor(0, 0, 0));
void drawTabShadow(QPainter* p, const QRect& rect, const RadiusesF& radius, const QColor& color);

void drawRadioButton(QPainter* p, const QRect& rect, const QColor& bgColor, const QColor& borderColor,
    const QColor& fgColor, qreal borderWidth, qreal progress);
void drawCheckButton(QPainter* p, const QRect& rect, qreal radius, const QColor& bgColor,
    const QColor& borderColor, const QColor& fgColor, qreal borderWidth, qreal progress, CheckState checkState);

void drawMenuSeparator(QPainter* p, const QRect& rect, const QColor& color, int thickness);

void drawElidedMultiLineText(QPainter& p, const QRect& rect, const QString& text, const QPaintDevice* paintDevice);

QString removeTrailingWhitespaces(const QString& str);
QString displayedShortcutString(const QKeySequence& shortcut);
void drawShortcut(QPainter& p, const QKeySequence& shortcut, const QRect& rect, const Theme& theme, bool enabled,
    Qt::Alignment alignment = Qt::AlignLeft | Qt::AlignVCenter);
QSize shortcutSizeHint(const QKeySequence& shortcut, const Theme& theme);

QPixmap getPixmap(const QIcon& icon, const QSize& iconSize, MouseState mouse, CheckState checked, const QWidget* widget);
QRect drawIcon(const QRect& rect, QPainter* p, const QIcon& icon, MouseState mouse, CheckState checked,
    const QWidget* widget, bool colorize = false, const QColor& color = QColor());

QPixmap makeClearButtonPixmap(const QSize& size, const QColor& color);
QPixmap makeCheckPixmap(const QSize& size, const QColor& color);
QPixmap makeCalendarPixmap(const QSize& size, const QColor& color);
QPixmap makeDoubleArrowRightPixmap(const QSize& size, const QColor& color);
QPixmap makeToolBarExtensionPixmap(const QSize& size, const QColor& color);
QPixmap makeArrowLeftPixmap(const QSize& size, const QColor& color);
QPixmap makeArrowRightPixmap(const QSize& size, const QColor& color);

QPixmap makeMessageBoxWarningPixmap(const QSize& size, const QColor& bgColor, const QColor& fgColor);
QPixmap makeMessageBoxCriticalPixmap(const QSize& size, const QColor& bgColor, const QColor& fgColor);
QPixmap makeMessageBoxQuestionPixmap(const QSize& size, const QColor& bgColor, const QColor& fgColor);
QPixmap makeMessageBoxInformationPixmap(const QSize& size, const QColor& bgColor, const QColor& fgColor);

};
};
