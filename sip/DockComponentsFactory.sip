%ModuleHeaderCode
  #include <Python.h>
  static PyObject* g_ads_factory_ref = nullptr;
%End

namespace ads
{

class CDockComponentsFactory
{
%TypeHeaderCode
#include <DockComponentsFactory.h>
%End

public:
  virtual ~CDockComponentsFactory();
  virtual CDockWidgetTab* createDockWidgetTab(CDockWidget* DockWidget /Transfer/) const;
  virtual CAutoHideTab* createDockWidgetSideTab(CDockWidget* DockWidget /Transfer/) const;
  virtual CDockAreaTabBar* createDockAreaTabBar(CDockAreaWidget* DockArea /Transfer/) const;
  virtual CDockAreaTitleBar* createDockAreaTitleBar(CDockAreaWidget* DockArea /Transfer/) const;

  static const CDockComponentsFactory* factory();
%MethodCode
    sipRes = ::ads::CDockComponentsFactory::factory().data();
%End

  static void setFactory(CDockComponentsFactory* Factory);
%MethodCode
    ::ads::CDockComponentsFactory::setFactory(a0);
    // print debug message
    printf("ads::CDockComponentsFactory::setFactory called\n");

    if (g_ads_factory_ref) {
        printf("ads::CDockComponentsFactory::setFactory: Releasing previous factory reference\n");
        Py_DECREF(g_ads_factory_ref);
        g_ads_factory_ref = nullptr;
    }

    PyObject *wrapper =
        sipConvertFromType(a0, sipType_ads_CDockComponentsFactory, nullptr);

    if (wrapper) {
        printf("ads::CDockComponentsFactory::setFactory: Setting new factory reference\n");
        Py_INCREF(wrapper);
        g_ads_factory_ref = wrapper;
    }
%End

  static void resetDefaultFactory();
%MethodCode
    ::ads::CDockComponentsFactory::resetDefaultFactory();

    if (g_ads_factory_ref) {
        Py_DECREF(g_ads_factory_ref);
        g_ads_factory_ref = nullptr;
    }
%End

};

};
