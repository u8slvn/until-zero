from __future__ import annotations

import tkinter

from functools import partial

from until_zero import constants as const
from until_zero.gui.button import BlueButton
from until_zero.gui.button import PurpleButton
from until_zero.gui.button import RedButton
from until_zero.gui.draggable import Draggable
from until_zero.gui.frame import Frame
from until_zero.gui.input import Input
from until_zero.gui.label import Label
from until_zero.gui.label import TimerLabel
from until_zero.gui.sprite import Sprite
from until_zero.tools import StepTimer
from until_zero.tools import format_timer_for_human
from until_zero.tools import open_alpha_image


class App(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.timers: list[int] = []
        self.width = const.WINDOW_WIDTH
        self.height = const.WINDOW_HEIGHT

        self.geometry(f"{self.width}x{self.height}")
        self.title(const.WINDOW_TITLE)
        self.resizable(width=False, height=False)
        self.configure(background=const.YELLOW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.position_window()

        self.config_timers = ConfigTimers(app=self)
        self.config_timers.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.run_timers: TimersWidget | None = None

    def position_window(self):
        self.update()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry("+%d+%d" % (x, y))

    def get_next_timer(self) -> StepTimer | None:
        if len(self.timers) > 0:
            return StepTimer(duration=self.timers.pop(0))
        return None

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()


class ConfigTimers(Frame):
    def __init__(self, app: App):
        super().__init__(app=app, rows=5, columns=3)

        self.reset_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-reset.png"))
        self.task_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-task.png"))
        self.s_break_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-s-break.png"))
        self.l_break_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-l-break.png"))
        self.start_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-start.png"))

        # --- Row 0
        self.steps_label = Label(self, text="STEPS:")
        self.clean_btn = BlueButton(self, image=self.reset_img, command=self.clean)
        # -- Row 1
        self.timers_input = Input(
            self,
            update_callback=self.update_total,
        )
        # -- Row 2
        self.total_label = Label(self, text=const.SUM_TIMERS_PLACEHOLDER, size=10)
        # -- Row 3
        self.task_btn = PurpleButton(
            self,
            image=self.task_img,
            command=partial(self.add_option, const.OPTION_TASK),
        )
        self.short_break_btn = PurpleButton(
            self,
            image=self.s_break_img,
            command=partial(self.add_option, const.OPTION_SHORT_BREAK),
        )
        self.long_break_btn = PurpleButton(
            self,
            image=self.l_break_img,
            command=partial(self.add_option, const.OPTION_LONG_BREAK),
        )
        # -- Row 4
        self.start_button = RedButton(self, image=self.start_img, command=self.start_timers)

        self.timers_input.bind("<Return>", self.start_timers)

        self.configure_component_grid()

    def configure_component_grid(self):
        self.steps_label.grid(row=0, column=0, padx=5, pady=0, sticky=tkinter.W)
        self.clean_btn.grid(row=0, column=2, padx=5, pady=0, sticky=tkinter.E)
        self.timers_input.grid(row=1, column=0, columnspan=3, padx=2, pady=0, sticky=tkinter.EW)
        self.total_label.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky=tkinter.E)
        self.task_btn.grid(row=3, column=0, padx=5, pady=1, sticky=tkinter.NSEW)
        self.short_break_btn.grid(row=3, column=1, padx=5, pady=1, sticky=tkinter.NSEW)
        self.long_break_btn.grid(row=3, column=2, padx=5, pady=1, sticky=tkinter.NSEW)
        self.start_button.grid(row=4, column=0, columnspan=3, padx=5, pady=8, sticky=tkinter.NSEW)

    def update_total(self, *_) -> None:
        timers = self.timers_input.get_timers()

        try:
            self.timers_input.mark_as_valid()
            text = format_timer_for_human(sum(timers))
            self.app.timers = timers
        except OverflowError:
            self.timers_input.mark_as_error()
            text = const.SUM_TIMERS_ERROR
            self.app.timers = []

        self.total_label.config(text=text)

    def add_option(self, option: int) -> None:
        timers_input = self.timers_input.input_var.get()
        if timers_input != "":
            self.timers_input.input_var.set(f"{timers_input}+{option}")
        else:
            self.timers_input.input_var.set(str(option))
        self.timers_input.icursor(tkinter.END)

    def clean(self) -> None:
        self.timers_input.delete(0, tkinter.END)
        self.timers_input.insert(0, "")

    def start_timers(self, _: tkinter.Event | None = None) -> None:
        if not self.app.timers:
            return

        self.app.timers_widget = TimersWidget(app=self.app)
        self.app.timers_widget.start_timers()
        self.app.hide()

    def stop_timers(self) -> None:
        self.clean()
        self.app.timers_widget.destroy()
        self.app.show()


class TimersWidget(tkinter.Toplevel):
    def __init__(self, app: App) -> None:
        super().__init__(master=app)
        self.app = app
        self.current_timer = None
        self.paused = False
        self.width = const.WINDOW_TIMER_WIDTH
        self.height = const.WINDOW_TIMER_HEIGHT

        self.geometry(f"{self.width}x{self.height}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(background=const.YELLOW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.position_window()

        self.play_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-play.png"))
        self.pause_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-pause.png"))
        self.stop_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-stop.png"))

        # --- Column 0
        self.pause_btn = PurpleButton(self, image=self.pause_img, command=self.toggle_pause)
        # --- Column 1
        self.timer_label = TimerLabel(self, text="No timer, no work!", size=10)
        # --- Column 2
        frames = [
            const.ASSETS_DIR.joinpath("bongo-cat-0.png"),
            const.ASSETS_DIR.joinpath("bongo-cat-1.png"),
            const.ASSETS_DIR.joinpath("bongo-cat-2.png"),
        ]
        self.bongo_cat = Sprite(self, width=38, height=30, frames=frames, frame_rate=150)
        # --- Column 3
        self.stop_btn = RedButton(
            self,
            image=self.stop_img,
            command=self.app.config_timers.stop_timers,
        )
        # --- Column 4
        self.draggable = Draggable(self, width=10)

        self.configure_component_grid()

    def position_window(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = 0
        self.geometry("+%d+%d" % (x, y))

    def configure_component_grid(self) -> None:
        self.pause_btn.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.W)
        self.timer_label.grid(row=0, column=1, padx=5, pady=0, sticky=tkinter.EW)
        self.bongo_cat.grid(row=0, column=2, padx=5, pady=0, sticky=tkinter.E)
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5, sticky=tkinter.E)
        self.draggable.grid(row=0, column=4, sticky=tkinter.NS)

    def _pause(self) -> None:
        self.pause_btn.configure(image=self.play_img)
        self.bongo_cat.stop()

    def _unpause(self) -> None:
        self.after(1000, self.update_timer)
        self.pause_btn.configure(image=self.pause_img)
        self.bongo_cat.start()

    def toggle_pause(self) -> None:
        self.paused = not self.paused
        if self.paused is False and self.current_timer is not None:
            self._unpause()
        else:
            self._pause()

    def start_timers(self) -> None:
        self.current_timer = self.app.get_next_timer()
        if self.current_timer is not None:
            self.update_timer()
        else:
            self._pause()

    def update_timer(self) -> None:
        if self.paused is True:
            return

        text = format_timer_for_human(self.current_timer.duration)
        self.timer_label.update_text(text=text)
        self.current_timer.tick()
        self.after(1000, [self.start_timers, self.update_timer][self.current_timer.is_running()])
