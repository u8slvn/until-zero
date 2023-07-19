from __future__ import annotations

from datetime import timedelta

from until_zero.constants import SUM_TIMERS_PLACEHOLDER


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
