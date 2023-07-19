from __future__ import annotations

import tkinter

from typing import TYPE_CHECKING

from until_zero import constants as const


if TYPE_CHECKING:
    pass


class Draggable(tkinter.Frame):
    def __init__(self, parent, width: int) -> None:
        super().__init__(master=parent)
        self.parent = parent
        self.root = self.parent.winfo_toplevel()
        self.width = width
        self.pos_x = 0
        self.pos_y = 0
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = tkinter.Label(self, text="⋮", cursor="fleur", relief=tkinter.FLAT)
        self.label.configure(background=const.DRAGGABLE_BG)

        self.label.bind("<Button-1>", self.on_hold)
        self.label.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<B1-Motion>", self.on_drag)

        self.configure_component_grid()

    def configure_component_grid(self):
        self.label.grid(row=0, column=0, sticky=tkinter.NSEW)

    def on_hold(self, _: tkinter.Event) -> None:
        mouse_x, mouse_y = self.parent.winfo_pointerxy()
        _, root_x, root_y = self.root.geometry().split("+")
        self.pos_x = mouse_x - int(root_x)
        self.pos_y = mouse_y - int(root_y)

    def on_drag(self, event: tkinter.Event) -> None:
        x = event.x_root - self.pos_x - self.winfo_rootx() + self.winfo_rootx()
        y = event.y_root - self.pos_y - self.winfo_rooty() + self.winfo_rooty()

        self.parent.geometry("+%i+%i" % (x, y))

    def on_release(self, _: tkinter.Event) -> None:
        self.pos_x = 0
        self.pos_y = 0
