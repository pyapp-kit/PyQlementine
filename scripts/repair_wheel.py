"""Delocate wheel file.

Sets the correct RPATH for Qt framework resolution at runtime.
PyQt6 wheels need @loader_path/../PyQt6/Qt6/lib
PySide6 wheels need @loader_path/../PySide6/Qt/lib plus PySide6 and shiboken6
"""

from __future__ import annotations

import re
import shutil
import sys
import sysconfig
from pathlib import Path
from subprocess import run

# RPATH configurations per Qt binding package
RPATHS = {
    "PyQt6": {
        "darwin": ["@loader_path/../PyQt6/Qt6/lib"],
        "linux": ["$ORIGIN/../PyQt6/Qt6/lib"],
    },
    "PySide6": {
        "darwin": [
            "@loader_path/../PySide6/Qt/lib",
            "@loader_path/../shiboken6",
            "@loader_path/../PySide6",
        ],
        "linux": [
            "$ORIGIN/../PySide6/Qt/lib",
            "$ORIGIN/../shiboken6",
            "$ORIGIN/../PySide6",
        ],
    },
}


def detect_binding(wheel: str) -> str:
    """Detect whether this is a PyQt6 or PySide6 wheel from its filename."""
    name = Path(wheel).name.lower()
    if "pyside6" in name:
        return "PySide6"
    return "PyQt6"


def main() -> None:
    if sys.platform == "win32":
        return

    dest_dir, wheel, *_ = sys.argv[1:]
    binding = detect_binding(wheel)
    platform = "darwin" if sys.platform == "darwin" else "linux"
    rpaths = RPATHS[binding][platform]

    # unzip the wheel to a tmp directory
    tmp_dir = Path(wheel).parent / "tmp"
    shutil.unpack_archive(wheel, tmp_dir, format="zip")

    # fix the rpath in the tmp directory
    for so in Path(tmp_dir).rglob("*.so"):
        if sys.platform == "darwin":
            fix_rpath_macos(so, rpaths)
        else:
            fix_rpath_linux(so, rpaths)

    # re-zip the tmp directory and place it at dest_dir / wheel.name
    new_wheel = Path(dest_dir) / Path(wheel).name
    shutil.make_archive(new_wheel, "zip", tmp_dir)
    # remove the .zip extension
    shutil.move(f"{new_wheel}.zip", new_wheel)
    assert new_wheel.exists()
    print("Placed the repaired wheel at", new_wheel)


RPATH_RE_MAC = re.compile(r"^\s*path (.+) \(offset \d+\)$", re.MULTILINE)


def fix_rpath_macos(so: Path, new_rpaths: list[str]) -> None:
    # delete all current rpaths
    current_rpath = run(["otool", "-l", str(so)], capture_output=True, text=True)
    for rpath in RPATH_RE_MAC.findall(current_rpath.stdout):
        run(["install_name_tool", "-delete_rpath", rpath, so], check=True)

    # add new rpaths
    for rpath in new_rpaths:
        run(["install_name_tool", "-add_rpath", rpath, so], check=True)
    print(f"Updated RPATH for {so} to {new_rpaths}")


def fix_rpath_linux(so: Path, new_rpaths: list[str]) -> None:
    run(["patchelf", "--remove-rpath", str(so)], check=True)
    rpath_str = ":".join(new_rpaths)
    run(["patchelf", "--set-rpath", rpath_str, str(so)], check=True)
    print(f"Updated RPATH for {so} to {rpath_str}")


def fix_installed(binding: str = "PyQt6") -> None:
    """Fix RPATHs on an already-installed package in site-packages."""
    if sys.platform == "win32":
        return

    PKG_NAMES = {"PyQt6": "PyQt6Qlementine", "PySide6": "PySide6Qlementine"}
    pkg_dir = Path(sysconfig.get_path("purelib")) / PKG_NAMES[binding]
    if not pkg_dir.exists():
        raise FileNotFoundError(f"{pkg_dir} not found")

    platform = "darwin" if sys.platform == "darwin" else "linux"
    rpaths = RPATHS[binding][platform]
    for so in pkg_dir.rglob("*.so"):
        if sys.platform == "darwin":
            fix_rpath_macos(so, rpaths)
        else:
            fix_rpath_linux(so, rpaths)


if __name__ == "__main__":
    main()
