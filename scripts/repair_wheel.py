"""Delocate wheel file."""

import re
import sys
from subprocess import run
from pathlib import Path
import shutil


def main() -> None:
    if sys.platform == "win32":
        # nothing to do on non-Windows platforms
        return

    dest_dir, wheel, *_ = sys.argv[1:]

    # unzip the wheel to a tmp directory
    tmp_dir = Path(wheel).parent / "tmp"
    shutil.unpack_archive(wheel, tmp_dir, format="zip")

    # fix the rpath in the tmp directory
    for so in Path(tmp_dir).rglob("*.so"):
        if sys.platform == "darwin":
            fix_rpath_macos(so)
        else:
            fix_rpath_linux(so)

    # re-zip the tmp directory and place it at dest_dir / wheel.name
    new_wheel = Path(dest_dir) / Path(wheel).name
    shutil.make_archive(new_wheel, "zip", tmp_dir)
    # remove the .zip extension
    shutil.move(f"{new_wheel}.zip", new_wheel)
    assert new_wheel.exists()
    print("Placed the repaired wheel at", new_wheel)


RPATH_RE_MAC = re.compile(r"^\s*path (.+) \(offset \d+\)$", re.MULTILINE)


def fix_rpath_macos(so: Path, new_rpath: str = "@loader_path/../PyQt6/Qt6/lib") -> None:
    # delete all current rpaths
    current_rpath = run(["otool", "-l", str(so)], capture_output=True, text=True)
    for rpath in RPATH_RE_MAC.findall(current_rpath.stdout):
        run(["install_name_tool", "-delete_rpath", rpath, so], check=True)

    # add new rpath
    run(["install_name_tool", "-add_rpath", new_rpath, so], check=True)
    print(f"Updated RPATH for {so} to {new_rpath}")


def fix_rpath_linux(so: Path, new_rpath: str = "$ORIGIN/../PyQt6/Qt6/lib") -> None:
    # delete all current rpaths
    current_rpath = run(
        ["patchelf", "--print-rpath", str(so)], capture_output=True, text=True
    ).stdout.strip()

    # Remove the old RPATH and add the new one
    run(["patchelf", "--remove-rpath", str(so)], check=True)
    run(["patchelf", "--set-rpath", new_rpath, str(so)], check=True)

    print(f"Updated RPATH for {so} from {current_rpath} to {new_rpath}")


if __name__ == "__main__":
    main()
