from typing import Optional

from ..enums import ExitCode
from ..package import Package


class PackageWifi(Package):
    NAME = "WiFi RTL88x2BU driver"

    @classmethod
    def install_ask(cls) -> Optional["PackageWifi"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageWifi()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=(
                "bc",
                "dkms",
                "iwd",
                "linux-headers",
            ),
            aur_urls=("https://aur.archlinux.org/rtl88x2bu-dkms-git.git",),
            daemons=("iwd",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        return self.enable_daemon(self.daemons[0], password, True)
