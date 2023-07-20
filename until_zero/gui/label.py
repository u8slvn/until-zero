from __future__ import annotations

import tkinter

from until_zero import constants as const
from until_zero.constants import DEFAULT_SIZE


class Label(tkinter.Label):
    def __init__(self, master: tkinter.Misc, text: str, size: int = DEFAULT_SIZE) -> None:
        super().__init__(
            master=master,
            text=text,
            font=(const.FONT, size),
        )
        self.configure(foreground=const.BLACK, background=const.YELLOW)

    def update_text(self, text: str) -> None:
        self.configure(text=text)


class TimerLabel(Label):
    def __init__(self, master: tkinter.Misc, text: str, size: int = DEFAULT_SIZE) -> None:
        super().__init__(
            master=master,
            text=text,
            size=size,
        )
        self.configure(foreground=const.WHITE, background=const.BLACK, justify=tkinter.CENTER)
