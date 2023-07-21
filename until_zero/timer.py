from __future__ import annotations

from typing import Generator

from playsound import playsound

from until_zero import constants as const
from until_zero.tools import format_time_for_human


class Timer:
    tick_duration = 1000
    sound = str(const.ASSETS_DIR.joinpath("bip.wav"))

    def __init__(self, duration: int) -> None:
        self.paused = True
        self.duration = duration
        self.time = duration

    def reset(self) -> None:
        self.time = self.duration

    def tick(self) -> None:
        if self.time <= 0:
            self.ring()
        self.time -= 1

    def is_ended(self) -> bool:
        return self.time < 0

    def ring(self) -> None:
        playsound(self.sound, block=False)

    def __repr__(self) -> str:
        return f"Timer<duration: {self.time}>"


class TimersSequence:
    def __init__(self, timers: list[Timer]):
        def timers_iterator() -> Generator[Timer]:
            for timer in timers:
                yield timer

        self._timers = timers_iterator()
        self._current: Timer | None = self._get_next_timer()
        self._running = True

    def _get_next_timer(self) -> Timer | None:
        try:
            return next(self._timers)
        except StopIteration:
            return None

    def is_done(self) -> bool:
        return not self._running

    def tick(self):
        if self._current is None:
            self._running = False
            return

        print("tick")

        self._current.tick()

        if self._current.is_ended():
            self._current = self._get_next_timer()

    def get_human_readable_duration(self) -> str:
        if self._current is None:
            return "ZER0"

        return format_time_for_human(time=self._current.time)
