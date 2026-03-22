"""Generate UtilsBridge.hpp from the PyQt6 SIP files.

Reads all .sip files in packages/PyQt6-Qlementine/sip/_utils/, extracts
function declarations, and emits a C++ header with a UtilsBridge class
that wraps each free function as a static method.

This keeps the SIP files as the single source of truth for which functions
are exposed and with what signatures.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SIP_DIR = REPO_ROOT / "packages" / "PyQt6-Qlementine" / "sip" / "_utils"
OUTPUT = Path(__file__).resolve().parents[1] / "UtilsBridge.hpp"

def _find_functions(text: str) -> list[tuple[str, str, str]]:
    """Extract function declarations, handling nested parens in defaults."""
    results: list[tuple[str, str, str]] = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith(("%", "#", "namespace", "}", "//")):
            continue
        if "(" not in line or not line.endswith(";"):
            continue
        line = line.rstrip(";").strip()
        # Find the first ( which starts the parameter list
        paren_start = line.index("(")
        # Walk forward to find the matching ) (handles nested parens)
        depth = 0
        close = -1
        for i in range(paren_start, len(line)):
            if line[i] == "(":
                depth += 1
            elif line[i] == ")":
                depth -= 1
                if depth == 0:
                    close = i
                    break
        if close < 0:
            continue
        prefix = line[:paren_start].strip()
        params = line[paren_start + 1 : close].strip()
        # Split prefix into return type and function name
        m = re.match(r"^(.*?)\s+(\w+)$", prefix)
        if m:
            results.append((m.group(1).strip(), m.group(2).strip(), params))
    return results

# Matches #include lines inside %TypeHeaderCode blocks
INCLUDE_RE = re.compile(r"^#include\s+[<\"](.+?)[>\"]", re.MULTILINE)


def parse_sip_file(path: Path) -> tuple[list[str], list[tuple[str, str, str]]]:
    """Parse a .sip file, returning (includes, functions).

    Each function is (return_type, name, params_string).
    """
    text = path.read_text()

    # Extract includes from %TypeHeaderCode blocks
    includes: list[str] = []
    for block in re.findall(r"%TypeHeaderCode\n(.*?)%End", text, re.DOTALL):
        for m in INCLUDE_RE.finditer(block):
            includes.append(m.group(1))

    # Extract function declarations (outside %TypeHeaderCode blocks)
    cleaned = re.sub(r"%TypeHeaderCode.*?%End", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"namespace\s+\w+\s*\{", "", cleaned)
    cleaned = cleaned.replace("};", "")

    # Join continuation lines (lines not ending with ; that continue a decl)
    joined_lines: list[str] = []
    for line in cleaned.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if joined_lines and not joined_lines[-1].endswith(";"):
            joined_lines[-1] += " " + stripped
        else:
            joined_lines.append(stripped)
    cleaned = "\n".join(joined_lines)

    functions = _find_functions(cleaned)
    return includes, functions


def format_call_args(params: str) -> str:
    """Extract argument names from a parameter list for forwarding."""
    if not params.strip():
        return ""
    args = []
    for param in _split_params(params):
        param = param.strip()
        # Remove default value
        param = re.sub(r"\s*=\s*.*$", "", param)
        # Extract the argument name (last identifier)
        # Handle: "const QColor& color", "QPainter* p", "qreal radius"
        m = re.search(r"(\w+)\s*$", param)
        if m:
            args.append(m.group(1))
    return ", ".join(args)


def _split_params(params: str) -> list[str]:
    """Split parameter list respecting nested parens/angle brackets."""
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in params:
        if ch in "(<":
            depth += 1
            current.append(ch)
        elif ch in ")>":
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current))
    return parts


def generate_bridge(
    all_includes: list[str],
    all_functions: list[tuple[str, str, str]],
) -> str:
    """Generate the UtilsBridge.hpp content."""
    lines = [
        "// UtilsBridge.hpp — AUTO-GENERATED from PyQt6 SIP files.",
        "// Do not edit manually. Run: scripts/generate_utils_bridge.py",
        "//",
        "// Wraps qlementine free functions as static methods so that shiboken6",
        "// can generate correct bindings (shiboken cannot handle namespace-level",
        "// free functions).",
        "",
        "#pragma once",
        "",
    ]

    # Deduplicate includes, keep order
    seen: set[str] = set()
    for inc in all_includes:
        if inc not in seen:
            seen.add(inc)
            lines.append(f"#include <{inc}>")
    # Always need QlementineStyle for appStyle
    if "oclero/qlementine/style/QlementineStyle.hpp" not in seen:
        lines.append("#include <oclero/qlementine/style/QlementineStyle.hpp>")

    lines.extend([
        "",
        "namespace oclero::qlementine {",
        "",
        "class UtilsBridge {",
        "public:",
        "    static QlementineStyle* appStyle() {",
        "        return oclero::qlementine::appStyle();",
        "    }",
    ])

    for ret_type, name, params in all_functions:
        call_args = format_call_args(params)
        if ret_type == "void":
            body = f"oclero::qlementine::{name}({call_args});"
        else:
            body = f"return oclero::qlementine::{name}({call_args});"

        # Format the static method
        lines.append(f"    static {ret_type} {name}({params}) {{")
        lines.append(f"        {body}")
        lines.append("    }")

    lines.extend([
        "};",
        "",
        "} // namespace oclero::qlementine",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    all_includes: list[str] = []
    all_functions: list[tuple[str, str, str]] = []

    for sip_file in sorted(SIP_DIR.glob("*.sip")):
        if sip_file.name.startswith("PyQt6"):
            continue  # skip the module definition file
        includes, functions = parse_sip_file(sip_file)
        all_includes.extend(includes)
        all_functions.extend(functions)

    content = generate_bridge(all_includes, all_functions)
    OUTPUT.write_text(content)
    print(f"Generated {OUTPUT} ({len(all_functions)} functions)")


if __name__ == "__main__":
    main()
