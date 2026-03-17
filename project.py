import os
import re
import shutil
from pathlib import Path

from pyqtbuild import PyQtBindings, PyQtProject, QmakeBuilder


class _Builder(QmakeBuilder):
    # small hack to make a custom __init__ file
    # not using Project.dunder_init... since that seems to affect PyQt6.__init__
    def install_project(self, target_dir, *, wheel_tag=None):
        super().install_project(target_dir, wheel_tag=wheel_tag)
        package = Path(target_dir, "PyQt6Ads")
        if os.name != "nt":
            contents = "from ._ads import *\n"
        else:
            contents = """
try:
    import PyQt6  # force addition of Qt6/bin to dll_directories
except ImportError:
    raise ImportError("PyQt6 must be installed in order to use PyQt6Ads.") from None

from ._ads import *
del PyQt6
            """
        (package / "__init__.py").write_text(contents)

        # rename _ads.pyi to __init__.pyi
        stubs = package / "_ads.pyi"
        stubs = stubs.rename(package / "__init__.pyi")

        # fix some errors in the stubs
        stubs_src = stubs.read_text()
        # replace erroneous [...*] syntax
        stubs_src = stubs_src.replace("*]", "]")
        stubs_src = stubs_src.replace(" Any", " typing.Any")
        # remove all of the ` = ...  # type: ` enum type hints
        stubs_src = re.sub(r"=\s*\.\.\.\s*#\s*type:\s*\S+", "= ...", stubs_src)

        stubs.write_text(stubs_src)
        if shutil.which("ruff"):
            import subprocess

            subprocess.run(
                ["ruff", "check", str(stubs), "--fix-only", "--select", "E,F,W,I,TC"]
            )
            subprocess.run(["ruff", "format", str(stubs), "--line-length", "110"])

        (package / "py.typed").touch()


class PyQt6Ads(PyQtProject):
    def __init__(self):
        super().__init__()
        self.builder_factory = _Builder
        self.bindings_factories = [PyQt6Adsmod]
        self.verbose = bool(os.getenv("CI") or os.getenv("CIBUILDWHEEL"))

    def apply_user_defaults(self, tool):
        if tool == "sdist":
            return super().apply_user_defaults(tool)
        qmake_path = "bin/qmake"
        if os.name == "nt":
            qmake_path += ".exe"
        try:
            qmake_bin = str(next(Path(self.root_dir).rglob(qmake_path)).absolute())
        except StopIteration:
            raise RuntimeError(
                "qmake not found.\n"
                "Please run `uvx --from aqtinstall aqt install-qt ...`"
            )
        print(f"USING QMAKE: {qmake_bin}")
        self.builder.qmake = qmake_bin
        return super().apply_user_defaults(tool)

    def build_wheel(self, wheel_directory):
        # use lowercase name for wheel, for
        # https://packaging.python.org/en/latest/specifications/binary-distribution-format/
        self.name = self.name.lower()
        return super().build_wheel(wheel_directory)


class PyQt6Adsmod(PyQtBindings):
    def __init__(self, project):
        super().__init__(project, "PyQt6Ads")

    def apply_user_defaults(self, tool):
        resource_file = os.path.join(
            self.project.root_dir, "Qt-Advanced-Docking-System", "src", "ads.qrc"
        )
        self.builder_settings.append("RESOURCES += " + resource_file)
        super().apply_user_defaults(tool)
