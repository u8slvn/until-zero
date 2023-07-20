from __future__ import annotations

import tkinter

from typing import Callable

from until_zero import constants as const


class Input(tkinter.Entry):
    def __init__(self, master: tkinter.Misc, validate: str, update_callback: Callable[[], None]):
        self.input_var = tkinter.StringVar()
        self.input_var.trace("w", update_callback)
        super().__init__(
            master=master,
            justify=tkinter.CENTER,
            font=(const.FONT, const.DEFAULT_SIZE),
            textvariable=self.input_var,
        )
        self.config(validate="key", validatecommand=(validate, "%P"))
        self.configure(
            borderwidth=3,
            relief=tkinter.FLAT,
            background=const.BLACK,
            foreground=const.WHITE,
            insertbackground=const.WHITE,
        )

    def mark_as_valid(self) -> None:
        self.configure(foreground=const.WHITE)

    def mark_as_error(self) -> None:
        self.configure(foreground=const.RED)
