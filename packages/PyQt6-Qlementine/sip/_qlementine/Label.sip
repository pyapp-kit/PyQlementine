namespace oclero
{
namespace qlementine
{

class Label : QLabel
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/Label.hpp>
%End

public:
    explicit Label(QWidget* parent /TransferThis/ = nullptr);
    explicit Label(const QString& text, TextRole role = oclero::qlementine::TextRole::Default, QWidget* parent /TransferThis/ = nullptr);
    virtual ~Label();

    TextRole role() const;

public slots:
    void setRole(TextRole role);

signals:
    void roleChanged();
};

};
};
