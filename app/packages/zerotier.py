from typing import Optional

import questionary

from .. import console
from ..enums import ExitCode
from ..package import Command, Package


class PackageZerotier(Package):
    NAME = "ZeroTier One"

    @classmethod
    def install_ask(cls) -> Optional["PackageZerotier"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageZerotier()

    def __init__(self) -> None:
        self.network = questionary.text("Network ID:", qmark="  -").ask()
        super().__init__(
            name=self.NAME,
            pacman_pkgs=("zerotier-one",),
            daemons=("zerotier-one",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        exit_code = self.enable_daemon(self.daemons[0], password, True)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        with console.status("Connect with VPN"):
            exit_code = self.run_bash(Command(f"zerotier-cli join {self.network}", password))
            if exit_code != ExitCode.SUCCESS:
                return exit_code
        console.log("VPN connected", style="green")

        return ExitCode.SUCCESS
