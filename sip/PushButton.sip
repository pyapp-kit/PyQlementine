%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CPushButton : QPushButton
{
%TypeHeaderCode
#include <PushButton.h>
%End
    
public:
  enum Orientation {
    Horizontal,
    VerticalTopToBottom,
    VerticalBottomToTop
  };
  virtual QSize sizeHint() const;
  
  CPushButton::Orientation buttonOrientation() const;
  void setButtonOrientation(CPushButton::Orientation orientation);
};

};
