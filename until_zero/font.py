from __future__ import annotations

import sys

import pyglet  # type: ignore

from until_zero.constants import ASSETS_DIR


FONT_NAME = "CozetteVector"
FONT_PATH = ASSETS_DIR.joinpath(f"fonts/{FONT_NAME}.ttf")


def load_font() -> None:
    if sys.platform.startswith("win"):
        pyglet.options["win32_gdi_font"] = True
    pyglet.font.add_file(str(FONT_PATH))
