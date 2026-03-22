namespace oclero
{
namespace qlementine
{

class ThemeMeta
{

%TypeHeaderCode
#include <oclero/qlementine/style/Theme.hpp>
%End

public:
    QString name;
    QString version;
    QString author;

    bool operator==(const ThemeMeta& other) const;
    bool operator!=(const ThemeMeta& other) const;
};


class Theme
{

%TypeHeaderCode
#include <oclero/qlementine/style/Theme.hpp>
%End

public:
    Theme();
    Theme(const Theme& other);
    virtual ~Theme();

    static Theme fromJsonPath(const QString& jsonPath);
%MethodCode
    auto result = oclero::qlementine::Theme::fromJsonPath(*a0);
    if (result.has_value()) {
        sipRes = new oclero::qlementine::Theme(std::move(result.value()));
    } else {
        PyErr_SetString(PyExc_ValueError, "Failed to load theme from JSON path");
        sipIsErr = 1;
    }
%End

    static Theme fromJsonDoc(const QJsonDocument& jsonDoc);
%MethodCode
    auto result = oclero::qlementine::Theme::fromJsonDoc(*a0);
    if (result.has_value()) {
        sipRes = new oclero::qlementine::Theme(std::move(result.value()));
    } else {
        PyErr_SetString(PyExc_ValueError, "Failed to load theme from JSON document");
        sipIsErr = 1;
    }
%End

    QJsonDocument toJson() const;

    bool operator==(const Theme& other) const;
    bool operator!=(const Theme& other) const;

    ThemeMeta meta;

    QColor backgroundColorMain1;
    QColor backgroundColorMain2;
    QColor backgroundColorMain3;
    QColor backgroundColorMain4;
    QColor backgroundColorMainTransparent;

    QColor backgroundColorWorkspace;
    QColor backgroundColorTabBar;

    QColor neutralColor;
    QColor neutralColorHovered;
    QColor neutralColorPressed;
    QColor neutralColorDisabled;
    QColor neutralColorTransparent;

    QColor focusColor;

    QColor primaryColor;
    QColor primaryColorHovered;
    QColor primaryColorPressed;
    QColor primaryColorDisabled;
    QColor primaryColorTransparent;

    QColor primaryColorForeground;
    QColor primaryColorForegroundHovered;
    QColor primaryColorForegroundPressed;
    QColor primaryColorForegroundDisabled;
    QColor primaryColorForegroundTransparent;

    QColor primaryAlternativeColor;
    QColor primaryAlternativeColorHovered;
    QColor primaryAlternativeColorPressed;
    QColor primaryAlternativeColorDisabled;
    QColor primaryAlternativeColorTransparent;

    QColor secondaryColor;
    QColor secondaryColorHovered;
    QColor secondaryColorPressed;
    QColor secondaryColorDisabled;
    QColor secondaryColorTransparent;

    QColor secondaryColorForeground;
    QColor secondaryColorForegroundHovered;
    QColor secondaryColorForegroundPressed;
    QColor secondaryColorForegroundDisabled;
    QColor secondaryColorForegroundTransparent;

    QColor secondaryAlternativeColor;
    QColor secondaryAlternativeColorHovered;
    QColor secondaryAlternativeColorPressed;
    QColor secondaryAlternativeColorDisabled;
    QColor secondaryAlternativeColorTransparent;

    QColor statusColorSuccess;
    QColor statusColorSuccessHovered;
    QColor statusColorSuccessPressed;
    QColor statusColorSuccessDisabled;
    QColor statusColorInfo;
    QColor statusColorInfoHovered;
    QColor statusColorInfoPressed;
    QColor statusColorInfoDisabled;
    QColor statusColorWarning;
    QColor statusColorWarningHovered;
    QColor statusColorWarningPressed;
    QColor statusColorWarningDisabled;
    QColor statusColorError;
    QColor statusColorErrorHovered;
    QColor statusColorErrorPressed;
    QColor statusColorErrorDisabled;
    QColor statusColorForeground;
    QColor statusColorForegroundHovered;
    QColor statusColorForegroundPressed;
    QColor statusColorForegroundDisabled;

    QColor shadowColor1;
    QColor shadowColor2;
    QColor shadowColor3;
    QColor shadowColorTransparent;

    QColor borderColor;
    QColor borderColorHovered;
    QColor borderColorPressed;
    QColor borderColorDisabled;
    QColor borderColorTransparent;

    QColor semiTransparentColor1;
    QColor semiTransparentColor2;
    QColor semiTransparentColor3;
    QColor semiTransparentColor4;
    QColor semiTransparentColorTransparent;

    bool useSystemFonts;

    int fontSize;
    int fontSizeMonospace;
    int fontSizeH1;
    int fontSizeH2;
    int fontSizeH3;
    int fontSizeH4;
    int fontSizeH5;
    int fontSizeS1;
    int animationDuration;
    int focusAnimationDuration;
    int sliderAnimationDuration;
    double borderRadius;
    double checkBoxBorderRadius;
    double menuItemBorderRadius;
    double menuBarItemBorderRadius;
    int borderWidth;
    int controlHeightLarge;
    int controlHeightMedium;
    int controlHeightSmall;
    int controlDefaultWidth;
    int dialMarkLength;
    int dialMarkThickness;
    int dialTickLength;
    int dialTickSpacing;
    int dialGrooveThickness;
    int focusBorderWidth;
    QSize iconSize;
    QSize iconSizeMedium;
    QSize iconSizeLarge;
    QSize iconSizeExtraSmall;
    int sliderTickSize;
    int sliderTickSpacing;
    int sliderTickThickness;
    int sliderGrooveHeight;
    int progressBarGrooveHeight;
    int spacing;
    int scrollBarThicknessFull;
    int scrollBarThicknessSmall;
    int scrollBarMargin;
    int tabBarPaddingTop;
    int tabBarTabMaxWidth;
    int tabBarTabMinWidth;

    QFont fontRegular;
    QFont fontBold;
    QFont fontH1;
    QFont fontH2;
    QFont fontH3;
    QFont fontH4;
    QFont fontH5;
    QFont fontCaption;
    QFont fontMonospace;

    QPalette palette;
};

};
};
