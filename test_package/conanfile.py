import os
from pathlib import Path

from conans import CMake, ConanFile, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            bin_path = Path('bin') / 'test_package'
            script_path = Path(__file__).resolve()
            jsonnet_path = script_path.parent / 'sours.jsonnet'
            self.run(
                f"{bin_path} {jsonnet_path}",
                run_environment=True,
            )
