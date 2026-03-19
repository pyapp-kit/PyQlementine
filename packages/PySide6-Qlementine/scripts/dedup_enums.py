"""Remove duplicate enum converter code from shiboken6 output.

Shiboken6 does not fully support nested invisible namespaces
(e.g. ``<namespace-type name="outer" visible="false">`` containing
``<namespace-type name="inner" visible="false">``).  One consequence is
that namespace-level enum converter functions and initialization blocks
are emitted multiple times in the module wrapper.  This script removes
the duplicates, keeping only the first occurrence.

See https://qt-project.atlassian.net/browse/PYSIDE-3291

Two patterns are deduplicated:
1. File-scope static converter functions (e.g. Enum_PythonToCpp_...)
2. Enum initialization blocks bounded by comment markers
   (e.g. // Initialization of enum 'X'. ... // End of 'X' enum.)
"""

from __future__ import annotations

import re
import sys


def dedup_module_wrapper(path: str) -> None:
    with open(path) as f:
        lines = f.readlines()

    seen_funcs: set[str] = set()
    seen_enums: set[str] = set()
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Pattern 1: file-scope static function definitions
        if line.startswith("static "):
            m = re.match(
                r"^static\s+(?:void|PyObject\s*\*|PythonToCppFunc)\s*"
                r"(\w+)\s*\(",
                line,
            )
            if m:
                name = m.group(1)
                if name in seen_funcs:
                    # Skip entire function body (brace counting).
                    # The opening { may be on this line or the next.
                    depth = line.count("{") - line.count("}")
                    i += 1
                    while i < len(lines):
                        depth += lines[i].count("{") - lines[i].count("}")
                        i += 1
                        if depth <= 0:
                            break
                    continue
                seen_funcs.add(name)

        # Pattern 2: enum initialization blocks inside registerEnums_*()
        m2 = re.match(r"\s+// Initialization of enum '(\w+)'\.", line)
        if m2:
            enum_name = m2.group(1)
            if enum_name in seen_enums:
                # Skip until "// End of '<enum_name>' enum."
                end_marker = f"// End of '{enum_name}' enum."
                i += 1
                while i < len(lines) and end_marker not in lines[i]:
                    i += 1
                i += 1  # skip the end marker line too
                continue
            seen_enums.add(enum_name)

        out.append(line)
        i += 1

    with open(path, "w") as f:
        f.writelines(out)


if __name__ == "__main__":
    dedup_module_wrapper(sys.argv[1])
