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

    QColor primaryColor;
    QColor primaryColorHovered;
    QColor primaryColorPressed;
    QColor primaryColorDisabled;

    QColor primaryColorForeground;

    QColor secondaryColor;
    QColor secondaryColorHovered;
    QColor secondaryColorPressed;
    QColor secondaryColorDisabled;

    QColor secondaryColorForeground;

    QColor statusColorSuccess;
    QColor statusColorInfo;
    QColor statusColorWarning;
    QColor statusColorError;
    QColor statusColorForeground;

    QColor focusColor;
    QColor borderColor;

    bool useSystemFonts;
    int fontSize;
    int animationDuration;
    double borderRadius;
    int borderWidth;
    int controlHeightLarge;
    int controlHeightMedium;
    int controlHeightSmall;
    int spacing;
    QSize iconSize;

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
