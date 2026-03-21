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

        # -- __init__.py: types + appStyle at top level ----------------------
        dll_preamble = ""
        if os.name == "nt":
            dll_preamble = """\
try:
    import PyQt6  # force addition of Qt6/bin to dll_directories
except ImportError:
    raise ImportError(
        "PyQt6 must be installed in order to use PyQt6Qlementine."
    ) from None
del PyQt6

"""
        (package / "__init__.py").write_text(
            dll_preamble + _INIT_PY.format(ext="_qlementine")
        )

        # -- utils.py: all free functions ------------------------------------
        (package / "utils.py").write_text(
            _UTILS_PY.format(ext="_qlementine")
        )

        # -- stubs -----------------------------------------------------------
        raw_pyi = package / "_qlementine.pyi"
        stubs_src = raw_pyi.read_text()
        raw_pyi.unlink()

        # fix known SIP stub bugs
        stubs_src = stubs_src.replace("*]", "]")
        stubs_src = stubs_src.replace(" Any", " typing.Any")
        stubs_src = re.sub(r"=\s*\.\.\.\s*#\s*type:\s*\S+", "= ...", stubs_src)

        init_pyi, utils_pyi = _split_stubs(stubs_src)
        (package / "__init__.pyi").write_text(init_pyi)
        (package / "utils.pyi").write_text(utils_pyi)

        _run_ruff(package / "__init__.pyi")
        _run_ruff(package / "utils.pyi")
        (package / "py.typed").touch()


# Template for __init__.py — types and promoted functions only.
# {ext} is the C extension module name (_qlementine or PySide6Qlementine).
_INIT_PY = """\
def _init():
    import types
    from . import {ext} as _ql

    ns = globals()
    _promoted = frozenset({{"appStyle"}})
    for name in dir(_ql):
        if name.startswith("_"):
            continue
        obj = getattr(_ql, name)
        if not isinstance(obj, types.BuiltinFunctionType) or name in _promoted:
            ns[name] = obj

_init()
del _init

from . import utils as utils
"""

# Template for utils.py — free functions only.
_UTILS_PY = """\
\"\"\"Qlementine utility functions.\"\"\"
def _init():
    import types
    from . import {ext} as _ql

    ns = globals()
    for name in dir(_ql):
        if name.startswith("_"):
            continue
        obj = getattr(_ql, name)
        if isinstance(obj, types.BuiltinFunctionType):
            ns[name] = obj

_init()
del _init
"""


def _split_stubs(content: str) -> tuple[str, str]:
    """Split a flat .pyi into (__init__.pyi, utils.pyi).

    Classes/enums/imports + ``appStyle`` go to __init__.pyi.
    All other top-level ``def`` blocks go to utils.pyi.
    """
    lines = content.split("\n")
    init_lines: list[str] = []
    utils_lines: list[str] = []

    # Pending decorator lines that precede a def
    pending_decorators: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("@"):
            # Collect decorator — destination depends on the following def
            pending_decorators.append(line)
            i += 1
        elif line.startswith("def "):
            # Collect full function block (may span multiple lines)
            block = [line]
            i += 1
            while i < len(lines) and lines[i].startswith((" ", "\t")):
                block.append(lines[i])
                i += 1

            func_name = line.split("(")[0].removeprefix("def ").strip()
            if func_name == "appStyle":
                init_lines.extend(pending_decorators)
                init_lines.extend(block)
            else:
                utils_lines.extend(pending_decorators)
                utils_lines.extend(block)
            pending_decorators.clear()
        else:
            # Flush any stray decorators (shouldn't happen, but be safe)
            init_lines.extend(pending_decorators)
            pending_decorators.clear()
            init_lines.append(line)
            i += 1

    # utils.pyi needs the same import header plus re-import of our types
    # Find the end of the import block in init
    header: list[str] = []
    for ln in init_lines:
        if ln.startswith(("import ", "from ", "#", "try:", "    ", "except")):
            header.append(ln)
        elif ln.strip() == "" and header:
            header.append(ln)
        else:
            break

    utils_header = "\n".join(header).rstrip() + "\n\nfrom . import *\n\n"
    init_pyi = "\n".join(init_lines)
    utils_pyi = utils_header + "\n".join(utils_lines) + "\n"

    # Add utils re-export to init
    init_pyi = init_pyi.rstrip() + "\n\nfrom . import utils as utils\n"

    return init_pyi, utils_pyi


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
