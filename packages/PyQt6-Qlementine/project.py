import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

from pyqtbuild import PyQtBindings, PyQtProject, QmakeBuilder

# Relative rpaths so the .so resolves Qt from PyQt6 at runtime.
_RPATHS = {
    "darwin": ["@loader_path/../PyQt6/Qt6/lib"],
    "linux": ["$ORIGIN/../PyQt6/Qt6/lib"],
}

RPATH_RE_MAC = re.compile(r"^\s*path (.+) \(offset \d+\)$", re.MULTILINE)


def fix_rpath_macos(so: Path, new_rpaths: list[str]) -> None:
    # delete all current rpaths
    current_rpath = subprocess.run(
        ["otool", "-l", str(so)], capture_output=True, text=True
    )
    for rpath in RPATH_RE_MAC.findall(current_rpath.stdout):
        subprocess.run(
            ["install_name_tool", "-delete_rpath", rpath, str(so)], check=True
        )

    # add new rpaths
    for rpath in new_rpaths:
        subprocess.run(["install_name_tool", "-add_rpath", rpath, str(so)], check=True)
    print(f"Updated RPATH for {so} to {new_rpaths}")


def fix_rpath_linux(so: Path, new_rpaths: list[str]) -> None:
    subprocess.run(["patchelf", "--remove-rpath", str(so)], check=True)
    rpath_str = ":".join(new_rpaths)
    subprocess.run(["patchelf", "--set-rpath", rpath_str, str(so)], check=True)
    print(f"Updated RPATH for {so} to {rpath_str}")


def fix_rpaths(package_dir: Path) -> None:
    """Fix rpaths on installed .so files to resolve Qt from PyQt6."""
    rpaths = _RPATHS["darwin" if sys.platform == "darwin" else "linux"]
    for so in package_dir.rglob("*.so"):
        if sys.platform == "darwin":
            fix_rpath_macos(so, rpaths)
        else:
            fix_rpath_linux(so, rpaths)


def _find_repo_root() -> Path:
    """Walk up from this file to find the repo root (contains qlementine/)."""
    d = Path(__file__).resolve().parent
    while d != d.parent:
        if (d / "qlementine").is_dir():
            return d
        d = d.parent
    raise RuntimeError("Could not find repo root (no qlementine/ directory found)")


_AGL_PATTERNS = [
    re.compile(r"\s*-framework\s+AGL\b"),
    re.compile(r";-framework AGL\b"),
    re.compile(r"\s*/System/Library/Frameworks/AGL\.framework/Headers/?"),
]


def _patch_agl_framework(qt_prefix: Path) -> None:
    """Remove references to the deprecated AGL framework from Qt config files."""
    targets = list(qt_prefix.rglob("mkspecs/**/*.conf"))
    targets += list(qt_prefix.rglob("mkspecs/**/*.pri"))
    targets += list(qt_prefix.rglob("lib/**/*.prl"))
    for path in targets:
        text = path.read_text()
        patched = text
        for pat in _AGL_PATTERNS:
            patched = pat.sub("", patched)
        if patched != text:
            print(f"Patching AGL references in {path}")
            path.write_text(patched)


class _Builder(QmakeBuilder):
    def install_project(self, target_dir, *, wheel_tag=None):
        super().install_project(target_dir, wheel_tag=wheel_tag)
        package = Path(target_dir, "PyQt6Qlementine")

        # -- __init__.py -----------------------------------------------------
        init_lines = []
        if os.name == "nt":
            init_lines.append(
                "try:\n"
                "    import PyQt6\n"
                "except ImportError:\n"
                '    raise ImportError("PyQt6 must be installed to use '
                'PyQt6Qlementine.") from None\n'
                "del PyQt6\n"
            )
        init_lines.append("from ._qlementine import *  # noqa: F403\n")
        init_lines.append("from . import utils as utils\n")
        (package / "__init__.py").write_text("\n".join(init_lines))

        # -- utils.py --------------------------------------------------------
        (package / "utils.py").write_text(
            '"""Qlementine utility functions."""\n'
            "from ._utils import *  # noqa: F403\n"
        )

        # -- stubs -----------------------------------------------------------
        for src_name, dest_name in [
            ("_qlementine.pyi", "__init__.pyi"),
            ("_utils.pyi", "utils.pyi"),
        ]:
            src = package / src_name
            if not src.exists():
                continue
            text = src.read_text()
            src.unlink()
            # fix known SIP stub bugs
            text = text.replace("*]", "]")
            text = text.replace(" Any", " typing.Any")
            text = re.sub(r"=\s*\.\.\.\s*#\s*type:\s*\S+", "= ...", text)
            dest = package / dest_name
            dest.write_text(text)
            _run_ruff(dest)

        # Add utils re-export to __init__.pyi
        init_pyi = package / "__init__.pyi"
        if init_pyi.exists():
            text = init_pyi.read_text().rstrip()
            text += "\n\nfrom . import utils as utils\n"
            init_pyi.write_text(text)

        # Add cross-import to utils.pyi
        utils_pyi = package / "utils.pyi"
        if utils_pyi.exists():
            text = utils_pyi.read_text()
            # Insert `from . import *` after the import block
            lines = text.split("\n")
            insert_idx = 0
            for i, ln in enumerate(lines):
                if ln.startswith(("import ", "from ", "#", "try:", "    ", "except")):
                    insert_idx = i + 1
                elif ln.strip() == "" and insert_idx:
                    insert_idx = i + 1
                else:
                    break
            lines.insert(insert_idx, "from . import *\n")
            utils_pyi.write_text("\n".join(lines))

        (package / "py.typed").touch()

        # Fix rpaths so the .so resolves Qt from PyQt6 at runtime.
        if sys.platform != "win32":
            fix_rpaths(package)


def _run_ruff(path: Path) -> None:
    if not shutil.which("ruff"):
        return
    import subprocess

    subprocess.run(
        ["ruff", "check", str(path), "--fix-only", "--select", "E,F,W,I,TC"],
        check=False,
    )
    subprocess.run(
        ["ruff", "format", str(path), "--line-length", "110"],
        check=False,
    )


class PyQt6Qlementine(PyQtProject):
    def __init__(self):
        super().__init__()
        self.builder_factory = _Builder
        self.bindings_factories = [PyQt6Qlementinemod, PyQt6QlementineUtilsmod]
        self.verbose = bool(os.getenv("CI") or os.getenv("CIBUILDWHEEL"))

    def apply_user_defaults(self, tool):
        if tool == "sdist":
            return super().apply_user_defaults(tool)
        repo_root = _find_repo_root()
        qmake_path = "bin/qmake"
        if os.name == "nt":
            qmake_path += ".exe"
        try:
            qmake_bin = str(next(repo_root.rglob(qmake_path)).absolute())
        except StopIteration:
            raise RuntimeError(
                "qmake not found.\n"
                "Please run `uvx --from aqtinstall aqt install-qt ...`"
            )
        print(f"USING QMAKE: {qmake_bin}")
        self.builder.qmake = qmake_bin

        # AGL framework was removed in newer macOS SDKs; patch Qt mkspecs
        if platform.system() == "Darwin":
            _patch_agl_framework(Path(qmake_bin).parents[1])

        return super().apply_user_defaults(tool)

    def build_wheel(self, wheel_directory):
        # use lowercase name for wheel, for
        # https://packaging.python.org/en/latest/specifications/binary-distribution-format/
        self.name = self.name.lower()
        return super().build_wheel(wheel_directory)


class PyQt6QlementineUtilsmod(PyQtBindings):
    def __init__(self, project):
        super().__init__(project, "PyQt6QlementineUtils")

    def apply_user_defaults(self, tool):
        self.builder_settings.append("CONFIG += c++17")
        if sys.platform == "win32":
            self.builder_settings.append("QMAKE_CXXFLAGS += /std:c++17 /W0")
        else:
            self.builder_settings.append(
                "QMAKE_CXXFLAGS += -std=c++17 -Wno-error -Wno-overloaded-virtual"
            )
        super().apply_user_defaults(tool)


class PyQt6Qlementinemod(PyQtBindings):
    def __init__(self, project):
        super().__init__(project, "PyQt6Qlementine")

    def apply_user_defaults(self, tool):
        repo_root = str(_find_repo_root())
        # add Qt resource files
        for qrc in [
            "qlementine/lib/resources/qlementine.qrc",
            "qlementine/lib/resources/qlementine_font_inter.qrc",
            "qlementine/lib/resources/qlementine_font_roboto.qrc",
        ]:
            resource_file = os.path.join(repo_root, qrc)
            self.builder_settings.append("RESOURCES += " + resource_file)

        # enable C++17 and suppress warnings from qlementine headers
        self.builder_settings.append("CONFIG += c++17")
        if sys.platform == "win32":
            self.builder_settings.append("QMAKE_CXXFLAGS += /std:c++17 /W0")
        else:
            self.builder_settings.append(
                "QMAKE_CXXFLAGS += -std=c++17 -Wno-error -Wno-overloaded-virtual"
            )

        super().apply_user_defaults(tool)
