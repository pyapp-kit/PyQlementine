cmake_minimum_required(VERSION 3.21)
project(PySide6Qlementine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# ---- Find Python ----
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# ---- Detect PySide6/Shiboken6 paths from Python ----
execute_process(
    COMMAND ${Python_EXECUTABLE} -c
        "import sysconfig; print(sysconfig.get_path('purelib'))"
    OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(PYSIDE6_DIR "${PYTHON_SITE_PACKAGES}/PySide6")
set(PYSIDE6_INCLUDE_DIR "${PYSIDE6_DIR}/include")
set(PYSIDE6_TYPESYSTEMS "${PYSIDE6_DIR}/typesystems")
set(SHIBOKEN6_DIR "${PYTHON_SITE_PACKAGES}/shiboken6")
set(SHIBOKEN6_GENERATOR_DIR "${PYTHON_SITE_PACKAGES}/shiboken6_generator")
# Headers may be in shiboken6_generator/include (6.8) or shiboken6/include (6.10+)
if(EXISTS "${SHIBOKEN6_GENERATOR_DIR}/include/shiboken.h")
    set(SHIBOKEN6_INCLUDE_DIR "${SHIBOKEN6_GENERATOR_DIR}/include")
else()
    set(SHIBOKEN6_INCLUDE_DIR "${SHIBOKEN6_DIR}/include")
endif()
set(SHIBOKEN6_BIN "${SHIBOKEN6_GENERATOR_DIR}/shiboken6")

# ---- Find Qt6 ----
# Auto-detect Qt from repo-level Qt/ directory (installed by aqtinstall)
set(REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../..")
file(GLOB QT_INSTALL_DIRS "${REPO_ROOT}/Qt/*/macos" "${REPO_ROOT}/Qt/*/gcc_64" "${REPO_ROOT}/Qt/*/msvc*")
foreach(dir ${QT_INSTALL_DIRS})
    list(APPEND CMAKE_PREFIX_PATH "${dir}")
endforeach()

# Patch deprecated AGL framework reference before finding Qt
# (AGL was removed in recent macOS SDKs)
if(APPLE)
    file(GLOB_RECURSE _fwo_files "${REPO_ROOT}/Qt/*/FindWrapOpenGL.cmake")
    foreach(_fwo ${_fwo_files})
        file(READ "${_fwo}" _fwo_content)
        string(FIND "${_fwo_content}" "AGL" _has_agl)
        if(NOT _has_agl EQUAL -1)
            string(REPLACE "find_library(WrapOpenGL_AGL NAMES AGL)" "" _fwo_content "${_fwo_content}")
            string(REPLACE "-framework AGL" "" _fwo_content "${_fwo_content}")
            file(WRITE "${_fwo}" "${_fwo_content}")
            message(STATUS "Patched AGL in ${_fwo}")
        endif()
    endforeach()
endif()

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
target_compile_options(qlementine_static PRIVATE -Wno-error -Wno-overloaded-virtual)

# ---- Run shiboken6 to generate wrapper sources ----
set(GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}/PySide6Qlementine")
file(MAKE_DIRECTORY ${GENERATED_DIR})

set(WRAPPED_HEADER "${CMAKE_CURRENT_SOURCE_DIR}/bindings.h")
set(TYPESYSTEM "${CMAKE_CURRENT_SOURCE_DIR}/bindings.xml")

# Get Qt include paths for shiboken
get_target_property(QT_CORE_INCLUDES Qt6::Core INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(QT_GUI_INCLUDES Qt6::Gui INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(QT_WIDGETS_INCLUDES Qt6::Widgets INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(QT_SVG_INCLUDES Qt6::Svg INTERFACE_INCLUDE_DIRECTORIES)

# Build include path arguments for shiboken
set(SHIBOKEN_INCLUDE_ARGS "")
foreach(inc ${QT_CORE_INCLUDES} ${QT_GUI_INCLUDES} ${QT_WIDGETS_INCLUDES} ${QT_SVG_INCLUDES})
    list(APPEND SHIBOKEN_INCLUDE_ARGS "-I${inc}")
endforeach()
list(REMOVE_DUPLICATES SHIBOKEN_INCLUDE_ARGS)

# Framework include paths for macOS
if(APPLE)
    get_target_property(QT_CORE_LOC Qt6::Core LOCATION)
    get_filename_component(QT_LIB_DIR ${QT_CORE_LOC} DIRECTORY)
    # Go up from QtCore.framework/Versions/A/QtCore to the lib dir
    get_filename_component(QT_LIB_DIR "${QT_LIB_DIR}/../../.." ABSOLUTE)
    set(SHIBOKEN_FRAMEWORK_ARGS "-F${QT_LIB_DIR}")
else()
    set(SHIBOKEN_FRAMEWORK_ARGS "")
endif()

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

add_custom_command(
    OUTPUT ${WRAPPER_SOURCES}
    COMMAND ${SHIBOKEN6_BIN}
        --generator-set=shiboken
        --enable-parent-ctor-heuristic
        --enable-pyside-extensions
        --enable-return-value-heuristic
        --use-isnull-as-nb-bool
        --avoid-protected-hack
        -I${QLEMENTINE_INCLUDE}
        -I${QLEMENTINE_PRIVATE_INCLUDE}
        -I${PYSIDE6_INCLUDE_DIR}
        ${SHIBOKEN_INCLUDE_ARGS}
        ${SHIBOKEN_FRAMEWORK_ARGS}
        -T${PYSIDE6_TYPESYSTEMS}
        -T${CMAKE_CURRENT_SOURCE_DIR}
        --output-directory=${CMAKE_CURRENT_BINARY_DIR}
        ${WRAPPED_HEADER}
        ${TYPESYSTEM}
    DEPENDS ${WRAPPED_HEADER} ${TYPESYSTEM}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Running shiboken6 to generate PySide6Qlementine wrappers"
)

# Build the Python extension module
Python_add_library(PySide6Qlementine MODULE ${WRAPPER_SOURCES})

target_include_directories(PySide6Qlementine PRIVATE
    ${GENERATED_DIR}
    ${QLEMENTINE_INCLUDE}
    ${QLEMENTINE_PRIVATE_INCLUDE}
    ${PYSIDE6_INCLUDE_DIR}
    ${PYSIDE6_INCLUDE_DIR}/QtCore
    ${PYSIDE6_INCLUDE_DIR}/QtGui
    ${PYSIDE6_INCLUDE_DIR}/QtWidgets
    ${PYSIDE6_INCLUDE_DIR}/QtSvg
    ${SHIBOKEN6_INCLUDE_DIR}
    ${Python_INCLUDE_DIRS}
)

# Link against libshiboken6/libpyside6 — the dylib ABI version (e.g. 6.8) is
# stable across all patch releases within a minor series, so we pin the runtime
# dependency to PySide6>=6.8,<6.9 to ensure the dylib name matches.
file(GLOB SHIBOKEN6_LIB "${SHIBOKEN6_DIR}/libshiboken6*${CMAKE_SHARED_LIBRARY_SUFFIX}")
file(GLOB PYSIDE6_LIB "${PYSIDE6_DIR}/libpyside6.abi3*${CMAKE_SHARED_LIBRARY_SUFFIX}")

# Force-load the static library to keep all symbols (moc staticMetaObjects etc.)
if(APPLE)
    target_link_libraries(PySide6Qlementine PRIVATE
        -Wl,-force_load $<TARGET_FILE:qlementine_static>
        Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Svg
        ${SHIBOKEN6_LIB} ${PYSIDE6_LIB}
    )
elseif(UNIX)
    target_link_libraries(PySide6Qlementine PRIVATE
        -Wl,--whole-archive qlementine_static -Wl,--no-whole-archive
        Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Svg
        ${SHIBOKEN6_LIB} ${PYSIDE6_LIB}
    )
else()
    target_link_libraries(PySide6Qlementine PRIVATE
        qlementine_static
        Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Svg
        ${SHIBOKEN6_LIB} ${PYSIDE6_LIB}
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

# Install
install(TARGETS PySide6Qlementine
    LIBRARY DESTINATION PySide6Qlementine
    RUNTIME DESTINATION PySide6Qlementine
)
