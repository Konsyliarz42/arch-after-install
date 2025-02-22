import shutil
from typing import Optional

from .. import console
from ..constants import DOTFILES_PATH, HOME_PATH
from ..enums import ExitCode
from ..package import Package


class PackageNano(Package):
    NAME = "Nano"

    @classmethod
    def install_ask(cls) -> Optional["PackageNano"]:
        if cls._install_ask(f"Configure {cls.NAME}:"):
            return PackageNano()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=(
                "nano",
                "nano-syntax-highlighting",
            ),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        with console.status("Applying configuration"):
            src_file = DOTFILES_PATH.joinpath("nanorc")
            dest_file = HOME_PATH.joinpath(".config", "nano", "nanorc")
            shutil.copy(src_file, dest_file)
        console.log("Config file applied", style="green")

        return ExitCode.SUCCESS
