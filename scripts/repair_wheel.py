"""Repair wheel file for CI.

Applies the manylinux platform tag to Linux wheels (sipbuild already produces
manylinux-tagged wheels; scikit-build-core does not) and regenerates RECORD.

RPATH fixup is handled at build time by each package's build system:
- PyQt6-Qlementine: project.py _Builder.install_project()
- PySide6-Qlementine: CMakeLists.txt INSTALL_RPATH
"""

from __future__ import annotations

import csv
import hashlib
import io
import os
import re
import shutil
import sys
from base64 import urlsafe_b64encode
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main() -> None:
    if sys.platform == "win32":
        return

    dest_dir, wheel, *_ = sys.argv[1:]

    # unzip the wheel to a tmp directory
    tmp_dir = Path(wheel).parent / "tmp"
    shutil.unpack_archive(wheel, tmp_dir, format="zip")

    # regenerate RECORD and repack with the correct platform tag
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


if __name__ == "__main__":
    main()
