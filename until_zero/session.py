from __future__ import annotations

import tkinter

from typing import Callable

from until_zero.events import Events
from until_zero.timer import Timer
from until_zero.timer import TimersSequence


class Session:
    def __init__(self, root: tkinter.Tk) -> None:
        self.root: tkinter.Tk = root
        self._timers: list[Timer] = []
        self.setup_event()

    def setup_event(self) -> None:
        for event in Events:
            self.root.event_add(event, "None")

        self.bind_event(Events.TIMERS_STOPPED, self.reset_timers)

    def bind_event(self, event: Events, callback: Callable[[tkinter.Event], None]) -> None:
        self.root.bind(event, callback, add="+")

    def send_event(self, event: Events) -> None:
        self.root.event_generate(event)

    @property
    def timer_count(self) -> int:
        return len(self._timers)

    def has_timers(self) -> bool:
        return self.timer_count > 0

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
