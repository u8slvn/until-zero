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
def test_pause_replay_button_on_events(mocker, neutral_test_session, event, image_name):
    mocker.patch("until_zero.gui.button.session", neutral_test_session)
    app = neutral_test_session.root
    app.add_test_action(neutral_test_session.send_event, event)
    pause_replay_btn = PauseReplayButton(app, command=mocker.Mock())
    setattr(pause_replay_btn, "configure", mocker.Mock())

    app.run_test_actions()

    image = getattr(pause_replay_btn, image_name)
    getattr(pause_replay_btn, "configure").assert_called_once_with(image=image)
