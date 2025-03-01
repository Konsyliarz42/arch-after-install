import getpass
import shutil
from typing import Optional

import questionary

from .. import console
from ..constants import DOTFILES_PATH, HOME_PATH
from ..enums import ExitCode
from ..package import Command, Package


class PackageZsh(Package):
    NAME = "Zsh"

    @classmethod
    def install_ask(cls) -> Optional["PackageZsh"]:
        if cls._install_ask(f"Configure {cls.NAME}:"):
            return PackageZsh()

    def __init__(self) -> None:
        self.default_shell: str = questionary.confirm(
            "Use as default shell:", qmark="  -"
        ).unsafe_ask()
        super().__init__(
            name=self.NAME,
            pacman_pkgs=(
                "curl",
                "zsh",
                "zsh-autosuggestions",
                "zsh-syntax-highlighting",
            ),
            aur_urls=("https://aur.archlinux.org/zsh-pure-prompt.git",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        with console.status("Installing external packages"):
            exit_code = self.run_bash(
                self.stdout_path,
                Command(
                    'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended'
                ),
            )
            if exit_code != ExitCode.SUCCESS:
                return exit_code
        console.log("External packages installed", style="green")

        with console.status("Applying configuration"):
            # Copy config
            src_file = DOTFILES_PATH.joinpath("zshrc")
            dest_file = HOME_PATH.joinpath(".zshrc")
            shutil.copy(src_file, dest_file)
            # Copy custom functions
            src_file = DOTFILES_PATH.joinpath("zsh_functions")
            dest_file = HOME_PATH.joinpath(".zsh_functions")
            shutil.copy(src_file, dest_file)

            if self.default_shell:
                exit_code = self.run_bash(
                    self.stdout_path, Command(f"chsh -s /bin/zsh {getpass.getuser()}", password)
                )
                if exit_code != ExitCode.SUCCESS:
                    return exit_code
        console.log("Config file applied", style="green")

        return ExitCode.SUCCESS
