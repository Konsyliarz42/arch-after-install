from typing import Optional

from app.enums import ExitCode

from ..package import Package


class PackageNetworkManager(Package):
    NAME = "Network Manager"

    @classmethod
    def install_ask(cls) -> Optional["PackageNetworkManager"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageNetworkManager()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=("networkmanager",),
            daemons=("NetworkManager",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        return self.enable_daemon(self.daemons[0], password, True)
