qt_version := "6.8.1"
host := if os() == "macos" { "mac" } else if os() == "windows" { "windows" } else { "linux" }
export UV_NO_EDITABLE := "1"
export QT_VERSION := qt_version

@_default:
    just --list

# install dependencies and (re)-build the package
install: _clone _install-qt
    uv sync --reinstall-package pyqt6-qlementine

# Clean build artifacts
clean:
    rm -rf build dist wheelhouse Qt

# run demo widget
demo:
    uv run examples/demo.py

# build wheel (into ./wheelhouse)
build-wheel:
    uvx cibuildwheel --config-file pyproject.toml packages/PyQt6-Qlementine

_clone:
    git submodule update --init --recursive

_install-qt:
    #!/usr/bin/env sh
    if [ -d "Qt/{{ qt_version }}" ]; then
        echo "Qt {{ qt_version }} already installed"
    else
        uvx --from aqtinstall aqt install-qt {{ host }} desktop {{ qt_version }} --outputdir Qt
    fi
