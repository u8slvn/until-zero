from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING
from typing import Generator

from until_zero.timer import Timer


if TYPE_CHECKING:
    import tkinter


class TimersDurationOverFlow(Exception):
    pass


class VirtualEvents(StrEnum):
    START_TIMERS = "<<StartTimers>>"
    STOP_TIMERS = "<<StopTimers>>"
    PAUSE_TIMER = "<<PauseTimer>>"
    UNPAUSE_TIMER = "<<UnpauseTimer>>"


class _Session:
    def __init__(self) -> None:
        self._root: tkinter.Tk | None = None
        self._timers: list[Timer] = []
        self._current_timers: Generator[Timer] | None = None

    def register_root(self, root: tkinter.Tk) -> None:
        self._root = root
        for v_event in VirtualEvents:
            self._root.event_add(v_event, "None")

    def send_event(self, v_event: VirtualEvents) -> None:
        self._root.event_generate(v_event)

    def has_timers(self) -> bool:
        return len(self._timers) > 0

    def set_timers(self, durations: list[int]) -> int | None:
        self.reset_timers()
        try:
            sum_durations = sum(durations)
            for duration in durations:
                self._timers.append(Timer(duration=duration))
            return sum_durations
        except OverflowError:
            return None

    def reset_timers(self) -> None:
        self._timers = []

    def get_next_timer(self) -> Timer | None:
        try:
            return next(self._current_timers)
        except StopIteration:
            return None

    def start_timers(self, _: tkinter.Event | None = None) -> None:
        if not self.has_timers():
            return

        def timers() -> Generator[Timer]:
            for timer in self._timers:
                yield timer

        self._current_timers = timers()
        self.send_event(v_event=VirtualEvents.START_TIMERS)

    def stop_timers(self, _: tkinter.Event | None = None) -> None:
        self._current_timers = None
        for timer in self._timers:
            timer.reset()

        self.send_event(v_event=VirtualEvents.STOP_TIMERS)


session = _Session()
