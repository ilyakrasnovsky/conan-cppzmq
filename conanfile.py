#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class CppZmqConan(ConanFile):
    name = "cppzmq"
    version = "4.3.0"
    url = "https://github.com/bincrafters/conan-cppzmq"
    description = "C++ binding for 0MQ"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = ['compiler', 'arch', 'os']

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def configure(self):
        """
        Configure prior to build.
        """

        # our linux version does not support conan-libsodium,
        # so we skip encryption until we build libsodium with HAVE_EXPLICIT_BZERO
        # not defined, or safely upgrade the glibc version on our target linux environment to > 2.23
        if (self.settings.os == "Linux"):
            self.options["zmq"].encryption = None

    def requirements(self):
        self.requires.add('zmq/4.2.4@idt/testing')

    def source(self):
        source_url = "https://github.com/zeromq/cppzmq"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        tools.replace_in_file(os.path.join(self.source_subfolder, 'CMakeLists.txt'),
                              'CMAKE_SOURCE_DIR',
                              'CMAKE_CURRENT_SOURCE_DIR')
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)

    def package_id(self):
        self.info.header_only()
