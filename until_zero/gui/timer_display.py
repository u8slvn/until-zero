from __future__ import annotations

import tkinter

from until_zero import constants as const
from until_zero.gui.label import TimerLabel


class TimerDisplay(tkinter.Frame):
    def __init__(self, parent: tkinter.Misc, timer_count: int) -> None:
        super().__init__(master=parent)
        self.configure(background=const.BLACK)

        self.time_label = TimerLabel(self)
        self.time_label.configure(background=const.BLACK)
        self.timer_progress = TimersProgress(self, timer_count=timer_count)

        self._configure_component_grid()

    def _configure_component_grid(self) -> None:
        # --- row 0
        self.time_label.pack(fill="both", expand=True)
        # --- row 1
        self.timer_progress.pack(fill="both", expand=True, padx=2)

    def update_labels(self, time: str, timer_index: int) -> None:
        self.time_label.update_text(text=time)
        self.timer_progress.update_progress(timer_index=timer_index)


class TimersProgress(tkinter.Canvas):
    def __init__(self, parent: tkinter.Misc, timer_count: int) -> None:
        self.height = 2
        super().__init__(master=parent, height=self.height, highlightthickness=0, relief="ridge")
        self.configure(background=const.BLACK, border=0)
        self.timer_count = timer_count
        self.separator = 2

    def update_progress(self, timer_index: int) -> None:
        self.update_idletasks()
        width = self.winfo_width()
        rect_size = (width - (self.timer_count - 1) * self.separator) / self.timer_count
        x = 0.0
        for i in range(self.timer_count):
            if i > (self.timer_count - timer_index):
                fill = const.BLUE
            elif i == (self.timer_count - timer_index):
                fill = const.PURPLE
            else:
                fill = const.WHITE

            self.create_rectangle(x, 0, x + rect_size, self.height, fill=fill, outline="")
            x += rect_size + self.separator
