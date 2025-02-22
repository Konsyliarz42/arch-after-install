import shutil
from typing import Optional

from app.enums import ExitCode

from .. import console
from ..constants import DOTFILES_PATH, HOME_PATH
from ..package import Package


class PackageVscode(Package):
    NAME = "VS Code"

    @classmethod
    def install_ask(cls) -> Optional["PackageVscode"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageVscode()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=(
                "alsa-lib",
                "gcc-libs",
                "glibc",
                "gnupg",
                "gtk3",
                "libnotify",
                "libsecret",
                "libxkbfile",
                "libxss",
                "lsof",
                "nss",
                "shared-mime-info",
                "xdg-utils",
            ),
            aur_urls=("https://aur.archlinux.org/visual-studio-code-bin.git",),
        )

    def install(self, password):
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        with console.status("Applying configuration"):
            src_file = DOTFILES_PATH.joinpath("keybindings.json")
            dest_file = HOME_PATH.joinpath(".config", "Code", "User", "keybindings.json")
            shutil.copy(src_file, dest_file)
        console.log("Config file applied", style="green")

        return ExitCode.SUCCESS
