from __future__ import annotations

import tkinter

import pytest

from until_zero import constants as const
from until_zero.gui.input import TimersInput


@pytest.mark.parametrize(
    "value, result",
    [
        ("12:21+0:30+4:50", True),
        ("12:37+1223+2+12+3:60", True),
        ("12+2+1212+3+43+4+123", True),
        ("12:12+12+12+12", True),
        ("12:31", True),
        ("12:70", True),
        ("1+2:", True),
        ("1+2:0:4:4:4", False),
        ("11111", False),
        ("aaa", False),
        ("@#)", False),
        ("12:123test", False),
        ("12+123test", False),
    ],
)
def test_validate_timers_input(value, result):
    assert TimersInput.validate_timers_input(value=value) is result


def test_get_durations(mocker, test_app):
    app = test_app(app_cls=tkinter.Tk)
    timers_input = TimersInput(app, mocker.MagicMock())
    timers_input.input_var.get = mocker.Mock(return_value="100+10:10+1+10:5")
    app.pump_events()

    result = timers_input.get_durations()

    assert result == [6000, 610, 60, 605]


def test_clean(mocker, test_app):
    app = test_app(app_cls=tkinter.Tk)
    timers_input = TimersInput(app, mocker.MagicMock())
    timers_input.insert(0, "hello")
    app.pump_events()

    timers_input.clean()

    assert timers_input.get() == ""


def test_mark_as_status(mocker, test_app):
    app = test_app(app_cls=tkinter.Tk)
    timers_input = TimersInput(app, mocker.MagicMock())
    app.pump_events()

    timers_input.mark_as_error()

    assert timers_input["foreground"] == const.RED

    timers_input.mark_as_valid()

    assert timers_input["foreground"] == const.WHITE
