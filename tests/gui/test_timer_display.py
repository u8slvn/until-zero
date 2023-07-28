from __future__ import annotations

from until_zero import constants as const
from until_zero.gui.timer_display import TimersProgress


def test_timers_progress(mocker, test_session):
    app = test_session.root
    timers_progress = TimersProgress(app)
    timers_progress.set_timer_count(count=3)
    timers_progress.winfo_width = mocker.Mock(return_value=31)
    timers_progress.create_rectangle = mocker.Mock()

    timers_progress.update_progress(timer_index=2)

    assert timers_progress.create_rectangle.call_args_list == [
        mocker.call(0.0, 0, 9.0, 2, fill=const.BLUE, outline=""),
        mocker.call(11.0, 0, 20.0, 2, fill=const.PURPLE, outline=""),
        mocker.call(22.0, 0, 31, 2, fill=const.WHITE, outline=""),
    ]
