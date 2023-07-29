from __future__ import annotations

import tkinter

import pytest

from until_zero.events import Events
from until_zero.gui.button import PauseReplayButton
from until_zero.session import Session


@pytest.mark.parametrize(
    "event, image_name",
    [
        (Events.TIMERS_STOPPED, "image_replay"),
        (Events.PAUSE_TIMER, "image_play"),
        (Events.UNPAUSE_TIMER, "image"),
    ],
)
def test_pause_replay_button_on_events(mocker, test_app, event, image_name):
    app = test_app(app_cls=tkinter.Tk)
    session = Session(root=app)
    pause_replay_btn = PauseReplayButton(app, command=mocker.Mock())
    pause_replay_btn.bind_session(session=session)
    setattr(pause_replay_btn, "configure", mocker.Mock())
    app.pump_events()

    session.send_event(event=event)

    image = getattr(pause_replay_btn, image_name)
    getattr(pause_replay_btn, "configure").assert_called_once_with(image=image)
