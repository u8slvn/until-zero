from __future__ import annotations

import tkinter

from itertools import cycle
from typing import TYPE_CHECKING

from until_zero import constants as const


if TYPE_CHECKING:
    from PIL import ImageTk


class Sprite(tkinter.Label):
    def __init__(
        self,
        parent: tkinter.Misc,
        width: int,
        height: int,
        frames: list[ImageTk.PhotoImage],
        frame_rate: int,
    ):
        super().__init__(master=parent, width=width, height=height)
        self.width = width
        self.height = height
        self._frames = frames
        self.frames = cycle(self._frames)
        self.frame_rate = frame_rate
        self.configure(background=const.YELLOW)
        self.stopped = False

        self.start()

    def _update_frame(self) -> None:
        if self.stopped is True:
            return

        next_frame = next(self.frames)
        self.configure(image=next_frame)
        self.after(self.frame_rate, self._update_frame)

    def start(self) -> None:
        self.stopped = False
        self._update_frame()

    def stop(self):
        self.stopped = True
