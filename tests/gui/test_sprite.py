from __future__ import annotations

import tkinter

import pytest

from tests import FIXTURES_DIR
from until_zero.gui.sprite import Sprite
from until_zero.tools import open_alpha_image


@pytest.fixture
def sprite_configure(monkeypatch, mocker):
    # TODO: Refactor this
    app = tkinter.Tk()

    def return_none_after_max_calls(func, max_calls):
        def wrapper(*args, **kwargs):
            if wrapper.nb_calls == max_calls:
                app.quit()

            wrapper.nb_calls += 1
            return func(*args, **kwargs)

        wrapper.nb_calls = 0
        return wrapper

    configure = mocker.Mock()
    monkeypatch.setattr(
        tkinter.Label, "after", return_none_after_max_calls(tkinter.Label.after, 3)
    )
    monkeypatch.setattr(tkinter.Label, "configure", configure)

    yield app, configure


def test_sprite(mocker, sprite_configure):
    app, configure = sprite_configure
    frame1 = (open_alpha_image(FIXTURES_DIR.joinpath("test-alpha-image.png")),)
    frame2 = (open_alpha_image(FIXTURES_DIR.joinpath("test-alpha-image.png")),)
    frame3 = open_alpha_image(FIXTURES_DIR.joinpath("test-alpha-image.png"))
    frames = [frame1, frame2, frame3]
    Sprite(app, width=270, height=270, frames=frames, frame_rate=1)
    app.mainloop()

    assert configure.call_args_list == [
        mocker.call(background="#ffe100"),
        mocker.call(image=frame1),
        mocker.call(image=frame2),
        mocker.call(image=frame3),
        mocker.call(image=frame1),
    ]
