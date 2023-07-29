from __future__ import annotations

import tkinter

from functools import partial

import _tkinter
import pytest

from until_zero import App
from until_zero import session


@pytest.fixture(autouse=True)
def clean_tkinter():
    tkinter._default_root = None


@pytest.fixture(autouse=True)
def test_session(monkeypatch):
    test_session = session._Session()
    monkeypatch.setattr(session, "session", test_session)

    return test_session


@pytest.fixture
def test_tkinter(monkeypatch, mocker):
    monkeypatch.setattr(tkinter, "_default_root", mocker.MagicMock())


def build_test_app(app_cls):
    class TestApp(app_cls):
        def __init__(self):
            super().__init__()
            self._test_actions = []

        def add_test_action(self, callback, *args):
            self._test_actions.append(partial(callback, *args))

        def run_test_actions(self):
            time = 10
            for action in self._test_actions:
                self.after(time, action)
                time += time

            self.after(time + 20, self.quit)
            self.mainloop()

    return TestApp()


@pytest.fixture
def neutral_test_session(test_session):
    test_app = build_test_app(app_cls=tkinter.Tk)
    test_session.register_root(root=test_app)

    yield test_session

    test_app.destroy()
    del test_session


@pytest.fixture
def test_app():
    class TestApp(App):
        def pump_events(self):
            while self.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT):
                pass

    test_app = TestApp()
    test_app.pump_events()

    yield test_app

    test_app.destroy()
    test_app.pump_events()
