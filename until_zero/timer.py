from __future__ import annotations

from playsound import playsound

from until_zero import constants as const
from until_zero.tools import format_timer_for_human


class Timer:
    sound = str(const.ASSETS_DIR.joinpath("bip.wav"))

    def __init__(self, duration: int) -> None:
        self._init_duration = duration
        self._duration = duration

    def reset(self) -> None:
        self._duration = self._init_duration

    def get_human_readable_duration(self) -> str:
        return format_timer_for_human(timer=self._duration)

    def tick(self) -> None:
        if self._duration <= 0:
            self.ring()
        self._duration -= 1

    def is_running(self) -> bool:
        return self._duration >= 0

    def ring(self) -> None:
        playsound(self.sound, block=False)

    def __repr__(self) -> str:
        return f"Timer<duration: {self._duration}>"
