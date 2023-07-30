from __future__ import annotations

from importlib import metadata

from until_zero.app import App


__app_name__ = "until_zero"
__version__ = metadata.version(__app_name__)

__all__ = ["__app_name__", "__version__", "App"]
