"""Thin wrapper around shiboken6-genpyi with bug workarounds.

shiboken6-genpyi has two bugs that prevent it from working on third-party
bindings out of the box:

1. find_imports() references a `PySide6` global that is only set when called
   from PySide6's own build (``_pyside_call=True``).  The CLI ``main()`` sets
   ``_pyside_call=False`` but still calls ``find_imports`` unconditionally.
   Fix: inject ``pyi_generator.PySide6 = PySide6`` before calling main().

2. On Python 3.10, ``layout.transform()`` converts ``Union[A, B]`` to
   ``A | B`` via ``operator.or_``, but ``ForwardRef.__or__`` was only added in
   Python 3.11.  The version guard (``>= 3.10``) is off by one.
   Fix: ``layout.create_signature = layout.create_signature_union``.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import PySide6
import PySide6Qlementine
import shiboken6  # noqa: F401 — activates the virtual shibokensupport module
from shibokensupport.signature import layout  # type: ignore
from shibokensupport.signature.lib import pyi_generator  # type: ignore

MODULE_NAME = "PySide6Qlementine"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate .pyi stubs")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    pkg_parent = Path(PySide6Qlementine.__file__).resolve().parent.parent

    # inject PySide6 global so find_imports() works
    pyi_generator.PySide6 = PySide6

    # skip transform() on Python < 3.11 (ForwardRef lacks __or__)
    if sys.version_info < (3, 11):
        layout.create_signature = layout.create_signature_union

    # shiboken6-genpyi expects <module>/ as a directory relative to --outpath
    sys.argv = [sys.argv[0], MODULE_NAME, "--outpath", str(pkg_parent)]
    pyi_generator.main()

    # shiboken writes <module>.pyi next to the package; move to outdir
    generated = pkg_parent / f"{MODULE_NAME}.pyi"
    if args.outdir:
        dest = Path(args.outdir) / "__init__.pyi"
    else:
        dest = Path(PySide6Qlementine.__file__).parent / "__init__.pyi"
    dest.parent.mkdir(parents=True, exist_ok=True)

    # -- post-process --
    text = generated.read_text()

    # Strip self-references: shiboken qualifies all names with the module name,
    # but inside __init__.pyi they should be unqualified.
    text = text.replace(f"import {MODULE_NAME}\n", "")
    text = text.replace(f"{MODULE_NAME}.", "")

    # Fix C++ type names that shiboken doesn't map to Python types
    text = text.replace(": double", ": float")

    # Shiboken emits ForwardRef('oclero.qlementine.Foo') for types it can't
    # resolve from the C++ namespace. Replace with the unqualified Python name.
    text = re.sub(
        r"ForwardRef\(['\"]oclero\.qlementine\.(\w+)['\"]\)",
        r"\1",
        text,
    )

    dest.write_text(text)
    generated.unlink()

    # Run ruff to clean up the generated stubs (best-effort)
    if ruff := shutil.which("ruff"):
        ruff_args = ["--target-version", "py310"]
        subprocess.run(
            [
                ruff,
                "check",
                *ruff_args,
                "--fix",
                "--unsafe-fixes",
                str(dest),
                "--select",
                "E,F,W,I,UP,RUF",
                "--ignore",
                "E501",
                "--quiet",
            ],
            check=False,
        )
        subprocess.run(
            [ruff, "format", *ruff_args, str(dest), "--line-length", "116"],
            check=False,
        )

    print(f"Wrote stubs to {dest}")


if __name__ == "__main__":
    main()
