from __future__ import annotations

from until_zero import App


def test_timers_dont_start_if_input_is_empty(mocker, test_app):
    app = test_app(app_cls=App)
    send_event = mocker.patch("until_zero.app.Session.send_event")
    app.config_timers.start_button.invoke()
    app.pump_events()

    send_event.assert_not_called()


def test_timers_can_be_setup_with_pomodoro_buttons(test_app):
    app = test_app(app_cls=App)
    app.config_timers.task_btn.invoke()
    app.config_timers.short_break_btn.invoke()
    app.config_timers.long_break_btn.invoke()
    app.pump_events()

    assert app.config_timers.timers_input.input_var.get() == "25+5+20"


def test_timers_can_be_reset(test_app):
    app = test_app(app_cls=App)
    app.config_timers.task_btn.invoke()
    app.config_timers.short_break_btn.invoke()
    app.config_timers.long_break_btn.invoke()
    app.config_timers.clean_btn.invoke()
    app.pump_events()

    assert app.config_timers.timers_input.input_var.get() == ""


# def test_timers_start_on_return_event(test_app):
#     test_app.config_timers.timers_input.insert(0, "5")
#     test_app.config_timers.timers_input.event_generate("<Return>")
#     test_app.pump_events()
#
#     assert test_app.config_timers.timers_input.input_var.get() == "5"
#     assert test_app.session.timer_count == 1
#     assert test_app.timers_window.winfo_viewable() == 1
#     assert test_app.winfo_viewable() == 0
#     assert test_app.timers_window.bongo_cat.stopped is False
#     assert test_app.timers_window.timer_display.time_label.cget("text") == "5m"


def test_timers_start(test_app):
    app = test_app(app_cls=App)
    app.config_timers.task_btn.invoke()
    app.config_timers.short_break_btn.invoke()
    app.config_timers.start_button.invoke()
    app.pump_events()

    assert app.session.timer_count == 2
    assert app.timers_window.winfo_viewable() == 1
    assert app.winfo_viewable() == 0
    assert app.timers_window.bongo_cat.stopped is False
    assert app.timers_window.timer_display.time_label.cget("text") == "25m"


def test_started_timers_can_be_paused_an_restart(test_app):
    app = test_app(app_cls=App)
    app.config_timers.task_btn.invoke()
    app.config_timers.start_button.invoke()
    app.timers_window.pause_btn.invoke()
    app.pump_events()

    assert app.timers_window.paused is True
    assert app.timers_window.bongo_cat.stopped is True

    app.timers_window.pause_btn.invoke()
    app.pump_events()

    assert app.timers_window.paused is False
    assert app.timers_window.bongo_cat.stopped is False


def test_timers_stop(test_app):
    app = test_app(app_cls=App)
    app.config_timers.task_btn.invoke()
    app.config_timers.short_break_btn.invoke()
    app.config_timers.start_button.invoke()
    app.timers_window.stop_btn.invoke()
    app.pump_events()

    assert app.timers_window.winfo_viewable() == 0
    assert app.winfo_viewable() == 1
    assert app.focus_get() is app.config_timers.timers_input
