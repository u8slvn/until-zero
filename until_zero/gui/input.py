from __future__ import annotations

import re
import tkinter

from typing import Callable

from until_zero import constants as const


class TimersInput(tkinter.Entry):
    # https://regex101.com/r/Mf1U4z/1
    EXTRACT_REG = re.compile(r"(?:(\d+)(?::(\d+))?\+?)")
    # https://regex101.com/r/svZXAc/1
    CHECK_REG = re.compile(r"^(((\d+):(\d?(?!\d+:\d+)))|(\d+(?<!\d{5}))\+?){1,40}$")

    def __init__(self, master: tkinter.Misc, update_callback: Callable[[], None]):
        self.input_var = tkinter.StringVar()
        self.input_var.trace("w", update_callback)
        super().__init__(
            master=master,
            justify=tkinter.CENTER,
            font=(const.FONT, const.DEFAULT_SIZE),
            textvariable=self.input_var,
        )
        input_validator = self.register(self.validate_timers_input)
        self.config(validate="key", validatecommand=(input_validator, "%P"))
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

    @classmethod
    def validate_timers_input(cls, value: str) -> bool:
        match = cls.CHECK_REG.match(value)
        return any(
            [
                match is not None and len(value) < const.TIMERS_INPUT_LENGTH,
                value == "",
            ]
        )

    def get_durations(self) -> list[int]:
        string = self.input_var.get()
        matches = self.EXTRACT_REG.findall(string)

        timers = []
        for match in matches:
            m, s = match
            timer = int(m) * 60
            timer += int(s) if s.isdigit() else 0
            timers.append(timer)

        return timers

    def clean(self) -> None:
        self.delete(0, tkinter.END)
        self.insert(0, "")
