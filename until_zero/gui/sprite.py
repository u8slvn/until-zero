from __future__ import annotations

import tkinter

from itertools import cycle
from typing import TYPE_CHECKING

from until_zero import constants as const
from until_zero.session import Events
from until_zero.session import session
from until_zero.tools import open_alpha_image


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


class BongoCat(Sprite):
    def __init__(self, parent: tkinter.Misc):
        frames = [
            open_alpha_image(const.ASSETS_DIR.joinpath("bongo-cat-0.png")),
            open_alpha_image(const.ASSETS_DIR.joinpath("bongo-cat-1.png")),
            open_alpha_image(const.ASSETS_DIR.joinpath("bongo-cat-2.png")),
        ]
        super().__init__(parent=parent, width=38, height=30, frames=frames, frame_rate=150)

        session.bind_event(Events.PAUSE_TIMER, self.on_pause)
        session.bind_event(Events.UNPAUSE_TIMER, self.on_unpause)
        session.bind_event(Events.TIMERS_STOPPED, self.on_pause)

    def on_pause(self, _: tkinter.Event) -> None:
        self.stop()

    def on_unpause(self, _: tkinter.Event) -> None:
        self.start()
