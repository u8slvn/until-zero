from __future__ import annotations

import pytest

from until_zero.events import Events
from until_zero.gui.button import PauseReplayButton


@pytest.mark.parametrize(
    "event, image_name",
    [
        (Events.TIMERS_STOPPED, "image_replay"),
        (Events.PAUSE_TIMER, "image_play"),
        (Events.UNPAUSE_TIMER, "image"),
    ],
)
def test_pause_replay_button_on_events(mocker, monkeypatch, test_session, event, image_name):
    mocker.patch("until_zero.gui.button.session", test_session)
    test_session.root.add_test_action(test_session.send_event, event)
    pause_replay_btn = PauseReplayButton(test_session.root, command=mocker.Mock())
    monkeypatch.setattr(pause_replay_btn, "configure", mocker.Mock())

    test_session.root.run_test_actions()

    image = getattr(pause_replay_btn, image_name)
    getattr(pause_replay_btn, "configure").assert_called_once_with(image=image)
