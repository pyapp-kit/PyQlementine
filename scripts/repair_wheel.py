"""Delocate wheel file.

Sets the correct RPATH for Qt framework resolution at runtime.
PyQt6 wheels need @loader_path/../PyQt6/Qt6/lib
PySide6 wheels need @loader_path/../PySide6/Qt/lib plus PySide6 and shiboken6
"""

from __future__ import annotations

import csv
import hashlib
import io
import os
import re
import shutil
import sys
import sysconfig
from base64 import urlsafe_b64encode
from pathlib import Path
from subprocess import run
from zipfile import ZIP_DEFLATED, ZipFile

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

    # regenerate RECORD and repack the wheel
    _regenerate_record(tmp_dir)
    new_wheel = Path(dest_dir) / _manylinux_filename(Path(wheel).name)
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    _zip_directory(tmp_dir, new_wheel)
    shutil.rmtree(tmp_dir)
    print(f"Repaired wheel: {new_wheel}")


def _hash_file(path: Path) -> tuple[str, int]:
    """Return (sha256 digest in urlsafe-base64, file size) for a file."""
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
            size += len(chunk)
    digest = urlsafe_b64encode(h.digest()).rstrip(b"=").decode("ascii")
    return f"sha256={digest}", size


def _regenerate_record(unpacked_dir: Path) -> None:
    """Regenerate the RECORD file inside an unpacked wheel directory."""
    dist_info = next(unpacked_dir.glob("*.dist-info"))
    record_path = dist_info / "RECORD"

    rows: list[list[str]] = []
    for file in sorted(unpacked_dir.rglob("*")):
        if file.is_dir():
            continue
        rel = file.relative_to(unpacked_dir).as_posix()
        if rel == record_path.relative_to(unpacked_dir).as_posix():
            continue
        digest, size = _hash_file(file)
        rows.append([rel, digest, str(size)])

    # RECORD itself is listed with no hash
    rows.append([record_path.relative_to(unpacked_dir).as_posix(), "", ""])

    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerows(rows)
    record_path.write_text(buf.getvalue(), encoding="utf-8")


def _zip_directory(source_dir: Path, dest: Path) -> None:
    """Zip a directory into a wheel file (deterministic, no compression dirs)."""
    with ZipFile(dest, "w", compression=ZIP_DEFLATED) as zf:
        for file in sorted(source_dir.rglob("*")):
            if file.is_dir():
                continue
            zf.write(file, file.relative_to(source_dir))


LINUX_PLAT_RE = re.compile(r"-linux_(x86_64|i686|aarch64)\.whl$")


def _manylinux_filename(filename: str) -> str:
    """Replace bare linux platform tag with manylinux, if needed.

    sipbuild already produces manylinux-tagged wheels; scikit-build-core does
    not. This ensures both get the correct tag for PyPI upload.
    """
    match = LINUX_PLAT_RE.search(filename)
    if "manylinux" in filename or not match:
        return filename
    glibc = os.confstr("CS_GNU_LIBC_VERSION")  # e.g. "glibc 2.28"
    major, minor = glibc.split()[1].split(".")
    arch = match.group(1)
    tag = f"manylinux_{major}_{minor}_{arch}"
    new = LINUX_PLAT_RE.sub(f"-{tag}.whl", filename)
    print(f"Retagged wheel: {filename} -> {new}")
    return new


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
