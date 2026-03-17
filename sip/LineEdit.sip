namespace oclero
{
namespace qlementine
{

class LineEdit : QLineEdit
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/LineEdit.hpp>
%End

public:
    explicit LineEdit(QWidget* parent /TransferThis/ = nullptr);

    const QIcon& icon() const;

    void setUseMonoSpaceFont(bool useMonoSpaceFont);
    bool useMonoSpaceFont() const;

    Status status() const;

public slots:
    void setIcon(const QIcon& icon);
    void setStatus(Status status);

signals:
    void iconChanged();
    void statusChanged();
};

};
};
