%Module(name=PyQt6Ads._ads, call_super_init=True, keyword_arguments="Optional", use_limited_api=True)
%HideNamespace(name=ads)

%Import QtCore/QtCoremod.sip
%DefaultSupertype PyQt6.sip.simplewrapper

%Include ads_globals.sip
%Include AutoHideDockContainer.sip
%Include AutoHideSideBar.sip
%Include AutoHideTab.sip
%Include DockWidget.sip
%Include DockAreaTabBar.sip
%Include DockAreaTitleBar_p.sip
%Include DockAreaTitleBar.sip
%Include DockAreaWidget.sip
%Include DockComponentsFactory.sip
%Include DockContainerWidget.sip
%Include DockingStateReader.sip
%Include DockFocusController.sip
%Include DockManager.sip
%Include DockOverlay.sip
%Include DockSplitter.sip
%Include DockWidgetTab.sip
%Include ElidingLabel.sip
%Include FloatingDockContainer.sip
%Include FloatingDragPreview.sip
%Include IconProvider.sip
%Include PushButton.sip
%Include ResizeHandle.sip
%If (Linux)
    %Include linux/FloatingWidgetTitleBar.sip
%End
