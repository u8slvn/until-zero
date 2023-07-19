from __future__ import annotations

import re


# https://regex101.com/r/Mf1U4z/1
EXTRACT_REG = re.compile(r"(?:(\d+)(?::(\d+))?\+?)")
# https://regex101.com/r/3RtSGv/1
CHECK_REG = re.compile(r"^(((\d+):(\d?(?!\d+:\d+)))|(\d+)\+?)+$")


def validate_input(string: str) -> bool:
    return CHECK_REG.match(string) is not None or string == ""


def extract_timers_from_input(string) -> list[int] | None:
    matches = EXTRACT_REG.findall(string)

    timers = []
    try:
        for match in matches:
            m, s = match
            timer = int(m) * 60
            timer += int(s) if s.isdigit() else 0
            timers.append(timer)
    except OverflowError:
        return None

    return timers
