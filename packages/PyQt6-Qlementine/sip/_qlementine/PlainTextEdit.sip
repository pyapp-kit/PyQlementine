namespace oclero
{
namespace qlementine
{

class PlainTextEdit : QPlainTextEdit
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/PlainTextEdit.hpp>
%End

public:
    explicit PlainTextEdit(QWidget* parent /TransferThis/ = nullptr);

    QSize minimumSizeHint() const;
    QSize sizeHint() const;

    void setUseMonoSpaceFont(bool useMonoSpaceFont);
    bool useMonoSpaceFont() const;

    Status status() const;

public slots:
    void setStatus(Status status);

signals:
    void statusChanged();
};

};
};
