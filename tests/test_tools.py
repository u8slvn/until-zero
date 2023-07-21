from __future__ import annotations

import pytest

from PIL import ImageTk

from tests import FIXTURES_DIR
from until_zero.tools import format_time_for_human
from until_zero.tools import open_alpha_image


@pytest.mark.parametrize(
    "timer, expected",
    [
        (0, "0s"),
        (5, "5s"),
        (60, "1m"),
        (65, "1m, 5s"),
        (60 * 60, "1h"),
        (60 * 60 + 5, "1h, 5s"),
        (60 * 60 + 60, "1h, 1m"),
        (60 * 60 + 60 + 5, "1h, 1m, 5s"),
        (24 * 60 * 60, "1day"),
        (24 * 60 * 60 + 5, "1day, 5s"),
        (24 * 60 * 60 + 60 + 5, "1day, 1m, 5s"),
        (24 * 60 * 60 + 60 * 60 + 60 + 5, "1day, 1h, 1m, 5s"),
        (48 * 60 * 60 + 60 * 60 + 60 + 5, "2days, 1h, 1m, 5s"),
        (123456789, "1428days, 21h, 33m, 9s"),
    ],
)
def test_format_timer_for_human(timer, expected):
    result = format_time_for_human(time=timer)

    assert result == expected


def test_open_alpha_image(monkeypatch_tkinter):
    image = open_alpha_image(FIXTURES_DIR.joinpath("test-alpha-image.png"))

    assert isinstance(image, ImageTk.PhotoImage)
