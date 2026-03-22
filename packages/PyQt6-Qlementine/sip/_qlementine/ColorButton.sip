namespace oclero
{
namespace qlementine
{

class ColorButton : QAbstractButton
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/ColorButton.hpp>
%End

public:
    explicit ColorButton(QWidget* parent /TransferThis/ = nullptr);
    explicit ColorButton(const QColor& color, QWidget* parent /TransferThis/ = nullptr);
    explicit ColorButton(const QColor& color, ColorMode mode, QWidget* parent /TransferThis/ = nullptr);

    const QColor& color() const;
    void setColor(const QColor& color);
    void setColor(const QString& color);
%MethodCode
    sipCpp->setColor(QColor(*a0));
%End

    ColorMode colorMode() const;
    void setColorMode(ColorMode mode);

    QSize sizeHint() const;

signals:
    void colorChanged();
    void colorModeChanged();

protected:
    void paintEvent(QPaintEvent* e);
};

};
};
