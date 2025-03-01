from typing import Optional

from .. import console
from ..enums import ExitCode
from ..package import Command, Package


class PackageGnome(Package):
    NAME = "GNOME environment"

    @classmethod
    def install_ask(cls) -> Optional["PackageGnome"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageGnome()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=(
                "dcon",
                "gdm",
                "gnome-browser-connector",
                "gnome-calculator",
                "gnome-control-center",
                "gnome-disk-utility",
                "gnome-firmware",
                "gnome-font-viewer",
                "gnome-keyring",
                "gnome-menus",
                "gnome-session",
                "gnome-settings-daemon",
                "gnome-shell",
                "gnome-terminal",
                "gnome-tweaks",
                "nautilus",
                "resourcesxdg-user-dirs",
                "xdg-user-dirs-gtk",
            ),
            aur_urls=(
                "https://aur.archlinux.org/gnome-shell-extension-alphabetical-grid-extension.git",
                "https://aur.archlinux.org/gnome-shell-extension-arch-update.git",
            ),
            daemons=("gdm",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        with console.status("Applying configuration"):
            exit_code = self.run_bash(
                self.stdout_path,
                Command("timedatectl set-local-rtc 1 --adjust-system-clock", password),
            )
            if exit_code != ExitCode.SUCCESS:
                return exit_code
        console.log("Config file applied", style="green")

        return self.enable_daemon(self.daemons[0], password)
