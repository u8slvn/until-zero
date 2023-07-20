from __future__ import annotations

import tkinter

from until_zero import constants as const


class Button(tkinter.Button):
    def __init__(self, master: tkinter.Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        self.configure(relief=tkinter.GROOVE)


class BlueButton(Button):
    def __init__(self, master: tkinter.Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        self.configure(
            foreground=const.BLACK,
            activeforeground=const.BLACK,
            background=const.BLUE,
            activebackground=const.DARK_BLUE,
        )


class RedButton(Button):
    def __init__(self, master: tkinter.Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        self.configure(
            foreground=const.WHITE,
            activeforeground=const.WHITE,
            background=const.RED,
            activebackground=const.DARK_RED,
        )


class PurpleButton(Button):
    def __init__(self, master: tkinter.Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        self.configure(
            foreground=const.WHITE,
            activeforeground=const.WHITE,
            background=const.PURPLE,
            activebackground=const.DARK_PURPLE,
        )
