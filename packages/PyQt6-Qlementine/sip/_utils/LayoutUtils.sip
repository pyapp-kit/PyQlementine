namespace oclero
{
namespace qlementine
{

%TypeHeaderCode
#include <oclero/qlementine/utils/LayoutUtils.hpp>
%End

QMargins getLayoutMargins(const QWidget* widget);
int getLayoutHSpacing(const QWidget* widget);
int getLayoutVSpacing(const QWidget* widget);
void clearLayout(QLayout* layout);

};
};
