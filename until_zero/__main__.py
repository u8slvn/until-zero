from __future__ import annotations

from until_zero import App
from until_zero.constants import COMPILED_ENV
from until_zero.font import load_font


if COMPILED_ENV:
    import pyi_splash  # type: ignore


if __name__ == "__main__":
    load_font()
    app = App()

    if COMPILED_ENV:
        pyi_splash.close()

    app.mainloop()
