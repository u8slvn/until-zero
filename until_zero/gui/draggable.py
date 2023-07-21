from __future__ import annotations

import tkinter

from typing import TYPE_CHECKING

from until_zero import constants as const
from until_zero.tools import open_alpha_image


if TYPE_CHECKING:
    from until_zero.app import TimersWidget


class Draggable(tkinter.Label):
    def __init__(self, parent: TimersWidget, width: int) -> None:
        super().__init__(master=parent)
        self.parent = parent
        self.root = self.parent.winfo_toplevel()
        self.width = width
        self.pos_x = 0
        self.pos_y = 0
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.img = open_alpha_image(const.ASSETS_DIR.joinpath("drag.png"))
        self.configure(
            image=self.img,
            cursor="fleur",
            borderwidth=0,
            highlightthickness=0,
            font=(const.FONT, 15),
            background=const.DARK_YELLOW,
        )

        self.bind("<Button-1>", self.on_hold)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Double-Button-1>", self.reset_parent_pos)

    def on_hold(self, _: tkinter.Event) -> None:
        mouse_x, mouse_y = self.parent.winfo_pointerxy()
        dimension, root_x, root_y = self.root.geometry().split("+")
        self.pos_x = mouse_x - int(root_x)
        self.pos_y = mouse_y - int(root_y)

    def on_drag(self, event: tkinter.Event) -> None:
        x = event.x_root - self.pos_x - self.winfo_rootx() + self.winfo_rootx()
        y = event.y_root - self.pos_y - self.winfo_rooty() + self.winfo_rooty()

        self.parent.geometry("+%i+%i" % (x, y))

    def on_release(self, _: tkinter.Event) -> None:
        self.pos_x = 0
        self.pos_y = 0

    def reset_parent_pos(self, _: tkinter.Event) -> None:
        self.parent.position_window()
