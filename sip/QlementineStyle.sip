%Import QtWidgets/QtWidgetsmod.sip

namespace oclero
{
namespace qlementine
{

class QlementineStyle : QCommonStyle
{

%TypeHeaderCode
#include <oclero/qlementine/style/QlementineStyle.hpp>
%End

public:
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

    QIcon makeThemedIcon(
        const QString& svgPath,
        const QSize& size = QSize(16, 16),
        ColorRole role = oclero::qlementine::ColorRole::Secondary) const;

    QIcon makeThemedIconFromName(
        const QString& name,
        const QSize& size = QSize(16, 16),
        ColorRole role = oclero::qlementine::ColorRole::Secondary) const;

signals:
    void themeChanged();
    void animationsEnabledChanged();
};

QlementineStyle* appStyle();

};
};
