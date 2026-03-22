namespace oclero
{
namespace qlementine
{

class AboutDialog : QDialog
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/AboutDialog.hpp>
%End

public:
    explicit AboutDialog(QWidget* parent /TransferThis/ = nullptr);
    virtual ~AboutDialog();

    void setIcon(const QIcon& icon);
    void setApplicationName(const QString& name);
    void setApplicationVersion(const QString& version);
    void setDescription(const QString& description);
    void setWebsiteUrl(const QString& url);
    void setLicense(const QString& license);
    void setCopyright(const QString& copyright);
    void addSocialMediaLink(const QString& name, const QString& url, const QIcon& icon = QIcon());
};

};
};
