from __future__ import annotations

from pathlib import Path


# --- Locations
ROOT_DIR = Path(__file__).parent
ASSETS_DIR = ROOT_DIR.joinpath("assets")

# --- Window info
WINDOW_TITLE = "Until Zero - タイマー"
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 145
WINDOW_TIMER_WIDTH = 350
WINDOW_TIMER_HEIGHT = 30

# --- Timer options
OPTION_TASK = 25
OPTION_SHORT_BREAK = 5
OPTION_LONG_BREAK = 20

# --- Timer Config
TIMERS_INPUT_LENGTH = 70

# --- Text
SUM_TIMERS_PLACEHOLDER = "0s"
SUM_TIMERS_ERROR = "To the infinity and beyond!"

# --- Fonts
FONT = "CozetteVector"
DEFAULT_SIZE = 12
POMODORO_PREVIEW_SIZE = 10
OPTION_BTN_SIZE = 9
START_BTN_SIZE = 12
CLEAN_BTN_SIZE = 7
TIMER_WINDOW_BTN_SIZE = 12

# --- Color palette
WHITE = "#ffffff"
BLACK = "#000000"
RED = "#c5143e"
DARK_RED = "#c22349"
YELLOW = "#ffe100"
DARK_YELLOW = "#f0ac00"
BLUE = "#10ebeb"
DARK_BLUE = "#27b3b3"
PURPLE = "#9370db"
DARK_PURPLE = "#7b4ddb"
