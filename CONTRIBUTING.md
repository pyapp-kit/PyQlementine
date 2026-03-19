# Developers

This is a monorepo with two packages:

- `packages/PyQt6-Qlementine` — PyQt6 bindings (SIP/PyQt-builder)
- `packages/PySide6-Qlementine` — PySide6 bindings (Shiboken6/CMake)

## Quick start (using [just](https://github.com/casey/just))

```sh
just install-pyqt6    # build & install PyQt6-Qlementine package
just install-pyside6  # build & install PySide6-Qlementine package
```

Run tests

```sh
uv run pytest
```

## Build wheels with cibuildwheel

```sh
just build-wheel PyQt6
just build-wheel PySide6
```

## Updating the C++ sources

```sh
# optionally pass a specific sha
just update-submodule
```

### Applying patches

To experiment with bug fixes or new features in the C++ sources, you should NOT
modify the submodule code, but you can apply patches to the `qlementine/`
submodule by adding patches to the `patches/` directory. An example patch, that
would apply [PR 145](https://github.com/oclero/qlementine/pull/145) locally
would look like this:

```diff
diff --git a/lib/src/widgets/Expander.cpp b/lib/src/widgets/Expander.cpp
index d9bcc5f..9a6bf35 100644
--- a/lib/src/widgets/Expander.cpp
+++ b/lib/src/widgets/Expander.cpp
@@ -113,7 +113,7 @@ void Expander::setExpanded(bool expanded) {
 
     const auto isVertical = _orientation == Qt::Orientation::Vertical;
     const auto current = isVertical ? height() : width();
-    const auto contentSizeHint = _content->sizeHint();
+    const auto contentSizeHint = _content ? _content->sizeHint() : QSize{ 0, 0 };
     const auto target = _content && _expanded ? (isVertical ? contentSizeHint.height() : contentSizeHint.width()) : 0;
     const auto animationDuration = isVisible() ? style()->styleHint(QStyle::SH_Widget_Animation_Duration) : 0;
     _animation.stop();
```

then run `just install-pyqt6` or `just install-pyside6` to apply the patch
and rebuild/install the updated package locally.

## Release process

### Version format

The version format is `X.Y.Z.B` (e.g. `1.4.2.0`), where `X.Y.Z` is the version
of Qlementine that the package is based on, and `B` is the build number for the
Python bindings. The build number should be reset to `0` whenever the Qlementine
version is updated.  The build number need not be the same between the PyQt6 and
PySide6 packages.

### Publishing to PyPI

Deployment is automated in the `publish-pyqt6.yml` and `publish-pyside6.yml`
GitHub Actions workflows, which are triggered by pushing a git tag in the format,
and authenticated using PyPI trusted publishing:

- "pyqt6/v*" for PyQt6-Qlementine
- "pyside6/v*" for PySide6-Qlementine

Before creating and pushing a release tag, make sure to update the version in
`packages/PyQt6-Qlementine/pyproject.toml` or
`packages/PySide6-Qlementine/pyproject.toml` accordingly.

For example:

```sh
# after changing version in pyproject.toml, and committing the change,
# create git tags for both packages (if needed):
git tag -a "pyqt6/v1.4.2.0" -m "pyqt6-qlementine v1.4.2.0"
git tag -a "pyside6/v1.4.2.0" -m "pyside6-qlementine v1.4.2.0"
git push upstream --follow-tags
```
