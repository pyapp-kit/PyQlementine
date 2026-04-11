%Import QtWidgets/QtWidgetsmod.sip

namespace oclero
{
namespace qlementine
{

class QlementineStyle : QCommonStyle
{

%TypeHeaderCode
#include <oclero/qlementine/style/QlementineStyle.hpp>
#include <functional>
#include <memory>
%End

public:
    enum class StandardPixmapExt {
        SP_Check,
        SP_Calendar,
    };

    enum class ControlElementExt {
        CE_CommandButtonLabel,
        CE_CommandButton,
    };

    enum class ContentsTypeExt {
        CT_CommandButton,
    };

    enum class PixelMetricExt {
        PM_MediumIconSize,
    };

    enum class PrimitiveElementExt {
        PE_CommandButtonPanel,
        PE_CommandButtonLabel,
    };

    explicit QlementineStyle(QObject* parent /TransferThis/ = nullptr);
    virtual ~QlementineStyle();

    const Theme& theme() const;
    void setTheme(const Theme& theme);
    void setThemeJsonPath(const QString& jsonPath);

    bool animationsEnabled() const;
    void setAnimationsEnabled(bool enabled);

    virtual void triggerCompleteRepaint();

    void setAutoIconColor(AutoIconColor autoIconColor);
    AutoIconColor autoIconColor() const;

    static void setAutoIconColor(QWidget* widget, AutoIconColor autoIconColor);
    AutoIconColor autoIconColor(const QWidget* widget) const;

    static void setIconStatus(QWidget* widget, Status status);
    Status iconStatus(const QWidget* widget) const;

    QPixmap getColorizedPixmap(
        const QPixmap& input, AutoIconColor autoIconColor,
        const QColor& fgcolor, const QColor& textColor) const;

    QPixmap getColorizedPixmap(
        const QPixmap& input, const QWidget* widget,
        const QColor& fgColor, const QColor& textColor,
        MouseState mouse = oclero::qlementine::MouseState::Normal) const;

    QIcon makeThemedIcon(
        const QString& svgPath,
        const QSize& size = QSize(16, 16),
        ColorRole role = oclero::qlementine::ColorRole::Secondary) const;

    QIcon makeThemedIconFromName(
        const QString& name,
        const QSize& size = QSize(16, 16),
        ColorRole role = oclero::qlementine::ColorRole::Secondary) const;

    // Icon path getter: accepts a Python callable (str) -> str, or None.
    void setIconPathGetter(SIP_PYCALLABLE /AllowNone/);
%MethodCode
    if (a0 == Py_None) {
        sipCpp->setIconPathGetter(std::function<QString(QString)>{});
    } else {
        // prevent GC; release when the std::function is destroyed
        Py_INCREF(a0);
        auto ref = std::shared_ptr<PyObject>(a0, [](PyObject* p) {
            if (Py_IsInitialized()) {
                PyGILState_STATE gil = PyGILState_Ensure();
                Py_DECREF(p);
                PyGILState_Release(gil);
            }
        });

        sipCpp->setIconPathGetter([ref](const QString& name) -> QString {
            PyGILState_STATE gil = PyGILState_Ensure();

            PyObject* pyName = PyUnicode_FromString(
                name.toUtf8().constData());
            PyObject* result = PyObject_CallFunctionObjArgs(
                ref.get(), pyName, nullptr);
            Py_DECREF(pyName);

            QString out;
            if (result) {
                PyObject* strResult = PyObject_Str(result);
                if (strResult) {
                    PyObject* bytes = PyUnicode_AsUTF8String(strResult);
                    if (bytes) {
                        out = QString::fromUtf8(PyBytes_AsString(bytes));
                        Py_DECREF(bytes);
                    }
                    Py_DECREF(strResult);
                }
                Py_DECREF(result);
            } else {
                PyErr_Print();
            }

            PyGILState_Release(gil);
            return out;
        });
    }
%End

    // Inherited QStyle virtuals — required for Python subclass overrides.
    virtual void drawPrimitive(QStyle::PrimitiveElement pe,
        const QStyleOption *opt, QPainter *p,
        const QWidget *w = nullptr) const;
    virtual void drawControl(QStyle::ControlElement ce,
        const QStyleOption *opt, QPainter *p,
        const QWidget *w = nullptr) const;
    virtual void drawComplexControl(QStyle::ComplexControl cc,
        const QStyleOptionComplex *opt, QPainter *p,
        const QWidget *w = nullptr) const;
    virtual void polish(QWidget *widget);
    virtual void polish(QPalette &palette);
    virtual void polish(QApplication *app);
    virtual void unpolish(QWidget *widget);
    virtual void unpolish(QApplication *app);
    virtual QSize sizeFromContents(QStyle::ContentsType ct,
        const QStyleOption *opt, const QSize &csz,
        const QWidget *w = nullptr) const;
    virtual QRect subElementRect(QStyle::SubElement se,
        const QStyleOption *opt,
        const QWidget *w = nullptr) const;
    virtual QRect subControlRect(QStyle::ComplexControl cc,
        const QStyleOptionComplex *opt, QStyle::SubControl sc,
        const QWidget *w = nullptr) const;
    virtual int pixelMetric(QStyle::PixelMetric m,
        const QStyleOption *opt = nullptr,
        const QWidget *w = nullptr) const;
    virtual int styleHint(QStyle::StyleHint sh,
        const QStyleOption *opt = nullptr,
        const QWidget *w = nullptr,
        QStyleHintReturn *hret = nullptr) const;
    virtual QIcon standardIcon(QStyle::StandardPixmap sp,
        const QStyleOption *opt = nullptr,
        const QWidget *w = nullptr) const;
    virtual int layoutSpacing(QSizePolicy::ControlType c1,
        QSizePolicy::ControlType c2, Qt::Orientation o,
        const QStyleOption *opt = nullptr,
        const QWidget *w = nullptr) const;
    virtual QStyle::SubControl hitTestComplexControl(
        QStyle::ComplexControl cc, const QStyleOptionComplex *opt,
        const QPoint &pos, const QWidget *w = nullptr) const;
    virtual QPixmap standardPixmap(QStyle::StandardPixmap sp,
        const QStyleOption *opt = nullptr,
        const QWidget *w = nullptr) const;
    virtual QPixmap generatedIconPixmap(QIcon::Mode mode,
        const QPixmap &pixmap, const QStyleOption *opt) const;
    virtual QPalette standardPalette() const;

    // Extended QStyle methods.
    virtual void drawPrimitiveExt(
        PrimitiveElementExt pe, const QStyleOption* opt, QPainter* p,
        const QWidget* w = nullptr) const;
    virtual QIcon standardIconExt(
        StandardPixmapExt sp, const QStyleOption* opt = nullptr,
        const QWidget* w = nullptr) const;
    virtual QSize sizeFromContentsExt(
        ContentsTypeExt ct, const QStyleOption* opt, const QSize& s,
        const QWidget* w = nullptr) const;
    virtual void drawControlExt(
        ControlElementExt ce, const QStyleOption* opt, QPainter* p,
        const QWidget* w = nullptr) const;
    virtual int pixelMetricExt(
        PixelMetricExt m, const QStyleOption* opt = nullptr,
        const QWidget* w = nullptr) const;

    // Theme color methods.
    virtual const QColor& color(MouseState mouse, ColorRole role) const;
    virtual const QColor& frameBackgroundColor(MouseState mouse) const;

    virtual const QColor& buttonBackgroundColor(
        MouseState mouse, ColorRole role, const QWidget* w = nullptr) const;
    virtual const QColor& buttonForegroundColor(
        MouseState mouse, ColorRole role, const QWidget* w = nullptr) const;

    virtual const QColor& toolButtonBackgroundColor(MouseState mouse, ColorRole role) const;
    virtual const QColor& toolButtonForegroundColor(MouseState mouse, ColorRole role) const;
    virtual const QColor& toolButtonSeparatorColor(MouseState mouse, ColorRole role) const;

    virtual const QColor& commandButtonBackgroundColor(MouseState mouse, ColorRole role) const;
    virtual const QColor& commandButtonTextColor(MouseState mouse, ColorRole role) const;
    virtual const QColor& commandButtonDescriptionColor(MouseState mouse, ColorRole role) const;
    virtual const QColor& commandButtonIconColor(MouseState mouse, ColorRole role) const;

    virtual const QColor& checkButtonBackgroundColor(MouseState mouse, CheckState checked) const;
    virtual const QColor& checkButtonForegroundColor(MouseState mouse, CheckState checked) const;
    virtual const QColor& checkButtonBorderColor(
        MouseState mouse, FocusState focus, CheckState checked) const;

    virtual const QColor& radioButtonBackgroundColor(MouseState mouse, CheckState checked) const;
    virtual const QColor& radioButtonForegroundColor(MouseState mouse, CheckState checked) const;
    virtual const QColor& radioButtonBorderColor(
        MouseState mouse, FocusState focus, CheckState checked) const;

    virtual const QColor& comboBoxBackgroundColor(MouseState mouse) const;
    virtual const QColor& comboBoxForegroundColor(MouseState mouse) const;
    virtual const QColor& comboBoxTextColor(
        MouseState mouse, Status status, const QWidget* w = nullptr) const;

    virtual const QColor& spinBoxBackgroundColor(MouseState mouse) const;
    virtual const QColor& spinBoxBorderColor(MouseState mouse, FocusState focus) const;
    virtual const QColor& spinBoxButtonBackgroundColor(MouseState mouse) const;
    virtual const QColor& spinBoxButtonForegroundColor(MouseState mouse) const;

    virtual const QColor& listItemRowBackgroundColor(
        MouseState mouse, AlternateState alternate) const;
    virtual QColor listItemBackgroundColor(
        MouseState mouse, SelectionState selected, FocusState focus,
        ActiveState active, const QModelIndex& index,
        const QWidget* widget = nullptr) const;
    virtual const QColor& listItemForegroundColor(
        MouseState mouse, SelectionState selected, FocusState focus,
        ActiveState active) const;
    virtual AutoIconColor listItemAutoIconColor(
        MouseState mouse, SelectionState selected, FocusState focus,
        ActiveState active, const QModelIndex& index,
        const QWidget* widget = nullptr) const;
    virtual const QColor& listItemCaptionForegroundColor(
        MouseState mouse, SelectionState selected, FocusState focus,
        ActiveState active) const;
    virtual const QColor& listItemCheckButtonBackgroundColor(
        MouseState mouse, CheckState checked, SelectionState selected,
        ActiveState active) const;
    virtual const QColor& listItemCheckButtonBorderColor(
        MouseState mouse, CheckState checked, SelectionState selected,
        ActiveState active) const;
    virtual const QColor& listItemCheckButtonForegroundColor(
        MouseState mouse, CheckState checked, SelectionState selected,
        ActiveState active) const;
    virtual const QColor& cellItemFocusBorderColor(
        FocusState focus, SelectionState selected, ActiveState active) const;

    virtual const QColor& menuBackgroundColor() const;
    virtual const QColor& menuBorderColor() const;
    virtual const QColor& menuSeparatorColor() const;

    virtual const QColor& menuItemBackgroundColor(MouseState mouse) const;
    virtual const QColor& menuItemForegroundColor(MouseState mouse) const;
    virtual const QColor& menuItemSecondaryForegroundColor(MouseState mouse) const;

    virtual const QColor& menuBarBackgroundColor() const;
    virtual const QColor& menuBarBorderColor() const;
    virtual const QColor& menuBarItemBackgroundColor(
        MouseState mouse, SelectionState selected) const;
    virtual const QColor& menuBarItemForegroundColor(
        MouseState mouse, SelectionState selected) const;

    virtual const QColor& tabBarBackgroundColor(MouseState mouse) const;
    virtual const QColor& tabBarShadowColor() const;
    virtual const QColor& tabBarBottomShadowColor() const;
    virtual const QColor& tabBackgroundColor(MouseState mouse, SelectionState selected) const;
    virtual const QColor& tabForegroundColor(MouseState mouse, SelectionState selected) const;
    virtual QColor tabTextColor(
        MouseState mouse, SelectionState selected,
        const QStyleOptionTab* optTab, const QWidget* w = nullptr) const;
    virtual const QColor& tabCloseButtonBackgroundColor(
        MouseState mouse, SelectionState selected) const;
    virtual const QColor& tabCloseButtonForegroundColor(
        MouseState mouse, SelectionState selected) const;
    virtual const QColor& tabBarScrollButtonBackgroundColor(MouseState mouse) const;

    virtual const QColor& progressBarGrooveColor(MouseState mouse) const;
    virtual const QColor& progressBarValueColor(MouseState mouse) const;

    virtual const QColor& textFieldBackgroundColor(MouseState mouse, Status status) const;
    virtual const QColor& textFieldBorderColor(
        MouseState mouse, FocusState focus, Status status) const;
    virtual const QColor& textFieldForegroundColor(MouseState mouse) const;

    virtual const QColor& sliderGrooveColor(MouseState mouse) const;
    virtual const QColor& sliderValueColor(MouseState mouse) const;
    virtual const QColor& sliderHandleColor(MouseState mouse) const;
    virtual const QColor& sliderTickColor(MouseState mouse) const;

    virtual const QColor& dialHandleColor(MouseState mouse) const;
    virtual const QColor& dialGrooveColor(MouseState mouse) const;
    virtual const QColor& dialValueColor(MouseState mouse) const;
    virtual const QColor& dialTickColor(MouseState mouse) const;
    virtual const QColor& dialMarkColor(MouseState mouse) const;
    virtual const QColor& dialBackgroundColor(MouseState mouse) const;

    virtual const QColor& labelForegroundColor(
        MouseState mouse, const QWidget* w = nullptr) const;
    virtual const QColor& labelCaptionForegroundColor(MouseState mouse) const;

    virtual const QColor& iconForegroundColor(MouseState mouse, ColorRole role) const;

    virtual const QColor& toolBarBackgroundColor() const;
    virtual const QColor& toolBarBorderColor() const;
    virtual const QColor& toolBarSeparatorColor() const;

    virtual const QColor& toolTipBackgroundColor() const;
    virtual const QColor& toolTipBorderColor() const;
    virtual const QColor& toolTipForegroundColor() const;

    virtual const QColor& scrollBarGrooveColor(MouseState mouse) const;
    virtual const QColor& scrollBarHandleColor(MouseState mouse) const;
    virtual int getScrollBarThickness(MouseState mouse) const;

    virtual const QColor& groupBoxTitleColor(
        MouseState mouse, const QWidget* w = nullptr) const;
    virtual const QColor& groupBoxBorderColor(MouseState mouse) const;
    virtual QColor groupBoxBackgroundColor(MouseState mouse) const;

    virtual const QColor& statusColor(Status status, MouseState mouse) const;
    virtual const QColor& statusColorForeground(Status status, MouseState mouse) const;
    virtual QColor focusBorderColor(Status status) const;
    virtual const QColor& frameBorderColor() const;
    virtual const QColor& separatorColor() const;

    virtual const QColor& colorForTextRole(TextRole role, MouseState mouse) const;
    virtual int pixelSizeForTextRole(TextRole role) const;
    virtual const QFont& fontForTextRole(TextRole role) const;
    virtual QPalette paletteForTextRole(TextRole role) const;

    virtual const QColor& switchGrooveColor(MouseState mouse, CheckState checked) const;
    virtual const QColor& switchGrooveBorderColor(
        MouseState mouse, FocusState focus, CheckState checked) const;
    virtual const QColor& switchHandleColor(MouseState mouse, CheckState checked) const;

    virtual const QColor& tableHeaderBgColor(MouseState mouse, CheckState checked) const;
    virtual const QColor& tableHeaderFgColor(MouseState mouse, CheckState checked) const;
    virtual const QColor& tableLineColor() const;

    virtual Status widgetStatus(const QWidget* widget) const;

    virtual const QColor& statusBarBackgroundColor() const;
    virtual const QColor& statusBarBorderColor() const;
    virtual const QColor& statusBarSeparatorColor() const;

    virtual const QColor& splitterColor(MouseState mouse) const;

signals:
    void themeChanged();
    void animationsEnabledChanged();
};

QlementineStyle* appStyle();

};
};
