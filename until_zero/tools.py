from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from PIL import Image
from PIL import ImageTk

from until_zero.constants import SUM_TIMERS_PLACEHOLDER


if TYPE_CHECKING:
    from pathlib import Path


def format_timer_for_human(timer: int) -> str:
    sum_timers = timedelta(seconds=timer)
    days = sum_timers.days
    hours, remainder = divmod(sum_timers.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    human_td = []
    if days > 0:
        human_td.append(f"{days}days" if days > 1 else f"{days}day")
    if hours > 0:
        human_td.append(f"{hours}h")
    if minutes > 0:
        human_td.append(f"{minutes}m")
    if seconds > 0:
        human_td.append(f"{seconds}s")

    if not human_td:
        return SUM_TIMERS_PLACEHOLDER

    return ", ".join(human_td)


class StepTimer:
    def __init__(self, duration: int) -> None:
        self.duration = duration

    def tick(self) -> None:
        if self.duration <= 0:
            self.ring()
        self.duration -= 1

    def is_running(self):
        return self.duration >= 0

    def ring(self) -> None:
        ...
        # print("Ring!")


def open_alpha_image(file: Path) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(Image.open(file).convert("RGBA"))
