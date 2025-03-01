from typing import Optional

import questionary

from .. import console
from ..enums import ExitCode
from ..package import Command, Package


class PackageWireguard(Package):
    NAME = "WireGuard"

    @classmethod
    def install_ask(cls) -> Optional["PackageWireguard"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageWireguard()

    def __init__(self) -> None:
        self.config_path: str = questionary.path("Config file:", qmark="  -").unsafe_ask()
        super().__init__(
            name=self.NAME,
            pacman_pkgs=("wireguard-tools",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        if not self.config_path:
            return ExitCode.SUCCESS

        with console.status("Connect with VPN"):
            exit_code = self.run_bash(
                self.stdout_path,
                Command(f"nmcli connection import type wireguard file {self.config_path}"),
            )
            if exit_code != ExitCode.SUCCESS:
                return exit_code
        console.log("VPN connected", style="green")

        return ExitCode.SUCCESS
