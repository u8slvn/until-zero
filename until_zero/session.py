from __future__ import annotations

import tkinter

from typing import Callable

from until_zero.events import Events
from until_zero.timer import Timer
from until_zero.timer import TimersSequence


class TimersDurationOverFlow(Exception):
    pass


class _Session:
    def __init__(self) -> None:
        self._root: tkinter.Tk | None = None
        self._timers: list[Timer] = []

    def register_root(self, root: tkinter.Tk) -> None:
        self._root = root
        for v_event in Events:
            self._root.event_add(v_event, "None")

        self.bind_event(Events.TIMERS_STOPPED, self.reset_timers)

    def bind_event(self, event: Events, callback: Callable[[tkinter.Event], None]) -> None:
        self._root.bind(event, callback, add="+")

    def send_event(self, event: Events) -> None:
        self._root.event_generate(event)

    def has_timers(self) -> bool:
        return len(self._timers) > 0

    def set_timers(self, durations: list[int]) -> int:
        self.clear_timers()
        sum_durations = sum(durations)
        for duration in durations:
            self._timers.append(Timer(duration=duration))
        return sum_durations

    def get_timers_sequence(self) -> TimersSequence:
        return TimersSequence(timers=self._timers)

    def clear_timers(self) -> None:
        self._timers = []

    def reset_timers(self, _: tkinter.Event | None = None) -> None:
        for timer in self._timers:
            timer.reset()

    def start_timers(self, _: tkinter.Event | None = None) -> None:
        if not self.has_timers():
            return

        self.send_event(event=Events.START_TIMERS)

    def stop_timers(self, _: tkinter.Event | None = None) -> None:
        self.reset_timers()

        self.send_event(event=Events.STOP_TIMERS)


session = _Session()
