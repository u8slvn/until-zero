from __future__ import annotations

import tkinter

from typing import Callable

from until_zero import constants as const
from until_zero.tools import open_alpha_image


BUTTON_THEMES = {
    "BLUE": {
        "foreground": const.BLACK,
        "activeforeground": const.BLACK,
        "background": const.BLUE,
        "activebackground": const.DARK_BLUE,
    },
    "RED": {
        "foreground": const.WHITE,
        "activeforeground": const.WHITE,
        "background": const.RED,
        "activebackground": const.DARK_RED,
    },
    "PURPLE": {
        "foreground": const.WHITE,
        "activeforeground": const.WHITE,
        "background": const.PURPLE,
        "activebackground": const.DARK_PURPLE,
    },
}


class Button(tkinter.Button):
    theme: dict[str, str]
    image_file: str

    def __init__(self, parent: tkinter.Misc, command: Callable[[], None], **kwargs):
        self.image = open_alpha_image(const.ASSETS_DIR.joinpath(self.image_file))
        super().__init__(master=parent, image=self.image, command=command, **kwargs)
        self.configure(relief=tkinter.GROOVE, **self.theme)


class StartButton(Button):
    theme = BUTTON_THEMES["RED"]
    image_file = "btn-start.png"


class ResetButton(Button):
    theme = BUTTON_THEMES["BLUE"]
    image_file = "btn-reset.png"


class PomodoroButton(Button):
    theme = BUTTON_THEMES["PURPLE"]


class TaskButton(PomodoroButton):
    image_file = "btn-task.png"


class ShortBreakButton(PomodoroButton):
    image_file = "btn-s-break.png"


class LongBreakButton(PomodoroButton):
    image_file = "btn-l-break.png"


class PauseButton(Button):
    theme = BUTTON_THEMES["PURPLE"]
    image_file = "btn-pause.png"


class StopButton(Button):
    theme = BUTTON_THEMES["RED"]
    image_file = "btn-stop.png"
