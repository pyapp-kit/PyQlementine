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

    # Split stubs into __init__.pyi (types) and utils.pyi (functions).
    # shiboken6-genpyi may generate UtilsBridge as a class or skip it entirely.
    # Either way, _split_stubs handles both cases (extracts methods from class
    # or passes through top-level defs).
    init_pyi, utils_pyi = _split_stubs(text)

    # If no utils functions were extracted (shiboken skipped UtilsBridge),
    # generate them by introspecting the UtilsBridge class signatures.
    if utils_pyi.rstrip().endswith("from . import *"):
        utils_pyi = _generate_utils_stubs_from_bridge(utils_pyi)

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
    Top-level ``def`` blocks (except ``appStyle``) go to utils.pyi.
    The ``UtilsBridge`` class is unwrapped: its static methods are extracted
    as module-level ``def`` statements in utils.pyi (``appStyle`` is kept in
    __init__.pyi), and the class itself is excluded from __init__.pyi.
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
        elif line.startswith("class UtilsBridge"):
            # Extract static methods from UtilsBridge as module-level defs
            i += 1
            method_decorators: list[str] = []
            while i < len(lines) and (
                lines[i].startswith((" ", "\t")) or lines[i].strip() == ""
            ):
                inner = lines[i]
                stripped = inner.strip()
                if stripped == "":
                    i += 1
                    continue
                if stripped.startswith("@"):
                    # Keep @overload, drop @staticmethod
                    if "staticmethod" not in stripped:
                        method_decorators.append(stripped)
                    i += 1
                elif stripped.startswith("def "):
                    # Remove 'self' first arg if present, dedent to top level
                    dedented = stripped
                    method_block = [dedented]
                    i += 1
                    while i < len(lines) and lines[i].startswith((" ", "\t")):
                        # Dedent method body (8 spaces -> 4 spaces)
                        body = lines[i]
                        if body.startswith("        "):
                            body = body[4:]
                        method_block.append(body)
                        i += 1

                    func_name = dedented.split("(")[0].removeprefix("def ").strip()
                    if func_name == "appStyle":
                        init_lines.extend(method_decorators)
                        init_lines.extend(method_block)
                    else:
                        utils_lines.extend(method_decorators)
                        utils_lines.extend(method_block)
                    method_decorators.clear()
                else:
                    i += 1
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


def _generate_utils_stubs_from_bridge(header: str) -> str:
    """Generate utils.pyi by introspecting UtilsBridge static method signatures."""
    import inspect

    from shibokensupport.signature import get_signature  # type: ignore

    bridge = PySide6Qlementine.PySide6Qlementine.UtilsBridge
    lines = [header.rstrip(), ""]

    for name in sorted(dir(bridge)):
        if name.startswith("_") or name == "appStyle":
            continue
        obj = getattr(bridge, name)
        if not callable(obj):
            continue
        try:
            sigs = get_signature(obj)
        except Exception:
            lines.append(f"def {name}(*args, **kwargs): ...")
            continue

        if not isinstance(sigs, list):
            sigs = [sigs]

        entries: list[str] = []
        for sig in sigs:
            params: list[str] = []
            for pname, param in sig.parameters.items():
                if pname == "self":
                    continue
                ann = _format_annotation(param.annotation)
                if param.default is not inspect.Parameter.empty:
                    params.append(f"{pname}: {ann} = ...")
                else:
                    params.append(f"{pname}: {ann}")
            ret = _format_annotation(sig.return_annotation)
            if ret == "None":
                ret_str = " -> None"
            elif ret == "inspect.Parameter.empty":
                ret_str = ""
            else:
                ret_str = f" -> {ret}"
            entries.append(f"def {name}({', '.join(params)}){ret_str}: ...")

        if len(entries) > 1:
            for entry in entries:
                lines.append("@typing.overload")
                lines.append(entry)
        else:
            lines.extend(entries)

    return "\n".join(lines) + "\n"


def _format_annotation(ann: object) -> str:
    """Format a type annotation for stub output."""
    import inspect
    import types
    import typing

    if ann is inspect.Parameter.empty or ann is None:
        return "None"
    if ann is type(None):
        return "None"
    if isinstance(ann, str):
        return ann

    origin = getattr(ann, "__origin__", None)
    args = getattr(ann, "__args__", None)

    if origin is typing.Union or origin is types.UnionType:
        parts = [_format_annotation(a) for a in (args or ())]
        return " | ".join(parts)
    if origin is not None and args:
        origin_name = _format_annotation(origin)
        arg_strs = ", ".join(_format_annotation(a) for a in args)
        return f"{origin_name}[{arg_strs}]"

    if hasattr(ann, "__module__") and hasattr(ann, "__qualname__"):
        mod = ann.__module__
        name = ann.__qualname__
        # Strip module prefix for builtins and our own module
        if mod == "builtins":
            return name
        if mod == "PySide6Qlementine":
            return f'"{name}"'
        # Use PySide6 short names
        for prefix in ("PySide6.QtCore.", "PySide6.QtGui.", "PySide6.QtWidgets."):
            full = f"{mod}.{name}"
            if full.startswith(prefix):
                return full
        return f"{mod}.{name}"

    return str(ann)


def _run_ruff(path: Path) -> None:
    if not (ruff := shutil.which("ruff")):
        return
    ruff_args = ["--target-version", "py310"]
    subprocess.run(
        [
            ruff,
            "check",
            *ruff_args,
            "--fix",
            "--unsafe-fixes",
            str(path),
            "--select",
            "E,F,W,I,UP,RUF",
            "--ignore",
            "E501",
            "--quiet",
        ],
        check=False,
    )
    subprocess.run(
        [ruff, "format", *ruff_args, str(path), "--line-length", "116"],
        check=False,
    )


if __name__ == "__main__":
    main()
