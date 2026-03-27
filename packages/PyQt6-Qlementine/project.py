import csv
import hashlib
import io
import os
import platform
import re
import shutil
import subprocess
import sys
from base64 import urlsafe_b64encode
from pathlib import Path

from pyqtbuild import PyQtBindings, PyQtProject, QmakeBuilder

# Relative rpaths so the .so resolves Qt from PyQt6 at runtime.
_RPATHS = {
    "darwin": ["@loader_path/../PyQt6/Qt6/lib"],
    "linux": ["$ORIGIN/../PyQt6/Qt6/lib"],
}

RPATH_RE_MAC = re.compile(r"^\s*path (.+) \(offset \d+\)$", re.MULTILINE)


def fix_rpath_macos(so: Path, new_rpaths: list[str]) -> None:
    current_rpath = subprocess.run(
        ["otool", "-l", str(so)], capture_output=True, text=True
    )
    for rpath in RPATH_RE_MAC.findall(current_rpath.stdout):
        subprocess.run(
            ["install_name_tool", "-delete_rpath", rpath, str(so)], check=True
        )
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


def _run_ruff(path: Path) -> None:
    if not shutil.which("ruff"):
        return
    subprocess.run(
        ["ruff", "check", str(path), "--fix-only", "--select", "E,F,W,I,TC"],
        check=False,
    )
    subprocess.run(
        ["ruff", "format", str(path), "--line-length", "110"],
        check=False,
    )


def _fix_pyi_stubs(pyi: Path) -> None:
    """Fix known SIP stub-generation bugs."""
    text = pyi.read_text()
    text = text.replace("*]", "]")
    text = text.replace(" Any", " typing.Any")
    text = re.sub(r"=\s*\.\.\.\s*#\s*type:\s*\S+", "= ...", text)
    pyi.write_text(text)
    _run_ruff(pyi)


def _generate_utils_pyi(init_pyi: Path, utils_pyi: Path) -> None:
    """Extract free-function stubs from __init__.pyi into utils.pyi.

    Copies only top-level ``def`` and ``@typing.overload`` lines (plus
    the import preamble) so that ``utils.pyi`` mirrors what
    ``utils.py`` re-exports at runtime.
    """
    lines = init_pyi.read_text().splitlines(keepends=True)
    imports: list[str] = []
    functions: list[str] = []
    in_class = False
    in_function = False

    for line in lines:
        stripped = line.rstrip()
        # Track class blocks (skip methods)
        if stripped.startswith("class "):
            in_class = True
            in_function = False
            continue
        if in_class:
            if stripped and not stripped[0].isspace():
                in_class = False
            else:
                continue

        # Collect import lines
        if stripped.startswith(("import ", "from ")):
            imports.append(line)
            continue

        # Collect top-level function defs and their decorators
        if stripped.startswith("@"):
            functions.append(line)
            continue
        if stripped.startswith("def "):
            in_function = True
            functions.append(line)
            continue
        # Continuation of a multi-line signature
        if in_function:
            functions.append(line)
            if stripped.endswith(":") or stripped == "...":
                in_function = False
            continue

    utils_pyi.write_text(
        "".join(imports) + "\nfrom . import *\n\n" + "".join(functions)
    )


def _regenerate_record(wheel_dir: Path) -> None:
    """Regenerate the RECORD file inside an unpacked wheel directory."""
    dist_info = next(wheel_dir.glob("*.dist-info"))
    record_path = dist_info / "RECORD"

    rows: list[list[str]] = []
    for file in sorted(wheel_dir.rglob("*")):
        if file.is_dir():
            continue
        rel = file.relative_to(wheel_dir).as_posix()
        if rel == record_path.relative_to(wheel_dir).as_posix():
            continue
        h = hashlib.sha256()
        size = 0
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
                size += len(chunk)
        digest = urlsafe_b64encode(h.digest()).rstrip(b"=").decode("ascii")
        rows.append([rel, f"sha256={digest}", str(size)])

    rows.append([record_path.relative_to(wheel_dir).as_posix(), "", ""])

    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerows(rows)
    record_path.write_text(buf.getvalue(), encoding="utf-8")


class _Builder(QmakeBuilder):
    def install_project(self, target_dir, *, wheel_tag=None):
        super().install_project(target_dir, wheel_tag=wheel_tag)
        package = Path(target_dir, "PyQt6Qlementine")

        # -- __init__.py -------------------------------------------------
        init = "from ._qlementine import *  # noqa: F403\n"
        if os.name == "nt":
            init = (
                "try:\n"
                "    import PyQt6\n"
                "except ImportError:\n"
                '    raise ImportError("PyQt6 must be installed to use '
                'PyQt6Qlementine.") from None\n'
                "del PyQt6\n\n" + init
            )
        init += "from . import utils as utils\n"
        (package / "__init__.py").write_text(init)

        # -- utils.py (re-export free functions from _qlementine) --------
        (package / "utils.py").write_text(
            '"""Qlementine utility functions."""\n\n\n'
            "def _init():\n"
            "    from . import _qlementine as _ql\n\n"
            "    ns = globals()\n"
            "    for name in dir(_ql):\n"
            "        if name.startswith('_'):\n"
            "            continue\n"
            "        obj = getattr(_ql, name)\n"
            "        if isinstance(obj, type):\n"
            "            continue\n"
            "        ns[name] = obj\n\n\n"
            "_init()\n"
            "del _init\n"
        )

        # -- stubs -------------------------------------------------------
        src_pyi = package / "_qlementine.pyi"
        init_pyi = package / "__init__.pyi"
        if src_pyi.exists():
            src_pyi.rename(init_pyi)
            _fix_pyi_stubs(init_pyi)

            # Generate utils.pyi from the function stubs
            utils_pyi = package / "utils.pyi"
            _generate_utils_pyi(init_pyi, utils_pyi)

            # Add utils re-export to __init__.pyi
            text = init_pyi.read_text().rstrip()
            text += "\n\nfrom . import utils as utils\n"
            init_pyi.write_text(text)

        (package / "py.typed").touch()

        # Fix rpaths so the .so resolves Qt from PyQt6 at runtime.
        if sys.platform != "win32":
            fix_rpaths(package)

        # Regenerate RECORD since we modified files after make install.
        _regenerate_record(Path(target_dir))


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

        if platform.system() == "Darwin":
            _patch_agl_framework(Path(qmake_bin).parents[1])

        return super().apply_user_defaults(tool)

    def build_wheel(self, wheel_directory):
        self.name = self.name.lower()
        return super().build_wheel(wheel_directory)


class PyQt6Qlementinemod(PyQtBindings):
    def __init__(self, project):
        super().__init__(project, "PyQt6Qlementine")

    def apply_user_defaults(self, tool):
        repo_root = str(_find_repo_root())
        for qrc in [
            "qlementine/lib/resources/qlementine.qrc",
            "qlementine/lib/resources/qlementine_font_inter.qrc",
            "qlementine/lib/resources/qlementine_font_roboto.qrc",
        ]:
            resource_file = os.path.join(repo_root, qrc)
            self.builder_settings.append("RESOURCES += " + resource_file)

        self.builder_settings.append("CONFIG += c++17")
        if sys.platform == "win32":
            self.builder_settings.append("QMAKE_CXXFLAGS += /std:c++17 /W0")
        else:
            self.builder_settings.append(
                "QMAKE_CXXFLAGS += -std=c++17 -Wno-error -Wno-overloaded-virtual"
            )

        super().apply_user_defaults(tool)
