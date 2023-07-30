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
package_name = "until_zero"
assets_folder = "assets"
upx_version = "4.0.2"

# ------ Build paths ------
build_path = Path(__file__).parent.resolve()
project_path = build_path.parent.resolve()
package_path = project_path.joinpath(package_name).resolve()
assets_path = package_path.joinpath(assets_folder)


def install_upx(version: str, os: str | None = None) -> Path:
    logger.info("Install UPX.")
    upx_filename = f"upx-{version}"
    upx_filename = f"{upx_filename}-{os}" if os is not None else upx_filename
    upx_zipfile = f"{upx_filename}.zip"
    upx_url = f"https://github.com/upx/upx/releases/download/v{version}/{upx_zipfile}"
    upx_path = build_path.joinpath(upx_filename)

    logger.info(f"→ Downloading UPX: {upx_url}")
    urllib.request.urlretrieve(url=upx_url, filename=upx_zipfile)

    logger.info(f"→ Extract UPX to: {build_path}")
    with zipfile.ZipFile(upx_zipfile, "r") as zip_ref:
        zip_ref.extractall(build_path)

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
    script_entrypoint = f"{package_name}/__main__.py"

    logger.info(f"→ entrypoint: {script_entrypoint}")
    build_args += [script_entrypoint]

    logger.info(f"→ Path to search for imports: {package_path}")
    build_args += [f"-p {package_path}"]

    logger.info(f"→ Spec file path: {build_path}")
    build_args += ["--specpath", f"{build_path}"]

    logger.info(f"→ Output exe filename: {output_name}")
    build_args += [f"-n {output_name}"]

    logger.info(f"→ Output file icon: {assets_path.joinpath('icon-32.png')}")
    build_args += ["--icon", f"{assets_path.joinpath('icon-32.png')}"]

    logger.info(f"→ Add assets folder: {assets_path}")
    build_args += ["--add-data", f"{assets_path};./{assets_folder}"]

    # --- Setup build options
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

    upx_path = install_upx(version=upx_version, os=os)
    build_args = build_pyinstaller_args(
        package_version="0.1.0",
        os_name=os_name,
        arch=arch,
        upx_path=upx_path,
    )
    run_pyinstaller(build_args=build_args)
