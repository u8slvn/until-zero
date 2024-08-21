from __future__ import annotations

import pytest

from freezegun import freeze_time

from until_zero.timer import Timer
from until_zero.timer import TimersSequence


def call_tick_n_times(ticker, n):
    for s in range(n):
        with freeze_time(f"2012-01-14 12:00:0{s}"):
            ticker.tick()


@pytest.fixture
def playsound(mocker):
    yield mocker.patch("until_zero.timer.playsound")


class TestTimer:
    def test_reset(self):
        duration = 5
        timer = Timer(duration=duration)

        timer.tick()
        timer.tick()

        timer.reset()

        assert timer.time == duration

    def test_tick(self):
        timer = Timer(duration=5)

        call_tick_n_times(timer, 4)

        assert timer.time == 2

    def test_is_ended(self, playsound):
        timer = Timer(duration=2)

        call_tick_n_times(timer, 4)

        assert timer.is_ended() is True
        playsound.assert_called_once_with(Timer.sound, block=False)

    def test_ring(self, playsound):
        timer = Timer(duration=2)

        timer.ring()

        playsound.assert_called_once_with(Timer.sound, block=False)

    def test_repr(self):
        timer = Timer(2)

        assert repr(timer) == "Timer<duration: 2>"


class TestTimerSequence:
    def test_tick(self, playsound):
        timers_sequence = TimersSequence(timers=[Timer(1), Timer(1)])

        assert timers_sequence.is_done() is False
        assert timers_sequence.get_current_timer_index() == 1

        call_tick_n_times(timers_sequence, 3)

        assert timers_sequence.get_current_timer_index() == 2

        call_tick_n_times(timers_sequence, 4)

        assert timers_sequence.is_done() is True
        assert playsound.call_count == 2

    def test_get_current_time_as_text(self, playsound):
        timers_sequence = TimersSequence(timers=[Timer(1)])

        time_text = timers_sequence.get_current_timer_time_as_text()

        assert time_text == "1s"

        call_tick_n_times(timers_sequence, 4)

        time_text = timers_sequence.get_current_timer_time_as_text()

        assert time_text == "ZER0"
