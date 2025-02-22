from os import environ
from pathlib import Path
from typing import Final

HOME_PATH: Final = Path(environ["HOME"])
AUR_PATH: Final = HOME_PATH.joinpath(".aur")
STDOUT_PATH: Final = Path("stdout")
DOTFILES_PATH: Final = Path("dotfiles")
