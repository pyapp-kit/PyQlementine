"""Repair wheel file for CI (Linux only).

Applies the manylinux platform tag to Linux wheels. sipbuild already produces
manylinux-tagged wheels; scikit-build-core does not. This ensures both get the
correct tag for PyPI upload.

RECORD regeneration is handled at build time by project.py.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main() -> None:
    dest_dir, wheel, *_ = sys.argv[1:]
    wheel_path = Path(wheel)

    new_name = _manylinux_filename(wheel_path.name)
    new_wheel = Path(dest_dir) / new_name
    Path(dest_dir).mkdir(parents=True, exist_ok=True)

    if new_name == wheel_path.name:
        # Already tagged correctly — just copy to dest_dir.
        shutil.copy2(wheel, new_wheel)
    else:
        # Unpack and repack with the new filename.
        tmp_dir = wheel_path.parent / "tmp"
        shutil.unpack_archive(wheel, tmp_dir, format="zip")
        _zip_directory(tmp_dir, new_wheel)
        shutil.rmtree(tmp_dir)
        print(f"Retagged wheel: {wheel_path.name} -> {new_name}")


def _zip_directory(source_dir: Path, dest: Path) -> None:
    """Zip a directory into a wheel file."""
    with ZipFile(dest, "w", compression=ZIP_DEFLATED) as zf:
        for file in sorted(source_dir.rglob("*")):
            if file.is_dir():
                continue
            zf.write(file, file.relative_to(source_dir))


LINUX_PLAT_RE = re.compile(r"-linux_(x86_64|i686|aarch64)\.whl$")


def _manylinux_filename(filename: str) -> str:
    """Replace bare linux platform tag with manylinux, if needed."""
    match = LINUX_PLAT_RE.search(filename)
    if "manylinux" in filename or not match:
        return filename
    glibc = os.confstr("CS_GNU_LIBC_VERSION")  # e.g. "glibc 2.28"
    major, minor = glibc.split()[1].split(".")
    arch = match.group(1)
    tag = f"manylinux_{major}_{minor}_{arch}"
    return LINUX_PLAT_RE.sub(f"-{tag}.whl", filename)


if __name__ == "__main__":
    main()
