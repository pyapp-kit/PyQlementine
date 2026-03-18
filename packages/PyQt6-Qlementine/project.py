import os
import platform
import re
import shutil
import sys
from pathlib import Path

from pyqtbuild import PyQtBindings, PyQtProject, QmakeBuilder


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
    # small hack to make a custom __init__ file
    # not using Project.dunder_init... since that seems to affect PyQt6.__init__
    def install_project(self, target_dir, *, wheel_tag=None):
        super().install_project(target_dir, wheel_tag=wheel_tag)
        package = Path(target_dir, "PyQt6Qlementine")
        if os.name != "nt":
            contents = "from ._qlementine import *\n"
        else:
            contents = """\
try:
    import PyQt6  # force addition of Qt6/bin to dll_directories
except ImportError:
    raise ImportError("
        PyQt6 must be installed in order to use PyQt6Qlementine.
    ") from None

from ._qlementine import *
del PyQt6
"""
        (package / "__init__.py").write_text(contents)

        # rename _qlementine.pyi to __init__.pyi
        stubs = package / "_qlementine.pyi"
        stubs = stubs.rename(package / "__init__.pyi")

        # fix some errors in the stubs
        stubs_src = stubs.read_text()
        # replace erroneous [...*] syntax
        stubs_src = stubs_src.replace("*]", "]")
        stubs_src = stubs_src.replace(" Any", " typing.Any")
        # remove all of the ` = ...  # type: ` enum type hints
        stubs_src = re.sub(r"=\s*\.\.\.\s*#\s*type:\s*\S+", "= ...", stubs_src)

        stubs.write_text(stubs_src)
        if shutil.which("ruff"):
            import subprocess

            subprocess.run(
                ["ruff", "check", str(stubs), "--fix-only", "--select", "E,F,W,I,TC"]
            )
            subprocess.run(["ruff", "format", str(stubs), "--line-length", "110"])

        (package / "py.typed").touch()


class PyQt6Qlementine(PyQtProject):
    def __init__(self):
        super().__init__()
        self.builder_factory = _Builder
        self.bindings_factories = [PyQt6Qlementinemod]
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
