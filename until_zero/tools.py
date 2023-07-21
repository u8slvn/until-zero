from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from PIL import Image
from PIL import ImageTk

from until_zero import constants as const


if TYPE_CHECKING:
    from pathlib import Path


def format_time_for_human(time: int) -> str:
    sum_timers = timedelta(seconds=time)
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
        return const.SUM_TIMERS_PLACEHOLDER

    return ", ".join(human_td)


def open_alpha_image(file: Path) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(Image.open(file).convert("RGBA"))
