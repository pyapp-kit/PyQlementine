%Import QtWidgets/QtWidgetsmod.sip

namespace ads
{

class CIconProvider
{
%TypeHeaderCode
#include <IconProvider.h>
%End

public:
  CIconProvider();
  virtual ~CIconProvider();
  QIcon customIcon(eIcon IconId);
  void registerCustomIcon(eIcon IconId, const QIcon& icon /TransferThis/ );
};

};
