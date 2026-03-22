host := if os() == "macos" { "mac" } else if os() == "windows" { "windows" } else { "linux" }
win_arch := if arch() == "aarch64" { "win64_msvc2022_arm64_cross_compiled" } else { "win64_msvc2022_64" }
win_msvc_arch := if arch() == "aarch64" { "arm64" } else { "amd64" }
export UV_NO_EDITABLE := "1"

set windows-shell := ["powershell.exe", "-NoProfile", "-NoLogo", "-Command"]

@_default:
    @just --list

# install (re)-build pyqt6-qlementine
[unix]
install-pyqt6: _clone install-qt
    uv sync --group pyqt6 --reinstall-package pyqt6-qlementine

[windows]
install-pyqt6: _clone install-qt
    just _vcvars uv sync --group pyqt6 --reinstall-package pyqt6-qlementine

# install (re)-build pyside6-qlementine
[unix]
install-pyside6: _clone (install-qt "6.10.2")
    uv sync --group pyside6 --reinstall-package pyside6-qlementine

[windows]
install-pyside6: _clone (install-qt "6.10.2")
    just _vcvars uv sync --group pyside6 --reinstall-package pyside6-qlementine

# Clean build artifacts
[unix]
clean:
    rm -rf build dist wheelhouse Qt
    rm -f aqtinstall.log

[windows]
clean:
    if (Test-Path build) { Remove-Item -Recurse -Force build }
    if (Test-Path dist) { Remove-Item -Recurse -Force dist }
    if (Test-Path wheelhouse) { Remove-Item -Recurse -Force wheelhouse }
    if (Test-Path Qt) { Remove-Item -Recurse -Force Qt }

# run demo widget
demo:
    uv run examples/demo.py

# build wheel (into ./wheelhouse)
[unix]
build-wheel target="PyQt6": _clone
    #!/usr/bin/env sh
    if echo "{{ target }}" | grep -qi pyside; then
        export QT_VERSION=6.10.2
    else
        export QT_VERSION=6.8.1
    fi
    just install-qt $QT_VERSION
    uvx cibuildwheel --config-file pyproject.toml packages/{{ target }}-Qlementine

[windows]
build-wheel target="PyQt6": _clone
    $qt_version = if ("{{ target }}" -match "(?i)pyside") { "6.10.2" } else { "6.8.1" }; \
    just install-qt qt_version=$qt_version; \
    uvx cibuildwheel --config-file pyproject.toml packages/{{ target }}-Qlementine

[unix]
install-qt qt_version="6.8.1":
    #!/usr/bin/env sh
    if [ -d "Qt/{{ qt_version }}" ]; then
        echo "Qt {{ qt_version }} already installed"
    else
        uvx --from aqtinstall aqt install-qt {{ host }} desktop {{ qt_version }} --outputdir Qt
    fi

[windows]
install-qt qt_version="6.8.1":
    if (Test-Path "Qt/{{ qt_version }}") { \
        Write-Host "Qt {{ qt_version }} already installed" \
    } else { \
        uvx --from aqtinstall aqt install-qt {{ host }} desktop {{ qt_version }} {{ win_arch }} --outputdir Qt \
    }

# point the qlementine submodule to a specific commit (default: origin/dev HEAD)
update-submodule sha="origin/dev":
    git -C qlementine fetch origin
    git -C qlementine checkout {{ sha }}
    git add qlementine

_clone:
    git submodule update --init --recursive
    @just _patch

# apply local patches to the qlementine submodule
[unix]
_patch:
    #!/usr/bin/env sh
    root="$(pwd)"
    for p in patches/*.patch; do
        [ -f "$p" ] || continue
        if git -C qlementine apply --check "$root/$p" 2>/dev/null; then
            git -C qlementine apply "$root/$p"
            echo "Applied $p"
        elif git -C qlementine apply --check -R "$root/$p" 2>/dev/null; then
            echo "Skipping $p (already applied)"
        else
            echo "ERROR: $p conflicts with current submodule state — patch needs updating" >&2
            exit 1
        fi
    done

# run a command inside the MSVC developer environment
[windows]
_vcvars +cmd:
    $ErrorActionPreference = 'Stop'; \
    $vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'; \
    if (-not (Test-Path $vswhere)) { throw "vswhere not found at $vswhere — is Visual Studio installed?" }; \
    $vsPath = & $vswhere -latest -property installationPath; \
    if (-not $vsPath) { throw "No Visual Studio installation found" }; \
    Import-Module (Join-Path $vsPath 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll'); \
    Enter-VsDevShell -VsInstallPath $vsPath -SkipAutomaticLocation -DevCmdArguments "-arch={{ win_msvc_arch }}" *>$null; \
    Invoke-Expression "{{ cmd }}"

[windows]
_patch:
    $root = (Get-Location).Path; \
    foreach ($p in Get-ChildItem -Path patches -Filter *.patch -ErrorAction SilentlyContinue) { \
        $pPath = $p.FullName; \
        $check = git -C qlementine apply --check $pPath 2>&1; \
        if ($LASTEXITCODE -eq 0) { \
            git -C qlementine apply $pPath; \
            Write-Host "Applied $($p.Name)" \
        } else { \
            $checkR = git -C qlementine apply --check -R $pPath 2>&1; \
            if ($LASTEXITCODE -eq 0) { \
                Write-Host "Skipping $($p.Name) (already applied)" \
            } else { \
                Write-Error "ERROR: $($p.Name) conflicts with current submodule state - patch needs updating"; \
                exit 1 \
            } \
        } \
    }

release tag:
    git tag -a "pyqt6/{{ tag }}" -m "pyqt6-qlementine {{ tag }}"
    git tag -a "pyside6/{{ tag }}" -m "pyside6-qlementine {{ tag }}"
    git push upstream --follow-tags
