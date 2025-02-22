from typing import Optional

from ..enums import ExitCode
from ..package import Package


class PackageOpenssh(Package):
    NAME = "OpenSSH server"

    @classmethod
    def install_ask(cls) -> Optional["PackageOpenssh"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageOpenssh()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=("openssh",),
            daemons=("sshd",),
        )

    def install(self, password) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        return self.enable_daemon(self.daemons[0], password, True)
