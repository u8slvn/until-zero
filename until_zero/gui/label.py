from __future__ import annotations

import tkinter

from until_zero import constants as const
from until_zero.constants import DEFAULT_SIZE


class Label(tkinter.Label):
    def __init__(
        self, master: tkinter.Misc, text: str, size: int = DEFAULT_SIZE, **kwargs
    ) -> None:
        super().__init__(
            master=master,
            text=text,
            font=(const.FONT, size),
            foreground=const.BLACK,
            background=const.YELLOW,
            **kwargs,
        )


class TimerLabel(tkinter.Label):
    def __init__(self, master: tkinter.Misc, text: str = "") -> None:
        super().__init__(
            master=master,
            text=text,
            font=(const.FONT, 10),
            foreground=const.WHITE,
            background=const.BLACK,
            justify=tkinter.CENTER,
        )

    def update_text(self, text: str) -> None:
        self.configure(text=text)
