%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{
%TypeHeaderCode
#include <linux/FloatingWidgetTitleBar.h>
%End
    
class CFloatingWidgetTitleBar : QWidget
{

protected:
	virtual void mousePressEvent(QMouseEvent *ev);
	virtual void mouseReleaseEvent(QMouseEvent *ev);
	virtual void mouseMoveEvent(QMouseEvent *ev);
    virtual void mouseDoubleClickEvent(QMouseEvent *event);
    
    void setMaximizeIcon(const QIcon& Icon);
    QIcon maximizeIcon() const;
    void setNormalIcon(const QIcon& Icon);
    QIcon normalIcon() const;

public:
	explicit CFloatingWidgetTitleBar(CFloatingDockContainer *parent /TransferThis/ = 0);
	virtual ~CFloatingWidgetTitleBar();
	void enableCloseButton(bool Enable);
	void setTitle(const QString &Text);
    void updateStyle();
    void setMaximizedIcon(bool maximized);

signals:
	void closeRequested();
    void maximizeRequested();
};

};
