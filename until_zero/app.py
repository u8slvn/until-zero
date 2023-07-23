from __future__ import annotations

import tkinter

from until_zero import constants as const
from until_zero.events import Events
from until_zero.gui.button import CleanButton
from until_zero.gui.button import LongBreakButton
from until_zero.gui.button import PauseReplayButton
from until_zero.gui.button import ShortBreakButton
from until_zero.gui.button import StartButton
from until_zero.gui.button import StopButton
from until_zero.gui.button import TaskButton
from until_zero.gui.draggable import Draggable
from until_zero.gui.frame import Frame
from until_zero.gui.input import TimersInput
from until_zero.gui.label import Label
from until_zero.gui.label import TimerLabel
from until_zero.gui.sprite import BongoCat
from until_zero.session import session
from until_zero.tools import format_time_for_human
from until_zero.tools import open_alpha_image


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
        self.config_timers = ConfigTimersFrame(self)
        self.config_timers.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.timers_widget: TimersWidget | None = None

        # --- Events
        self.bind(Events.START_TIMERS, self.on_start_timers)
        self.bind(Events.STOP_TIMERS, self.on_stop_timers)

    def position_window(self):
        self.update()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry("+%d+%d" % (x, y))

    def on_start_timers(self, _: tkinter.Event) -> None:
        self.timers_widget = TimersWidget(self)
        self.withdraw()

    def on_stop_timers(self, _: tkinter.Event) -> None:
        if self.timers_widget is not None:
            self.timers_widget.destroy()
        self.deiconify()
        self.config_timers.timers_input.focus_set()


class ConfigTimersFrame(Frame):
    def __init__(self, parent: tkinter.Tk):
        super().__init__(parent=parent, rows=5, columns=3)

        # --- Labels
        self.steps_label = Label(self, text="STEPS:")
        self.sum_timers_label = Label(self, text=const.SUM_TIMERS_PLACEHOLDER, size=10)

        # --- Inputs
        self.timers_input = TimersInput(self, update_callback=self.update_sum_timers)
        self.timers_input.bind("<Return>", session.start_timers)

        # --- Buttons
        self.clean_btn = CleanButton(self, command=self.timers_input.clean)
        self.task_btn = TaskButton(self, command=self.add_pomodoro_timer)
        self.short_break_btn = ShortBreakButton(self, command=self.add_pomodoro_timer)
        self.long_break_btn = LongBreakButton(self, command=self.add_pomodoro_timer)
        self.start_button = StartButton(self, command=session.start_timers)

        self._configure_component_grid()

    def _configure_component_grid(self):
        # --- Row 0
        self.steps_label.grid(row=0, column=0, padx=5, pady=0, sticky=tkinter.W)
        self.clean_btn.grid(row=0, column=2, padx=5, pady=0, sticky=tkinter.E)
        # -- Row 1
        self.timers_input.grid(row=1, column=0, columnspan=3, padx=2, pady=0, sticky=tkinter.EW)
        # -- Row 2
        self.sum_timers_label.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky=tkinter.E)
        # -- Row 3
        self.task_btn.grid(row=3, column=0, padx=5, pady=1, sticky=tkinter.NSEW)
        self.short_break_btn.grid(row=3, column=1, padx=5, pady=1, sticky=tkinter.NSEW)
        self.long_break_btn.grid(row=3, column=2, padx=5, pady=1, sticky=tkinter.NSEW)
        # -- Row 4
        self.start_button.grid(row=4, column=0, columnspan=3, padx=5, pady=8, sticky=tkinter.NSEW)

    def update_sum_timers(self, *_) -> None:
        timer_durations = self.timers_input.get_durations()
        sum_durations = session.set_timers(durations=timer_durations)

        if sum_durations > 14400 * 60:
            self.timers_input.mark_as_error()
            text = const.SUM_TIMERS_ERROR
        else:
            self.timers_input.mark_as_valid()
            text = format_time_for_human(sum_durations)

        self.sum_timers_label.config(text=text)

    def add_pomodoro_timer(self, option: int) -> None:
        timers_input = self.timers_input.input_var.get()
        if timers_input != "":
            self.timers_input.input_var.set(f"{timers_input}+{option}")
        else:
            self.timers_input.input_var.set(str(option))
        self.timers_input.icursor(tkinter.END)


class TimersWidget(tkinter.Toplevel):
    def __init__(self, parent: tkinter.Tk) -> None:
        super().__init__(master=parent)
        self.paused = False
        self.width = const.WINDOW_TIMER_WIDTH
        self.height = const.WINDOW_TIMER_HEIGHT
        self.timers_sequence = session.get_timers_sequence()

        # --- Configure windows
        self.geometry(f"{self.width}x{self.height}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(background=const.YELLOW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.position_window()

        # --- Labels
        self.timer_label = TimerLabel(self, text="", size=10)

        # --- Buttons
        self.pause_btn = PauseReplayButton(self, command=self.pause_replay_click)
        self.stop_btn = StopButton(self, command=session.stop_timers)

        # --- Sprites
        self.bongo_cat = BongoCat(self)

        # --- Draggable
        self.draggable = Draggable(self, width=10)

        self._configure_component_grid()
        self.tick()

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

    def pause_replay_click(self) -> None:
        # Replay
        if self.timers_sequence.is_done():
            session.send_event(Events.UNPAUSE_TIMER)
            self.paused = False
            self.timers_sequence = session.get_timers_sequence()
            self.tick()
            return

        # Toggle pause
        self.paused = not self.paused
        if self.paused is False and self.timers_sequence.is_done() is not None:
            session.send_event(Events.UNPAUSE_TIMER)
            self.after(1000, self.tick)
        else:
            session.send_event(Events.PAUSE_TIMER)

    def tick(self) -> None:
        if self.paused:
            return

        self.update_timer_label()
        self.timers_sequence.tick()
        if not self.timers_sequence.is_done():
            self.after(1000, self.tick)
        else:
            session.send_event(Events.TIMERS_STOPPED)

    def update_timer_label(self) -> None:
        text = self.timers_sequence.get_current_time_as_text()
        self.timer_label.update_text(text=text)
