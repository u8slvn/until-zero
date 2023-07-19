from __future__ import annotations

import tkinter

from itertools import cycle
from pathlib import Path

from PIL import Image
from PIL import ImageTk

from until_zero import constants as const


class Sprite(tkinter.Label):
    def __init__(
        self,
        parent: tkinter.Misc,
        width: int,
        height: int,
        frames: list[Path],
        frame_rate: int,
    ):
        super().__init__(master=parent, width=width, height=height)
        self.width = width
        self.height = height
        self._frames = [self._open_frame(file) for file in frames]
        self.frames = cycle(self._frames)
        self.frame_rate = frame_rate
        self.configure(background=const.BACKGROUND_COLOR)

        self.start()

    @staticmethod
    def _open_frame(file: Path) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(Image.open(file).convert("RGBA"))

    def _update_frame(self) -> None:
        next_frame = next(self.frames)
        self.configure(image=next_frame)
        self.after(self.frame_rate, self._update_frame)

    def start(self) -> None:
        self._update_frame()
