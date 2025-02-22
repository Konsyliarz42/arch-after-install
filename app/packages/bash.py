import shutil
from typing import Optional

from .. import console
from ..constants import DOTFILES_PATH, HOME_PATH
from ..enums import ExitCode
from ..package import Package


class PackageBash(Package):
    NAME = "Bash"

    @classmethod
    def install_ask(cls) -> Optional["PackageBash"]:
        if cls._install_ask(f"Configure {cls.NAME}:"):
            return PackageBash()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=("fastfetch",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        with console.status("Applying configuration"):
            src_file = DOTFILES_PATH.joinpath("bashrc")
            dest_file = HOME_PATH.joinpath(".bashrc")
            shutil.copy(src_file, dest_file)
        console.log("Config file applied", style="green")

        return ExitCode.SUCCESS
