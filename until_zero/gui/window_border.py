from __future__ import annotations

import tkinter

from typing import TYPE_CHECKING

from until_zero import constants as const


if TYPE_CHECKING:
    pass


class WindowBorder(tkinter.Frame):
    def __init__(self, app) -> None:
        super().__init__(master=app, cursor="fleur")
        self.app = app
        self.root = self.app.winfo_toplevel()
        self.pos_x = 0
        self.pos_y = 0
        self.configure(background=const.WINDOW_BAR_BG)

        self.app.bind("<Button-1>", self.on_hold)
        self.app.bind("<ButtonRelease-1>", self.on_release)
        self.app.bind("<B1-Motion>", self.on_drag)

    def on_hold(self, event: tkinter.Event) -> None:
        self.pos_x = event.x
        self.pos_y = event.y

    def on_drag(self, event: tkinter.Event) -> None:
        x = event.x_root - self.pos_x - self.winfo_rootx() + self.winfo_rootx()
        y = event.y_root - self.pos_y - self.winfo_rooty() + self.winfo_rooty()

        self.app.geometry("+%i+%i" % (x, y))

    def on_release(self, _: tkinter.Event) -> None:
        self.pos_x = 0
        self.pos_y = 0
