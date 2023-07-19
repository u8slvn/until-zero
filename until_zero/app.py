from __future__ import annotations

import tkinter

from functools import partial

from until_zero import constants as const
from until_zero import pomodoro
from until_zero.pomodoro import extract_timers_from_input
from until_zero.utils import format_timer_for_human


class App(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.timers: list[int] = []

        self.geometry(const.WINDOW_SIZE)
        self.title(const.WINDOW_TITLE)
        self.resizable(width=False, height=False)
        self.configure(
            background=const.BACKGROUND_COLOR,
        )

        self.validate_pomodoro_input = self.register(pomodoro.validate_input)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.config_frame = tkinter.Frame(self, width=const.WINDOW_WIDTH)
        self.config_frame.configure(background=const.BACKGROUND_COLOR)
        self.config_frame.grid(
            row=0, column=0, columnspan=3, padx=5, pady=5, sticky=tkinter.EW
        )
        self.config_frame.grid_columnconfigure(0, weight=1)
        self.config_frame.grid_columnconfigure(1, weight=1)
        self.config_frame.grid_columnconfigure(2, weight=1)

        self.label = Label(self.config_frame, text="STEPS:")
        self.label.grid(row=0, column=0, sticky=tkinter.W)

        self.clean_btn = CleanButton(
            self.config_frame, text="RESET", command=self.clean
        )
        self.clean_btn.grid(row=0, column=2, sticky=tkinter.E)

        self.input_var = tkinter.StringVar()
        self.input_var.trace("w", self.update_total)

        self.input = Input(
            self.config_frame,
            validate=self.validate_pomodoro_input,
            textvariable=self.input_var,
        )
        self.input.grid(row=1, column=0, columnspan=3, sticky=tkinter.EW)

        self.total = Label(self.config_frame, text=const.SUM_TIMERS_PLACEHOLDER)
        self.total.grid(row=2, column=2, sticky=tkinter.E)

        self.pomodoro_btn = OptionButton(
            self,
            text="POMODORO",
            command=partial(self.add_option, const.OPTION_POMODORO),
        )
        self.pomodoro_btn.grid(row=1, column=0, padx=5, pady=5)

        self.short_break_btn = OptionButton(
            self,
            text="SHORT BREAK",
            command=partial(self.add_option, const.OPTION_SHORT_BREAK),
        )
        self.short_break_btn.grid(row=1, column=1, padx=5, pady=5)

        self.long_break_btn = OptionButton(
            self,
            text="LONG BREAK",
            command=partial(self.add_option, const.OPTION_LONG_BREAK),
        )
        self.long_break_btn.grid(row=1, column=2, padx=5, pady=5)

        self.start_button = StartButton(self, text="START", command=self.start_timers)
        self.start_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    def add_option(self, option: int) -> None:
        timers_input = self.input_var.get()
        if timers_input != "":
            self.input_var.set(f"{timers_input}+{option}")
        else:
            self.input_var.set(str(option))

    def update_total(self, *_) -> None:
        timers_input = self.input_var.get()
        self.timers = extract_timers_from_input(timers_input)

        try:
            text = format_timer_for_human(sum(self.timers))
        except OverflowError:
            text = const.SUM_TIMERS_ERROR

        self.total.config(text=text)

    def clean(self) -> None:
        self.input.delete(0, tkinter.END)
        self.input.insert(0, "")

    def start_timers(self) -> None:
        self.state(newstate="iconic")
        self.clean_btn.config(state=tkinter.DISABLED)
        self.pomodoro_btn.config(state=tkinter.DISABLED)
        self.short_break_btn.config(state=tkinter.DISABLED)
        self.long_break_btn.config(state=tkinter.DISABLED)
        self.input.config(state=tkinter.DISABLED)
        self.start_button.config(text="STOP", command=self.stop_timers)

    def stop_timers(self) -> None:
        self.clean_btn.config(state=tkinter.NORMAL)
        self.pomodoro_btn.config(state=tkinter.NORMAL)
        self.short_break_btn.config(state=tkinter.NORMAL)
        self.long_break_btn.config(state=tkinter.NORMAL)
        self.input.config(state=tkinter.NORMAL)
        self.start_button.config(text="START", command=self.start_timers)


class CleanButton(tkinter.Button):
    def __init__(self, master: tkinter.Misc, text: str, **kwargs):
        super().__init__(
            master=master,
            text=text,
            font=(const.FONT, const.CLEAN_BTN_SIZE),
            **kwargs,
        )
        self.configure(
            foreground=const.CLEAN_BTN_COLOR,
            activeforeground=const.CLEAN_BTN_COLOR,
            background=const.CLEAN_BTN_BG_COLOR,
            activebackground=const.CLEAN_BTN_BG_ACTIVE_COLOR,
            relief=tkinter.GROOVE,
        )


class StartButton(tkinter.Button):
    def __init__(self, master: tkinter.Misc, text: str, **kwargs):
        super().__init__(
            master=master,
            text=text,
            width=100,
            font=(const.FONT, const.START_BTN_SIZE),
            **kwargs,
        )
        self.configure(
            foreground=const.START_BTN_COLOR,
            activeforeground=const.START_BTN_COLOR,
            background=const.START_BTN_BG_COLOR,
            activebackground=const.START_BTN_BG_ACTIVE_COLOR,
            relief=tkinter.GROOVE,
        )


class OptionButton(tkinter.Button):
    def __init__(self, master: tkinter.Misc, text: str, **kwargs):
        super().__init__(
            master=master,
            text=text,
            width=100,
            font=(const.FONT, const.OPTION_BTN_SIZE),
            **kwargs,
        )
        self.configure(
            foreground=const.OPTION_BTN_COLOR,
            activeforeground=const.OPTION_BTN_COLOR,
            background=const.OPTION_BTN_BG_COLOR,
            activebackground=const.OPTION_BTN_BG_ACTIVE_COLOR,
            relief=tkinter.GROOVE,
        )


class Label(tkinter.Label):
    def __init__(self, master: tkinter.Misc, text: str) -> None:
        super().__init__(
            master=master,
            text=text,
            font=(const.FONT, const.LABEL_SIZE),
            foreground=const.TEXT_COLOR,
            justify=tkinter.CENTER,
        )
        self.configure(
            background=const.BACKGROUND_COLOR,
        )


class Input(tkinter.Entry):
    def __init__(
        self, master: tkinter.Misc, validate: str, textvariable: tkinter.StringVar
    ):
        super().__init__(
            master=master,
            justify=tkinter.CENTER,
            font=(const.FONT, const.LABEL_SIZE),
            textvariable=textvariable,
        )
        self.config(validate="key", validatecommand=(validate, "%P"))
        self.configure(
            borderwidth=3,
            relief=tkinter.FLAT,
            background=const.INPUT_BG_COLOR,
            foreground=const.INPUT_COLOR,
            insertbackground=const.INPUT_COLOR,
        )
