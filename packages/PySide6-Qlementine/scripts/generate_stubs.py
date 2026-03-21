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

    # Split stubs into __init__.pyi (types) and utils.pyi (functions)
    init_pyi, utils_pyi = _split_stubs(text)

    dest.write_text(init_pyi)
    utils_dest = dest.parent / "utils.pyi"
    utils_dest.write_text(utils_pyi)
    generated.unlink()

    # Run ruff to clean up the generated stubs (best-effort)
    for stub_path in (dest, utils_dest):
        _run_ruff(stub_path)

    print(f"Wrote stubs to {dest} and {utils_dest}")


def _split_stubs(content: str) -> tuple[str, str]:
    """Split a flat .pyi into (__init__.pyi, utils.pyi).

    Classes/enums/imports + ``appStyle`` go to __init__.pyi.
    All other top-level ``def`` blocks go to utils.pyi.
    """
    lines = content.split("\n")
    init_lines: list[str] = []
    utils_lines: list[str] = []
    pending_decorators: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("@"):
            pending_decorators.append(line)
            i += 1
        elif line.startswith("def "):
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
            init_lines.extend(pending_decorators)
            pending_decorators.clear()
            init_lines.append(line)
            i += 1

    # utils.pyi needs the same import header plus re-import of our types
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

    init_pyi = init_pyi.rstrip() + "\n\nfrom . import utils as utils\n"

    return init_pyi, utils_pyi


def _run_ruff(path: Path) -> None:
    if not (ruff := shutil.which("ruff")):
        return
    ruff_args = ["--target-version", "py310"]
    subprocess.run(
        [
            ruff, "check", *ruff_args, "--fix", "--unsafe-fixes",
            str(path), "--select", "E,F,W,I,UP,RUF", "--ignore", "E501", "--quiet",
        ],
        check=False,
    )
    subprocess.run(
        [ruff, "format", *ruff_args, str(path), "--line-length", "116"],
        check=False,
    )


if __name__ == "__main__":
    main()
