from __future__ import annotations

import tkinter

from functools import partial

from until_zero import constants as const
from until_zero import pomodoro
from until_zero.gui.button import BlueButton
from until_zero.gui.button import PurpleButton
from until_zero.gui.button import RedButton
from until_zero.gui.frame import Frame
from until_zero.gui.input import Input
from until_zero.gui.label import Label
from until_zero.gui.sprite import Sprite
from until_zero.pomodoro import extract_timers_from_input
from until_zero.tools import StepTimer
from until_zero.tools import format_timer_for_human


class App(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.timers: list[int] = []
        self.width = const.WINDOW_WIDTH
        self.height = const.WINDOW_HEIGHT

        self.geometry(f"{self.width}x{self.height}")
        self.title(const.WINDOW_TITLE)
        self.resizable(width=False, height=False)
        self.configure(background=const.BACKGROUND_COLOR)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._position_window()

        self.validate_pomodoro_input = self.register(pomodoro.validate_input)

        self.config_timers = ConfigTimers(app=self)
        self.config_timers.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.run_timers: RunTimers | None = None

    def _position_window(self):
        self.update()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry("+%d+%d" % (x, y))

    def get_next_timer(self) -> StepTimer | None:
        if len(self.timers) > 0:
            return StepTimer(duration=self.timers.pop(-1))
        return None

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()


class ConfigTimers(Frame):
    def __init__(self, app: App):
        super().__init__(app=app, rows=5, columns=3)
        # --- Row 0
        self.steps_label = Label(self, text="STEPS:")
        self.clean_btn = BlueButton(
            self,
            text="RESET",
            text_size=const.CLEAN_BTN_SIZE,
            command=self.clean,
        )
        # -- Row 1
        self.timers_input = Input(
            self,
            validate=self.app.validate_pomodoro_input,
            update_callback=self.update_total,
        )
        # -- Row 2
        self.total_label = Label(self, text=const.SUM_TIMERS_PLACEHOLDER, size=10)
        # -- Row 3
        self.task_btn = PurpleButton(
            self,
            text="TASK",
            text_size=const.OPTION_BTN_SIZE,
            command=partial(self.add_option, const.OPTION_TASK),
        )
        self.short_break_btn = PurpleButton(
            self,
            text="SHORT BREAK",
            text_size=const.OPTION_BTN_SIZE,
            command=partial(self.add_option, const.OPTION_SHORT_BREAK),
        )
        self.long_break_btn = PurpleButton(
            self,
            text="LONG BREAK",
            text_size=const.OPTION_BTN_SIZE,
            command=partial(self.add_option, const.OPTION_LONG_BREAK),
        )
        # -- Row 4
        self.start_button = RedButton(
            self,
            text="START",
            text_size=const.START_BTN_SIZE,
            command=self.start_timers,
        )

        self.configure_component_grid()

    def configure_component_grid(self):
        self.steps_label.grid(row=0, column=0, padx=5, pady=0, sticky=tkinter.W)
        self.clean_btn.grid(row=0, column=2, padx=5, pady=0, sticky=tkinter.E)

        self.timers_input.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky=tkinter.EW)

        self.total_label.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky=tkinter.E)

        self.task_btn.grid(row=3, column=0, padx=5, pady=2, sticky=tkinter.EW)
        self.short_break_btn.grid(row=3, column=1, padx=5, pady=2, sticky=tkinter.EW)
        self.long_break_btn.grid(row=3, column=2, padx=5, pady=2, sticky=tkinter.EW)

        self.start_button.grid(row=4, column=0, columnspan=3, padx=3, pady=3, sticky=tkinter.EW)

    def update_total(self, *_) -> None:
        timers_input = self.timers_input.input_var.get()
        self.app.timers = extract_timers_from_input(timers_input)

        try:
            text = format_timer_for_human(sum(self.app.timers))
        except OverflowError:
            text = const.SUM_TIMERS_ERROR

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

    def start_timers(self) -> None:
        self.app.run_timers = RunTimers(app=self.app)
        self.app.run_timers.start_timers()
        self.app.hide()

    def stop_timers(self) -> None:
        self.clean()
        self.app.run_timers.destroy()
        self.app.show()


class RunTimers(tkinter.Toplevel):
    def __init__(self, app: App) -> None:
        super().__init__(master=app)
        self.app = app
        self.geometry("300x30")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(background=const.BACKGROUND_COLOR)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._position_window()
        self.current_timer = None
        self.paused = False

        # -- Column 0
        self.pause_btn = PurpleButton(
            self, text="⏸", text_size=const.TIMER_WINDOW_BTN_SIZE, command=self.toggle_pause
        )
        # -- Column 1
        self.timer_label = Label(self, text="yolo", size=10)
        # -- Column 2
        frames = [
            const.ASSETS_DIR.joinpath("bongo-cat-0.png"),
            const.ASSETS_DIR.joinpath("bongo-cat-1.png"),
            const.ASSETS_DIR.joinpath("bongo-cat-2.png"),
        ]
        self.bongo_cat = Sprite(self, width=38, height=30, frames=frames, frame_rate=150)
        # -- Column 3
        self.stop_btn = RedButton(
            self,
            text="⏹",
            text_size=const.TIMER_WINDOW_BTN_SIZE,
            command=self.app.config_timers.stop_timers,
        )

        self.configure_component_grid()

    def _position_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = 0
        self.geometry("+%d+%d" % (x, y))

    def configure_component_grid(self):
        self.pause_btn.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.W)
        self.timer_label.grid(row=0, column=1, padx=5, pady=0, sticky=tkinter.E)
        self.bongo_cat.grid(row=0, column=2, padx=5, pady=0, sticky=tkinter.E)
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5, sticky=tkinter.E)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused is False and self.current_timer is not None:
            self.after(1000, self.update_timer)
            self.pause_btn.configure(text="⏸")
            self.bongo_cat.start()
        else:
            self.pause_btn.configure(text="🞂")
            self.bongo_cat.stop()

    def start_timers(self):
        self.current_timer = self.app.get_next_timer()
        if self.current_timer is not None:
            self.update_timer()

    def update_timer(self):
        if self.paused is True:
            return

        text = format_timer_for_human(self.current_timer.duration)
        self.timer_label.configure(text=text)
        self.current_timer.tick()

        if self.current_timer.is_running():
            self.after(1000, self.update_timer)
        else:
            self.start_timers()
