from __future__ import annotations

from until_zero import App
from until_zero.constants import COMPILED_ENV


if COMPILED_ENV:
    import pyi_splash


if __name__ == "__main__":
    app = App()

    if COMPILED_ENV:
        pyi_splash.close()

    app.mainloop()
