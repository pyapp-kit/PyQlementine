namespace oclero
{
namespace qlementine
{

class ColorEditor : QWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/ColorEditor.hpp>
%End

public:
    explicit ColorEditor(QWidget* parent /TransferThis/ = nullptr);
    explicit ColorEditor(const QColor& color, QWidget* parent /TransferThis/ = nullptr);

    const QColor& color() const;
    void setColor(const QColor& color);

    ColorMode colorMode() const;
    void setColorMode(ColorMode mode);

signals:
    void colorChanged();
    void colorModeChanged();
};

};
};
