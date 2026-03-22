namespace oclero
{
namespace qlementine
{

class Expander : QWidget
{

%TypeHeaderCode
#include <oclero/qlementine/widgets/Expander.hpp>
%End

public:
    explicit Expander(QWidget* parent /TransferThis/ = nullptr);

    bool expanded() const;
    void toggleExpanded();

    Qt::Orientation orientation() const;

    QWidget* content() const;
    void setContent(QWidget* content /Transfer/);

    QSize sizeHint() const;

public slots:
    void setExpanded(bool expanded);
    void setOrientation(Qt::Orientation orientation);

signals:
    void expandedChanged();
    void aboutToExpand();
    void aboutToShrink();
    void didExpand();
    void didShrink();
    void orientationChanged();
    void contentChanged();
};

};
};
