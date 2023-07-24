from __future__ import annotations

from until_zero.gui.draggable import Draggable


def test_draggable(mocker, test_session):
    app = test_session.root
    app.winfo_pointerxy = mocker.Mock(return_value=(100, 100))
    app.geometry = mocker.Mock(return_value="50+50+50")
    draggable = Draggable(app, mocker.Mock())
    draggable.pack()
    app.add_test_action(draggable.event_generate, "<Button-1>")
    app.add_test_action(draggable.event_generate, "<B1-Motion>")
    app.add_test_action(draggable.event_generate, "<ButtonRelease-1>")

    app.run_test_actions()

    assert draggable.pos_x == 0
    assert draggable.pos_y == 0
    assert app.geometry.call_args_list == [mocker.call(), mocker.call("+-51+-51")]
