from __future__ import annotations

import tkinter

import _tkinter
import pytest


@pytest.fixture(autouse=True)
def clean_tkinter():
    tkinter._default_root = None


@pytest.fixture
def test_tkinter(monkeypatch, mocker):
    monkeypatch.setattr(tkinter, "_default_root", mocker.MagicMock())


class TestAppBuilder:
    def __init__(self):
        self.app = None

    def build_app(self, app_cls):
        class TestApp(app_cls):
            def pump_events(self):
                while self.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT):
                    pass

        self.app = TestApp()

    def __call__(self, app_cls: tkinter.Tk):
        self.build_app(app_cls=app_cls)
        self.app.pump_events()
        return self.app

    def destroy(self):
        if self.app is not None:
            self.app.pump_events()
            self.app.destroy()


@pytest.fixture
def test_app():
    test_app_builder = TestAppBuilder()

    yield test_app_builder

    test_app_builder.destroy()
