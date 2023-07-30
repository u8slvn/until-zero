#!/usr/bin/python3
from __future__ import annotations

import argparse
import logging
import urllib.request
import zipfile

from pathlib import Path

import PyInstaller.__main__  # noqa


logger = logging.getLogger(__name__)

# ------ Build config ------
PACKAGE_NAME = "until_zero"
ASSETS_FOLDER = "assets"
UPX_VERSION = "4.0.2"

# ------ Build paths ------
BUILD_PATH = Path(__file__).parent.resolve()
PROJECT_PATH = BUILD_PATH.parent.resolve()
PACKAGE_PATH = PROJECT_PATH.joinpath(PACKAGE_NAME).resolve()
ASSETS_PATH = PACKAGE_PATH.joinpath(ASSETS_FOLDER)


def install_upx(version: str, os: str | None = None) -> Path:
    logger.info("Install UPX.")
    upx_filename = f"upx-{version}"
    upx_filename = f"{upx_filename}-{os}" if os is not None else upx_filename
    upx_zipfile = f"{upx_filename}.zip"
    upx_url = f"https://github.com/upx/upx/releases/download/v{version}/{upx_zipfile}"
    upx_path = BUILD_PATH.joinpath(upx_filename)

    logger.info(f"→ Downloading UPX: {upx_url}")
    urllib.request.urlretrieve(url=upx_url, filename=upx_zipfile)

    logger.info(f"→ Extract UPX to: {BUILD_PATH}")
    with zipfile.ZipFile(upx_zipfile, "r") as zip_ref:
        zip_ref.extractall(BUILD_PATH)

    return upx_path


def build_pyinstaller_args(
    package_version: str,
    os_name: str,
    arch: str,
    upx_path: Path | None = None,
) -> list[str]:
    logger.info("Build Pyinstaller args.")
    build_args = []
    output_name = f"until-zero-{package_version}-{os_name}-{arch}"
    script_entrypoint = f"{PACKAGE_NAME}/__main__.py"

    logger.info(f"→ entrypoint: {script_entrypoint}")
    build_args += [script_entrypoint]

    logger.info(f"→ Path to search for imports: {PACKAGE_PATH}")
    build_args += [f"-p {PACKAGE_PATH}"]

    logger.info(f"→ Spec file path: {BUILD_PATH}")
    build_args += ["--specpath", f"{BUILD_PATH}"]

    logger.info(f"→ Output exe filename: {output_name}")
    build_args += [f"-n {output_name}"]

    logger.info(f"→ Output file icon: {ASSETS_PATH.joinpath('icon-32.png')}")
    build_args += ["--icon", f"{ASSETS_PATH.joinpath('icon-32.png')}"]

    logger.info(f"→ Add assets folder: {ASSETS_PATH}")
    build_args += ["--add-data", f"{ASSETS_PATH};./{ASSETS_FOLDER}"]

    logger.info(f"→ Add splash image: {ASSETS_PATH.joinpath('splash.png')}")
    build_args += ["--splash", f"{ASSETS_PATH.joinpath('splash.png')}"]

    logger.info("→ Build options: onefile, noconsole, clean")
    build_args += [
        "--onefile",  # One compressed output file
        "--noconsole",  # Disable log window
        "--clean",  # Clean cache and remove temp files
    ]

    if upx_path is not None:
        logger.info(f"→ Upx path: {upx_path}")
        build_args += ["--upx-dir", f"{upx_path}"]

    return build_args


def run_pyinstaller(build_args: list[str]) -> None:
    PyInstaller.__main__.run(build_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Until Zero build script.")
    parser.add_argument(
        "--os",
        metavar="os",
        required=True,
        choices=["win32", "win64"],
        type=str,
    )

    args = parser.parse_args()

    os = args.os

    os_name = "windows"
    if os == "win32":
        arch = "x86"
    else:
        arch = "x64"

    upx_path = install_upx(version=UPX_VERSION, os=os)
    build_args = build_pyinstaller_args(
        package_version="0.1.0",
        os_name=os_name,
        arch=arch,
        upx_path=upx_path,
    )
    run_pyinstaller(build_args=build_args)
