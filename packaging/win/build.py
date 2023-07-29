#!/usr/bin/python3
from __future__ import annotations

from pathlib import Path

import PyInstaller.__main__  # noqa

from PyInstaller.utils.hooks import copy_metadata


ROOT_PATH = Path(__file__).parent.parent.parent.resolve()

PACKAGE_NAME = "until_zero"
PACKAGE_PATH = ROOT_PATH.joinpath(PACKAGE_NAME).resolve()
PACKAGE_ENTRYPOINT = "__main__.py"
SPEC_PATH = ROOT_PATH.joinpath("packaging").resolve()
DIST_PATH = ROOT_PATH.joinpath("dist").resolve()

print(ROOT_PATH, PACKAGE_PATH)

OUTPUT_EXE_NAME = "until-zero"

build_args = []
datas = []
binaries = []

datas += copy_metadata(PACKAGE_NAME, recursive=True)

build_args += ["--specpath", str(SPEC_PATH)]

build_args += [
    f"{PACKAGE_NAME}/{PACKAGE_ENTRYPOINT}",
    "--onefile",
]

# Add package path
build_args += [
    f"-p {PACKAGE_PATH}",
]

# Manage debug options
build_args += [
    "--noconsole",  # Disable log window
    "--clean",  # Clean cache and remove temp files
]

# Set output name
output_exe_name = OUTPUT_EXE_NAME
build_args += [
    f"-n{output_exe_name}",
]

build_args += [
    "--icon",
    f"{PACKAGE_PATH.joinpath('assets/icon-32.png')}",
]

build_args += [
    "--add-data",
    f"{PACKAGE_PATH.joinpath('assets')};./assets",
]

PyInstaller.__main__.run(build_args)
