from __future__ import annotations

import tkinter

from typing import TYPE_CHECKING

from until_zero import constants as const


if TYPE_CHECKING:
    pass


class Frame(tkinter.Frame):
    def __init__(self, app, rows: int, columns: int):
        super().__init__(master=app)
        self.app = app
        self.rows = rows
        self.columns = columns
        self._configure_grid()
        self.configure(background=const.BACKGROUND_COLOR)

    def _configure_grid(self):
        for row_index in range(self.rows):
            self.grid_rowconfigure(row_index, weight=1)
        for col_index in range(self.columns):
            self.grid_columnconfigure(col_index, weight=1)
