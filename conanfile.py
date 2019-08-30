import os
from pathlib import Path

from conans import CMake, ConanFile, tools


class JsonnetConan(ConanFile):
    name = "jsonnet"
    version = "0.13.0"
    description = "Jsonnet - The data templating language"
    topics = ("json", "file-format")
    url = "https://github.com/rhololkeolke/conan-jsonnet"
    homepage = "https://jsonnet.org/"
    author = "Devin Schwab <dschwab@andrew.cmu.edu>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/google/jsonnet"
        tools.get(
            f"{source_url}/archive/v{self.version}.tar.gz",
            sha256="f6f0c4ea333f3423f1a7237a8a107c589354c38be8a2a438198f9f7c69b77596",
        )
        extracted_dir = f"{self.name}-{self.version}"

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.definitions["BUILD_STATIC_LIBS"] = not self.options.shared
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["USE_SYSTEM_GTEST"] = True
        cmake.definitions["BUILD_JSONNET"] = True
        cmake.definitions["BUILD_JSONNETFMT"] = True
        cmake.configure(build_folder=self._build_subfolder)

        # CMakeLists doesn't have the correct paths to the compiled
        # to_c_array binary when used as a subproject
        build_subfolder = Path(os.getcwd()) / self._build_subfolder
        bin_folder = build_subfolder / "bin"

        to_c_array = bin_folder / "to_c_array"
        to_c_array.touch()

        symlink_loc = build_subfolder / self._source_subfolder / "to_c_array"
        if not symlink_loc.exists():
            os.symlink(to_c_array, symlink_loc)

        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

        # Installer will copy both shared and static libs.  Delete
        # whichever one was not requested. Otherwise, when linking
        # against this package the shared objects will likely be used
        # even if a static library version was requested.
        package_folder = Path(self.package_folder)
        lib_folder = package_folder / "lib"
        if self.options.shared:
            lib_glob = "*.a*"
        else:
            lib_glob = "*.so*"
        for filepath in lib_folder.glob(lib_glob):
            filepath.unlink()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
