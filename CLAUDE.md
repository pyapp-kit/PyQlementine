# PyQlementine

Python bindings for [Qlementine](https://github.com/oclero/qlementine), a modern
QStyle for desktop Qt applications. Qlementine is a complete `QStyle` subclass
(not QSS-based) that overrides Qt's default widget rendering with a consistent,
custom appearance. This project wraps that C++ library so it can be used from
Python with either PyQt6 or PySide6.

## Repo layout

This is a **uv-based monorepo**. The two publishable packages live under
`packages/`:

| Path | Binding tech | License |
| ---- | ------------ | ------- |
| `packages/PyQt6-Qlementine/` | SIP / PyQt-builder | GPL-3.0 (required by PyQt6) |
| `packages/PySide6-Qlementine/` | Shiboken6 / CMake (scikit-build-core) | MIT |

Other important directories:

- `qlementine/` — **git submodule** pointing at the upstream C++ repo.
  **Never edit files here directly.** See "Patches" below.
- `patches/` — plain `git diff` patches applied to the submodule at build time.
  (Standard unified diff format, **not** `git format-patch` / email format.)
- `tests/` — shared test suite; a compat shim (`tests/_qt_compat.py`) lets the
  same tests run against whichever backend is installed.
- `scripts/` — build helpers (wheel repair, etc.).
- `examples/` — demo scripts.

## Justfile

A `justfile` provides all commonly-used dev commands. **Prefer these over
hand-crafting build/install invocations:**

| Command | What it does |
| ------- | ------------ |
| `just install-pyqt6` | Build & install PyQt6-Qlementine into the venv |
| `just install-pyside6` | Build & install PySide6-Qlementine into the venv |
| `just build-wheel [PyQt6\|PySide6]` | Build a wheel via cibuildwheel (local) |
| `just clean` | Remove build/dist/wheelhouse artifacts |
| `just update-submodule [sha]` | Update submodule (default: `origin/dev`) |
| `just install-qt [version]` | Download Qt via aqtinstall |
| `just demo` | Run `examples/demo.py` |

## Building

**Local development:** `just install-pyqt6` or `just install-pyside6`.
These handle submodule init, patch application, and `uv pip install`.

**Wheel builds (CI-style):** `just build-wheel PyQt6` or
`just build-wheel PySide6` — runs cibuildwheel, which is also how CI produces
the published wheels. cibuildwheel config lives in the root `pyproject.toml`
under `[tool.cibuildwheel]`.

## Patches

The `qlementine/` submodule should **never** be edited in-place. To apply a fix
or experiment with upstream changes:

1. Create a standard unified diff (`git diff` output, **not** `--email` /
   `format-patch` format).
2. Save it in `patches/` with a descriptive name (e.g.
   `152-fix-lineedit-width-calculation.patch`).
3. Patches are applied automatically by `just _patch` (called during install /
   build).

## Binding details

Both packages expose the same public API surface — `QlementineStyle`, `Theme`,
widgets, enums, icon utilities, etc. — but use different code-generation
toolchains:

- **PyQt6**: `.sip` files in `packages/PyQt6-Qlementine/sip/` define the
  Python ↔ C++ interface. Built by `sip-build` via `project.py`.
- **PySide6**: `bindings.xml` + `bindings.h` define the type system for
  shiboken6. Built by CMake (`CMakeLists.txt`). Has a `dedup_enums.py` script
  to work around shiboken bug PYSIDE-3291.

Both packages generate `__init__.pyi` type stubs automatically.

## Versioning

Format: `X.Y.Z.B` where `X.Y.Z` tracks the upstream Qlementine version and `B`
is the Python-bindings build number (reset to 0 on upstream version bumps).
PyQt6 and PySide6 build numbers are independent.

## Testing

```sh
uv run pytest                           # run all tests
uv run pytest tests/test_style.py -v    # run a single test file
```

Tests use `pytest-qt` and `pytest-xvfb` (headless on Linux). The
`_qt_compat.py` shim auto-detects the installed backend.

## CI / release

- CI workflow: `.github/workflows/ci.yml` → calls `build-package.yml` for each
  backend. Builds wheels on Linux, macOS, and Windows via cibuildwheel.
- Publish: push a tag like `pyqt6/v1.4.3.0` or `pyside6/v1.4.3.0` to trigger
  PyPI upload via trusted publishing.
