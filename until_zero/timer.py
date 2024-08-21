from __future__ import annotations

import time

from typing import Generator

from playsound import playsound

from until_zero import constants as const
from until_zero.tools import format_time_for_human


class Timer:
    sound = str(const.ASSETS_DIR.joinpath("bip.mp3"))

    def __init__(self, duration: int) -> None:
        self.paused = True
        self.duration = float(duration)
        self._time = self.duration
        self._last_tick = 0.0
        self._done = False

    @property
    def time(self) -> int:
        return round(self._time)

    def reset(self) -> None:
        self._last_tick = 0.0
        self._time = self.duration
        self._done = False

    def tick(self) -> None:
        if self.time <= 0 and not self._done:
            self._done = True
            self.ring()

        if self._last_tick == 0.0:
            self._last_tick = time.time()

        self._time -= time.time() - self._last_tick
        self._last_tick = time.time()

    def is_ended(self) -> bool:
        return self._done

    def ring(self) -> None:
        playsound(self.sound, block=False)

    def __repr__(self) -> str:
        return f"Timer<duration: {self.time}>"


class TimersSequence:
    def __init__(self, timers: list[Timer]):
        def timers_iterator() -> Generator[Timer, None, None]:
            for timer in timers:
                yield timer

        self._timers = timers_iterator()
        self._current_timer_index = 1
        self._current_timer: Timer | None = self._get_next_timer()
        self._running = True

    def _get_next_timer(self) -> Timer | None:
        try:
            return next(self._timers)
        except StopIteration:
            return None

    def is_done(self) -> bool:
        return not self._running

    def tick(self):
        if self._current_timer is None:
            self._running = False
            return

        self._current_timer.tick()

        if self._current_timer.is_ended():
            self._current_timer = self._get_next_timer()
            self._current_timer_index += 1

    def get_current_timer_time_as_text(self) -> str:
        if self._current_timer is None:
            return "ZER0"

        return format_time_for_human(time=self._current_timer.time)

    def get_current_timer_index(self) -> int:
        return self._current_timer_index
