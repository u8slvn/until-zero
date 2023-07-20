from __future__ import annotations

import tkinter

import pytest


@pytest.fixture
def monkeypatch_tkinter(monkeypatch, mocker):
    monkeypatch.setattr(tkinter, "_default_root", mocker.Mock())
