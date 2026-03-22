namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/WidgetUtils.hpp>
%End

QWidget* makeVerticalLine(QWidget* parentWidget, int maxHeight = -1);
QWidget* makeHorizontalLine(QWidget* parentWidget, int maxWidth = -1);
void centerWidget(QWidget* widget, QWidget* host = nullptr);
qreal getDpi(const QWidget* widget);
QWindow* getWindow(const QWidget* widget);
void clearFocus(QWidget* widget, bool recursive);

};
};
