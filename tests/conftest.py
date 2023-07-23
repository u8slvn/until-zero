from __future__ import annotations

import tkinter

from functools import partial

import pytest

from until_zero import session


@pytest.fixture(autouse=True)
def clean_tkinter():
    tkinter._default_root = None


@pytest.fixture
def test_tkinter(monkeypatch, mocker):
    monkeypatch.setattr(tkinter, "_default_root", mocker.Mock())


class TestApp(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


@pytest.fixture
def test_session() -> session._Session:
    test_session = session._Session()
    test_app = TestApp()
    test_session.register_root(root=test_app)

    yield test_session

    test_app.destroy()
    del test_session
