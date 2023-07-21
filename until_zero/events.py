from __future__ import annotations

from enum import StrEnum


class Events(StrEnum):
    START_TIMERS = "<<StartTimers>>"
    STOP_TIMERS = "<<StopTimers>>"
    PAUSE_TIMER = "<<PauseTimer>>"
    UNPAUSE_TIMER = "<<UnpauseTimer>>"
    TIMERS_STOPPED = "<<TimerStopped>>"
    REPLAY_TIMERS = "<<ReplayTimers>>"
