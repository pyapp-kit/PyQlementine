cmake_minimum_required(VERSION 3.21)
project(PySide6Qlementine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# ---- Find Python ----
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# ---- Detect site-packages for Shiboken6Tools ----
execute_process(
    COMMAND ${Python_EXECUTABLE} -c
        "import sysconfig; print(sysconfig.get_path('purelib'))"
    OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
# Shiboken6ToolsConfig.cmake auto-discovers PySide6/shiboken6 from here
list(APPEND CMAKE_PREFIX_PATH
    "${PYTHON_SITE_PACKAGES}/shiboken6_generator/lib/cmake"
)

# ---- Find Qt6 ----
# Auto-detect Qt from repo-level Qt/ directory (installed by aqtinstall)
set(REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../..")
file(GLOB QT_INSTALL_DIRS "${REPO_ROOT}/Qt/*/macos" "${REPO_ROOT}/Qt/*/gcc_64" "${REPO_ROOT}/Qt/*/msvc*")
foreach(dir ${QT_INSTALL_DIRS})
    list(APPEND CMAKE_PREFIX_PATH "${dir}")
endforeach()

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Svg)

# ---- Build qlementine static library ----
set(QLEMENTINE_SRC "${REPO_ROOT}/qlementine/lib")
set(QLEMENTINE_INCLUDE "${QLEMENTINE_SRC}/include")
set(QLEMENTINE_PRIVATE_INCLUDE "${QLEMENTINE_SRC}/src")

# Headers with Q_OBJECT (needed for AUTOMOC) - matching PyQt6 header list
set(QLEMENTINE_HEADERS
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/Common.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/animation/WidgetAnimationManager.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/animation/WidgetAnimator.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/style/Delegates.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/style/QlementineStyle.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/style/QlementineStyleOption.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/style/Theme.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/style/ThemeManager.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/tools/ThemeEditor.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/AboutDialog.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/AbstractItemListWidget.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/Action.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/ActionButton.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/ColorButton.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/ColorEditor.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/CommandLinkButton.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/Expander.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/IconWidget.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/Label.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/LineEdit.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/LoadingSpinner.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/Menu.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/NavigationBar.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/NotificationBadge.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/PlainTextEdit.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/Popover.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/PopoverButton.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/RoundedFocusFrame.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/SegmentedControl.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/StatusBadgeWidget.hpp
    ${QLEMENTINE_INCLUDE}/oclero/qlementine/widgets/Switch.hpp
    # Internal header with Q_OBJECT
    ${QLEMENTINE_PRIVATE_INCLUDE}/style/eventFilters/WidgetWithFocusFrameEventFilter.hpp
)

qt_add_library(qlementine_static STATIC
    ${QLEMENTINE_HEADERS}
    ${QLEMENTINE_SRC}/src/animation/WidgetAnimationManager.cpp
    ${QLEMENTINE_SRC}/src/animation/WidgetAnimator.cpp
    ${QLEMENTINE_SRC}/src/resources/ResourceInitialization.cpp
    ${QLEMENTINE_SRC}/src/style/Delegates.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/EventFilters_wrapper.cpp
    ${QLEMENTINE_SRC}/src/style/QlementineStyle.cpp
    ${QLEMENTINE_SRC}/src/style/Theme.cpp
    ${QLEMENTINE_SRC}/src/style/ThemeManager.cpp
    ${QLEMENTINE_SRC}/src/tools/ThemeEditor.cpp
    ${QLEMENTINE_SRC}/src/utils/BadgeUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/ColorUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/FontUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/GeometryUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/IconUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/ImageUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/LayoutUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/MenuUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/PrimitiveUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/RadiusesF.cpp
    ${QLEMENTINE_SRC}/src/utils/StateUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/StyleUtils.cpp
    ${QLEMENTINE_SRC}/src/utils/WidgetUtils.cpp
    ${QLEMENTINE_SRC}/src/widgets/AboutDialog.cpp
    ${QLEMENTINE_SRC}/src/widgets/AbstractItemListWidget.cpp
    ${QLEMENTINE_SRC}/src/widgets/Action.cpp
    ${QLEMENTINE_SRC}/src/widgets/ActionButton.cpp
    ${QLEMENTINE_SRC}/src/widgets/ColorButton.cpp
    ${QLEMENTINE_SRC}/src/widgets/ColorEditor.cpp
    ${QLEMENTINE_SRC}/src/widgets/CommandLinkButton.cpp
    ${QLEMENTINE_SRC}/src/widgets/Expander.cpp
    ${QLEMENTINE_SRC}/src/widgets/IconWidget.cpp
    ${QLEMENTINE_SRC}/src/widgets/Label.cpp
    ${QLEMENTINE_SRC}/src/widgets/LineEdit.cpp
    ${QLEMENTINE_SRC}/src/widgets/LoadingSpinner.cpp
    ${QLEMENTINE_SRC}/src/widgets/Menu.cpp
    ${QLEMENTINE_SRC}/src/widgets/NavigationBar.cpp
    ${QLEMENTINE_SRC}/src/widgets/NotificationBadge.cpp
    ${QLEMENTINE_SRC}/src/widgets/PlainTextEdit.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/Popover_patched.cpp
    ${QLEMENTINE_SRC}/src/widgets/PopoverButton.cpp
    ${QLEMENTINE_SRC}/src/widgets/RoundedFocusFrame.cpp
    ${QLEMENTINE_SRC}/src/widgets/SegmentedControl.cpp
    ${QLEMENTINE_SRC}/src/widgets/StatusBadgeWidget.cpp
    ${QLEMENTINE_SRC}/src/widgets/Switch.cpp
    # Qt resources
    ${QLEMENTINE_SRC}/resources/qlementine.qrc
    ${QLEMENTINE_SRC}/resources/qlementine_font_inter.qrc
    ${QLEMENTINE_SRC}/resources/qlementine_font_roboto.qrc
)
target_include_directories(qlementine_static
    PUBLIC ${QLEMENTINE_INCLUDE}
    PRIVATE ${QLEMENTINE_PRIVATE_INCLUDE}
)
target_link_libraries(qlementine_static PUBLIC Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Svg)
if(MSVC)
    target_compile_options(qlementine_static PRIVATE /W0)
else()
    target_compile_options(qlementine_static PRIVATE -Wno-error -Wno-overloaded-virtual)
endif()

# ---- Generate PySide6 bindings via Shiboken6Tools ----
find_package(Shiboken6Tools REQUIRED)

set(GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}/PySide6Qlementine")
set(WRAPPER_SOURCES
    ${GENERATED_DIR}/pyside6qlementine_module_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_aboutdialog_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_abstractitemlistwidget_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_actionbutton_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_colorbutton_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_coloreditor_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_commandlinkbutton_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_expander_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_iconwidget_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_label_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_lineedit_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_loadingspinner_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_menu_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_navigationbar_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_notificationbadge_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_plaintextedit_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_popover_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_popoverbutton_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_qlementinestyle_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_radiusesf_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_roundedfocusframe_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_segmentedcontrol_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_statusbadgewidget_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_switch_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_theme_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_thememanager_wrapper.cpp
    ${GENERATED_DIR}/oclero_qlementine_thememeta_wrapper.cpp
)

# Compute Qt framework search path for shiboken on macOS
# (the Shiboken6Tools macro computes this incorrectly for aqt-installed Qt)
set(SHIBOKEN_EXTRA "")
if(APPLE)
    get_target_property(_qtcore_loc Qt6::Core LOCATION)
    get_filename_component(_qt_fw_dir "${_qtcore_loc}/../../.." ABSOLUTE)
    get_filename_component(_qt_lib_dir "${_qt_fw_dir}/.." ABSOLUTE)
    list(APPEND SHIBOKEN_EXTRA "--framework-include-paths=${_qt_lib_dir}")
endif()

shiboken_generator_create_binding(
    EXTENSION_TARGET PySide6Qlementine
    GENERATED_SOURCES ${WRAPPER_SOURCES}
    HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/bindings.h
    TYPESYSTEM_FILE ${CMAKE_CURRENT_SOURCE_DIR}/bindings.xml
    LIBRARY_TARGET qlementine_static
    QT_MODULES Core Gui Widgets Svg
    SHIBOKEN_EXTRA_OPTIONS -I${QLEMENTINE_INCLUDE} ${SHIBOKEN_EXTRA}
    FORCE_LIMITED_API
)

# Work around shiboken6 bug: namespace-level enum converters are emitted once
# per wrapped type instead of once globally. Deduplicate after generation.
set(MODULE_WRAPPER "${GENERATED_DIR}/pyside6qlementine_module_wrapper.cpp")
set(DEDUP_STAMP "${GENERATED_DIR}/.dedup_stamp")
add_custom_command(
    OUTPUT ${DEDUP_STAMP}
    COMMAND ${Python_EXECUTABLE}
        "${CMAKE_CURRENT_SOURCE_DIR}/scripts/dedup_enums.py"
        "${MODULE_WRAPPER}"
    COMMAND ${CMAKE_COMMAND} -E touch "${DEDUP_STAMP}"
    DEPENDS ${MODULE_WRAPPER}
    COMMENT "Deduplicating enum converters in module wrapper"
)
add_custom_target(dedup_enums DEPENDS ${DEDUP_STAMP})
add_dependencies(PySide6Qlementine dedup_enums)

# Add generated wrapper dir to include path (for generated *_python.h headers)
target_include_directories(PySide6Qlementine PRIVATE ${GENERATED_DIR})

# Force-load the static library to keep all symbols (moc staticMetaObjects etc.)
if(APPLE)
    target_link_options(PySide6Qlementine PRIVATE
        "LINKER:-force_load,$<TARGET_FILE:qlementine_static>"
    )
elseif(UNIX)
    target_link_options(PySide6Qlementine PRIVATE
        "LINKER:--whole-archive" "$<TARGET_FILE:qlementine_static>" "LINKER:--no-whole-archive"
    )
endif()

# Set RPATH to find Qt/shiboken/pyside libs at runtime
if(APPLE)
    set_target_properties(PySide6Qlementine PROPERTIES
        INSTALL_RPATH "@loader_path/../PySide6/Qt/lib;@loader_path/../shiboken6;@loader_path/../PySide6"
        BUILD_WITH_INSTALL_RPATH OFF
    )
elseif(UNIX)
    set_target_properties(PySide6Qlementine PROPERTIES
        INSTALL_RPATH "$ORIGIN/../PySide6/Qt/lib:$ORIGIN/../shiboken6:$ORIGIN/../PySide6"
        BUILD_WITH_INSTALL_RPATH OFF
    )
endif()

# ---- Generate type stubs (.pyi) ----
# Stage the module so Python can import it, then run the stub generator.
# This mirrors how PySide6 itself generates stubs at build time.
set(STUB_STAGING "${CMAKE_CURRENT_BINARY_DIR}/_stub_staging")
set(STUB_PKG "${STUB_STAGING}/PySide6Qlementine")
set(STUB_OUTPUT "${STUB_PKG}/__init__.pyi")

add_custom_command(
    OUTPUT ${STUB_OUTPUT}
    COMMAND ${CMAKE_COMMAND} -E make_directory "${STUB_PKG}"
    COMMAND ${CMAKE_COMMAND} -E copy
        "${CMAKE_CURRENT_SOURCE_DIR}/PySide6Qlementine/__init__.py"
        "${STUB_PKG}/__init__.py"
    COMMAND ${CMAKE_COMMAND} -E create_symlink
        "$<TARGET_FILE:PySide6Qlementine>"
        "${STUB_PKG}/$<TARGET_FILE_NAME:PySide6Qlementine>"
    COMMAND ${CMAKE_COMMAND} -E env "PYTHONPATH=${STUB_STAGING}"
        "${Python_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_stubs.py"
        --outdir "${STUB_PKG}"
    DEPENDS PySide6Qlementine
    COMMENT "Generating type stubs for PySide6Qlementine"
)
add_custom_target(generate_stubs ALL DEPENDS ${STUB_OUTPUT})

# Install
install(TARGETS PySide6Qlementine
    LIBRARY DESTINATION PySide6Qlementine
    RUNTIME DESTINATION PySide6Qlementine
)
install(FILES ${STUB_OUTPUT} DESTINATION PySide6Qlementine)
