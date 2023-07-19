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
            foreground=const.TEXT_COLOR,
            justify=tkinter.CENTER,
        )
        self.configure(background=const.BACKGROUND_COLOR)
