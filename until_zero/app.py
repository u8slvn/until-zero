from __future__ import annotations

import tkinter

from functools import partial
from typing import TYPE_CHECKING

from until_zero import constants as const
from until_zero.gui.button import LongBreakButton
from until_zero.gui.button import PauseButton
from until_zero.gui.button import ResetButton
from until_zero.gui.button import ShortBreakButton
from until_zero.gui.button import StartButton
from until_zero.gui.button import StopButton
from until_zero.gui.button import TaskButton
from until_zero.gui.draggable import Draggable
from until_zero.gui.frame import Frame
from until_zero.gui.input import TimersInput
from until_zero.gui.label import Label
from until_zero.gui.label import TimerLabel
from until_zero.gui.sprite import Sprite
from until_zero.session import VirtualEvents
from until_zero.session import session
from until_zero.tools import format_timer_for_human
from until_zero.tools import open_alpha_image


if TYPE_CHECKING:
    from until_zero.timer import Timer


class App(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.width = const.WINDOW_WIDTH
        self.height = const.WINDOW_HEIGHT

        session.register_root(root=self)

        # --- Configure windows
        self.geometry(f"{self.width}x{self.height}")
        self.title(const.WINDOW_TITLE)
        self.iconphoto(True, open_alpha_image(const.ASSETS_DIR.joinpath("icon-32.png")))
        self.resizable(width=False, height=False)
        self.configure(background=const.YELLOW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.position_window()

        # --- Frames
        self.config_timers = ConfigTimersFrame(app=self)
        self.config_timers.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.timers_widget: TimersWidget | None = None

        # --- Events
        self.bind(VirtualEvents.START_TIMERS, self.on_start_timers)
        self.bind(VirtualEvents.STOP_TIMERS, self.on_stop_timers)

    def position_window(self):
        self.update()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry("+%d+%d" % (x, y))

    def on_start_timers(self, _: tkinter.Event) -> None:
        self.timers_widget = TimersWidget(self)
        self.timers_widget.start_timers()
        self.withdraw()

    def on_stop_timers(self, _: tkinter.Event) -> None:
        self.timers_widget.destroy()
        self.deiconify()


class ConfigTimersFrame(Frame):
    def __init__(self, app: App):
        super().__init__(app=app, rows=5, columns=3)

        # --- Labels
        self.steps_label = Label(self, text="STEPS:")
        self.total_label = Label(self, text=const.SUM_TIMERS_PLACEHOLDER, size=10)

        # --- Inputs
        self.timers_input = TimersInput(self, update_callback=self.update_total)
        self.timers_input.bind("<Return>", session.start_timers)

        # --- Buttons
        self.clean_btn = ResetButton(self, command=self.timers_input.reset)
        self.task_btn = TaskButton(self, command=partial(self.add_option, const.OPTION_TASK))
        self.short_break_btn = ShortBreakButton(
            self,
            command=partial(self.add_option, const.OPTION_SHORT_BREAK),
        )
        self.long_break_btn = LongBreakButton(
            self,
            command=partial(self.add_option, const.OPTION_LONG_BREAK),
        )
        self.start_button = StartButton(self, command=session.start_timers)

        self._configure_component_grid()

    def _configure_component_grid(self):
        # --- Row 0
        self.steps_label.grid(row=0, column=0, padx=5, pady=0, sticky=tkinter.W)
        self.clean_btn.grid(row=0, column=2, padx=5, pady=0, sticky=tkinter.E)
        # -- Row 1
        self.timers_input.grid(row=1, column=0, columnspan=3, padx=2, pady=0, sticky=tkinter.EW)
        # -- Row 2
        self.total_label.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky=tkinter.E)
        # -- Row 3
        self.task_btn.grid(row=3, column=0, padx=5, pady=1, sticky=tkinter.NSEW)
        self.short_break_btn.grid(row=3, column=1, padx=5, pady=1, sticky=tkinter.NSEW)
        self.long_break_btn.grid(row=3, column=2, padx=5, pady=1, sticky=tkinter.NSEW)
        # -- Row 4
        self.start_button.grid(row=4, column=0, columnspan=3, padx=5, pady=8, sticky=tkinter.NSEW)

    def update_total(self, *_) -> None:
        timer_durations = self.timers_input.get_durations()
        sum_durations = session.set_timers(durations=timer_durations)

        if sum_durations is None:
            self.timers_input.mark_as_error()
            text = const.SUM_TIMERS_ERROR
        else:
            self.timers_input.mark_as_valid()
            text = format_timer_for_human(sum_durations)

        self.total_label.config(text=text)

    def add_option(self, option: int) -> None:
        timers_input = self.timers_input.input_var.get()
        if timers_input != "":
            self.timers_input.input_var.set(f"{timers_input}+{option}")
        else:
            self.timers_input.input_var.set(str(option))
        self.timers_input.icursor(tkinter.END)


class TimersWidget(tkinter.Toplevel):
    def __init__(self, app: App) -> None:
        super().__init__(master=app)
        self.paused = False
        self.current_timer: Timer | None = None
        self.width = const.WINDOW_TIMER_WIDTH
        self.height = const.WINDOW_TIMER_HEIGHT

        # --- Configure windows
        self.geometry(f"{self.width}x{self.height}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(background=const.YELLOW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.position_window()

        # --- Load images
        self.play_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-play.png"))
        self.pause_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-pause.png"))
        self.stop_img = open_alpha_image(const.ASSETS_DIR.joinpath("btn-stop.png"))

        # --- Labels
        self.timer_label = TimerLabel(self, text="No timer, no work!", size=10)

        # --- Buttons
        self.pause_btn = PauseButton(self, command=self.toggle_pause)
        self.stop_btn = StopButton(self, command=session.stop_timers)

        # --- Sprites
        frames = [
            open_alpha_image(const.ASSETS_DIR.joinpath("bongo-cat-0.png")),
            open_alpha_image(const.ASSETS_DIR.joinpath("bongo-cat-1.png")),
            open_alpha_image(const.ASSETS_DIR.joinpath("bongo-cat-2.png")),
        ]
        self.bongo_cat = Sprite(self, width=38, height=30, frames=frames, frame_rate=150)

        # --- Draggable
        self.draggable = Draggable(self, width=10)

        self._configure_component_grid()

    def position_window(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = 0
        self.geometry(f"+{x}+{y}")

    def _configure_component_grid(self) -> None:
        # --- Column 0
        self.pause_btn.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.W)
        # --- Column 1
        self.timer_label.grid(row=0, column=1, padx=5, pady=0, sticky=tkinter.EW)
        # --- Column 2
        self.bongo_cat.grid(row=0, column=2, padx=5, pady=0, sticky=tkinter.E)
        # --- Column 3
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5, sticky=tkinter.E)
        # --- Column 4
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
        self.current_timer = session.get_next_timer()
        if self.current_timer is not None:
            self.update_timer()
        else:
            self._pause()

    def update_timer(self) -> None:
        if self.paused is True:
            return

        text = self.current_timer.get_human_readable_duration()
        self.timer_label.update_text(text=text)
        self.current_timer.tick()
        self.after(1000, [self.start_timers, self.update_timer][self.current_timer.is_running()])
