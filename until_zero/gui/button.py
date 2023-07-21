from __future__ import annotations

import tkinter

from functools import partial
from typing import Callable

from until_zero import constants as const
from until_zero.session import Events
from until_zero.session import session
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


class CleanButton(Button):
    theme = BUTTON_THEMES["BLUE"]
    image_file = "btn-reset.png"


class PomodoroButton(Button):
    theme = BUTTON_THEMES["PURPLE"]
    duration: int

    def __init__(self, parent: tkinter.Misc, command: Callable[[], None], **kwargs):
        super().__init__(parent=parent, command=partial(command, self.duration), **kwargs)


class TaskButton(PomodoroButton):
    image_file = "btn-task.png"
    duration = const.OPTION_TASK


class ShortBreakButton(PomodoroButton):
    image_file = "btn-s-break.png"
    duration = const.OPTION_SHORT_BREAK


class LongBreakButton(PomodoroButton):
    image_file = "btn-l-break.png"
    duration = const.OPTION_LONG_BREAK


class PauseReplayButton(Button):
    theme = BUTTON_THEMES["PURPLE"]
    image_file = "btn-pause.png"

    def __init__(self, parent: tkinter.Misc, command: Callable[[], None], **kwargs):
        super().__init__(parent=parent, command=command, **kwargs)
        self.image_play = open_alpha_image(const.ASSETS_DIR.joinpath("btn-play.png"))
        self.image_replay = open_alpha_image(const.ASSETS_DIR.joinpath("btn-replay.png"))
        self._status = "play"

        session.bind_event(Events.PAUSE_TIMER, self.on_pause)
        session.bind_event(Events.UNPAUSE_TIMER, self.on_unpause)
        session.bind_event(Events.TIMERS_STOPPED, self.on_timers_stop)

    def on_pause(self, _: tkinter.Event) -> None:
        self.configure(image=self.image_play)

    def on_unpause(self, _: tkinter.Event) -> None:
        self.configure(image=self.image)

    def on_timers_stop(self, _: tkinter.Event) -> None:
        self.configure(image=self.image_replay)


class StopButton(Button):
    theme = BUTTON_THEMES["RED"]
    image_file = "btn-stop.png"
