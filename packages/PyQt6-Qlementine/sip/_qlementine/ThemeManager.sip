namespace oclero
{
namespace qlementine
{

class ThemeManager : QObject
{

%TypeHeaderCode
#include <oclero/qlementine/style/ThemeManager.hpp>
%End

public:
    explicit ThemeManager(QlementineStyle* style, QObject* parent /TransferThis/ = nullptr);
    explicit ThemeManager(QObject* parent /TransferThis/ = nullptr);
    virtual ~ThemeManager();

    QlementineStyle* style() const;
    void setStyle(QlementineStyle* style);

    void addTheme(const Theme& theme);
    void loadDirectory(const QString& path);

    QString currentTheme() const;
    void setCurrentTheme(const QString& key);

    int themeCount() const;
    int themeIndex(const QString& key) const;
    int currentThemeIndex() const;
    void setCurrentThemeIndex(int index);

public slots:
    void setNextTheme();
    void setPreviousTheme();

signals:
    void currentThemeChanged();
    void themeCountChanged();
};

};
};
