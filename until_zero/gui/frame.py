from __future__ import annotations

import tkinter

from until_zero import constants as const


class Frame(tkinter.Frame):
    def __init__(self, parent: tkinter.Tk, rows: int, columns: int):
        super().__init__(master=parent)
        self.rows = rows
        self.columns = columns
        self._configure_grid()
        self.configure(background=const.YELLOW)

    def _configure_grid(self):
        for row_index in range(self.rows):
            self.grid_rowconfigure(row_index, weight=1)
        for col_index in range(self.columns):
            self.grid_columnconfigure(col_index, weight=1)
