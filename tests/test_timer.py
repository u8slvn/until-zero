from __future__ import annotations

import pytest

from until_zero.timer import Timer
from until_zero.timer import TimersSequence


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

        timer.tick()
        timer.tick()
        timer.tick()

        assert timer.time == 2

    def test_is_ended(self, playsound):
        timer = Timer(duration=2)
        timer.tick()
        timer.tick()
        timer.tick()

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

        timers_sequence.tick()
        timers_sequence.tick()
        timers_sequence.tick()
        timers_sequence.tick()
        timers_sequence.tick()
        timers_sequence.tick()

        assert timers_sequence.is_done() is True
        assert playsound.call_count == 2

    def test_get_current_time_as_text(self, playsound):
        timers_sequence = TimersSequence(timers=[Timer(1)])

        time_text = timers_sequence.get_current_time_as_text()

        assert time_text == "1s"

        timers_sequence.tick()
        timers_sequence.tick()
        timers_sequence.tick()

        time_text = timers_sequence.get_current_time_as_text()

        assert time_text == "ZER0"
