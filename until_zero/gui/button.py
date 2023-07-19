from __future__ import annotations

import tkinter

from until_zero import constants as const


class Button(tkinter.Button):
    def __init__(self, master: tkinter.Misc, text_size: int, **kwargs):
        super().__init__(master=master, font=(const.FONT, text_size), **kwargs)
        self.configure(relief=tkinter.GROOVE)


class BlueButton(Button):
    def __init__(self, master: tkinter.Misc, text_size: int, **kwargs):
        super().__init__(master=master, text_size=text_size, **kwargs)
        self.configure(
            foreground=const.BLUE_BTN_COLOR,
            activeforeground=const.BLUE_BTN_COLOR,
            background=const.BLUE_BTN_BG_COLOR,
            activebackground=const.BLUE_BTN_BG_ACTIVE_COLOR,
        )


class RedButton(Button):
    def __init__(self, master: tkinter.Misc, text_size: int, **kwargs):
        super().__init__(master=master, text_size=text_size, **kwargs)
        self.configure(
            foreground=const.RED_BTN_COLOR,
            activeforeground=const.RED_BTN_COLOR,
            background=const.RED_BTN_BG_COLOR,
            activebackground=const.RED_BTN_BG_ACTIVE_COLOR,
        )


class PurpleButton(Button):
    def __init__(self, master: tkinter.Misc, text_size: int, **kwargs):
        super().__init__(master=master, text_size=text_size, **kwargs)
        self.configure(
            foreground=const.PURPLE_BTN_COLOR,
            activeforeground=const.PURPLE_BTN_COLOR,
            background=const.PURPLE_BTN_BG_COLOR,
            activebackground=const.PURPLE_BTN_BG_ACTIVE_COLOR,
            relief=tkinter.GROOVE,
        )
