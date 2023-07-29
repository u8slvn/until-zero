from __future__ import annotations

import tkinter

from until_zero.gui.draggable import Draggable


def test_draggable(mocker, test_app):
    app = test_app(app_cls=tkinter.Tk)
    app.winfo_pointerxy = mocker.Mock(return_value=(100, 100))
    app.geometry = mocker.Mock(return_value="50+50+50")
    reset_pos = mocker.Mock()
    draggable = Draggable(app, reset_pos)
    draggable.pack()
    app.pump_events()

    draggable.event_generate("<Button-1>")
    draggable.event_generate("<B1-Motion>")
    draggable.event_generate("<ButtonRelease-1>")
    # draggable.event_generate("<Double-1>")

    assert draggable.pos_x == 0
    assert draggable.pos_y == 0
    assert app.geometry.call_args_list == [mocker.call(), mocker.call("+-51+-51")]
    # reset_pos.assert_called_once()
