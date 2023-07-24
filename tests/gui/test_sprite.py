from __future__ import annotations

import tkinter

import pytest

from tests import FIXTURES_DIR
from until_zero import constants as const
from until_zero.events import Events
from until_zero.gui.sprite import BongoCat
from until_zero.gui.sprite import Sprite
from until_zero.tools import open_alpha_image


@pytest.fixture
def sprite_app(monkeypatch):
    app = tkinter.Tk()

    def stop_sprite_and_quit_after_max_calls(func, max_calls):
        # This decorator will run the after method max_calls time and then stop the sprite
        # and quit the app.
        def wrapper(self, *args, **kwargs):
            if wrapper.nb_calls == max_calls:
                self.stop()
                func(self, 10, app.quit)

            wrapper.nb_calls += 1
            return func(self, *args, **kwargs)

        wrapper.nb_calls = 0
        return wrapper

    monkeypatch.setattr(
        Sprite, "after", stop_sprite_and_quit_after_max_calls(tkinter.Label.after, 3)
    )

    yield app

    app.destroy()


def test_sprite_anime_frames(mocker, monkeypatch, sprite_app):
    monkeypatch.setattr(Sprite, "configure", mocker.Mock())
    frame1 = open_alpha_image(FIXTURES_DIR.joinpath("test-alpha-image.png"))
    frame2 = open_alpha_image(FIXTURES_DIR.joinpath("test-alpha-image.png"))
    frame3 = open_alpha_image(FIXTURES_DIR.joinpath("test-alpha-image.png"))
    frames = [frame1, frame2, frame3]

    sprite = Sprite(sprite_app, width=270, height=270, frames=frames, frame_rate=1)

    sprite_app.mainloop()

    assert sprite.configure.call_args_list == [
        mocker.call(background=const.YELLOW),
        mocker.call(image=frame1),
        mocker.call(image=frame2),
        mocker.call(image=frame3),
        mocker.call(image=frame1),
    ]


@pytest.mark.parametrize(
    "action, event",
    [
        ("stop", Events.TIMERS_STOPPED),
        ("stop", Events.PAUSE_TIMER),
        ("start", Events.UNPAUSE_TIMER),
    ],
)
def test_bongo_cat_stop_or_start_on_event(mocker, monkeypatch, test_session, action, event):
    mocker.patch("until_zero.gui.sprite.session", test_session)
    app = test_session.root
    app.add_test_action(test_session.send_event, event)
    bongo_cat = BongoCat(app)
    monkeypatch.setattr(bongo_cat, action, mocker.Mock())

    app.run_test_actions()

    getattr(bongo_cat, action).assert_called_once()
