from __future__ import annotations

import tkinter

import pytest

from until_zero.events import Events
from until_zero.session import Session
from until_zero.timer import Timer
from until_zero.timer import TimersSequence


@pytest.fixture
def session(mocker):
    root = mocker.Mock(spec=tkinter.Tk)
    session = Session(root=root)
    session.root = root

    return session


def test_session_setup_event(mocker):
    root = mocker.Mock(spec=tkinter.Tk)

    session = Session(root=root)

    calls = [mocker.call(event, "None") for event in Events]
    root.event_add.assert_has_calls(calls)
    root.bind(Events.TIMERS_STOPPED, session.reset_timers, add="+")


def test_bind_event(session, mocker):
    session.bind_event(Events.STOP_TIMERS, mocker.sentinel.callback)

    assert session.root.bind.call_args_list[1] == mocker.call(
        Events.STOP_TIMERS, mocker.sentinel.callback, add="+"
    )


def test_send_event(session):
    session.send_event(Events.STOP_TIMERS)

    session.root.event_generate.assert_called_once_with(Events.STOP_TIMERS)


def test_set_timers(session):
    assert session.has_timers() is False

    sum_timers = session.set_timers(durations=[1, 2, 3])

    assert sum_timers == 6
    assert session.has_timers() is True


def test_get_timers_sequence(session):
    _ = session.set_timers(durations=[1, 2, 3])

    timers_sequence = session.get_timers_sequence()

    assert isinstance(timers_sequence, TimersSequence)


def test_clear_timers(session):
    _ = session.set_timers(durations=[1, 2, 3])

    assert session.has_timers() is True

    session.clear_timers()

    assert session.has_timers() is False


def test_reset_timers(mocker, session):
    timer_reset = mocker.patch("until_zero.session.Timer.reset", spec=Timer)
    durations = [1, 2, 3]
    _ = session.set_timers(durations=durations)

    session.reset_timers()

    assert timer_reset.call_count == len(durations)


def test_start_timers(session):
    _ = session.set_timers(durations=[1, 2, 3])

    session.start_timers()

    session.root.event_generate.assert_called_once_with(Events.START_TIMERS)


def test_start_timers_with_no_timers(session):
    session.start_timers()

    session.root.event_generate.assert_not_called()


def test_stop_timers(mocker, session):
    reset_timers = mocker.Mock()
    session.reset_timers = reset_timers
    _ = session.set_timers(durations=[1, 2, 3])

    session.stop_timers()

    reset_timers.asset_called_once()
    session.root.event_generate.assert_called_once_with(Events.STOP_TIMERS)
