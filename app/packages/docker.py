from typing import Optional

from .. import console
from ..enums import ExitCode
from ..package import Command, Package


class PackageDocker(Package):
    NAME = "Docker"

    @classmethod
    def install_ask(cls) -> Optional["PackageDocker"]:
        if cls._install_ask(f"Install {cls.NAME}"):
            return PackageDocker()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=(
                "docker",
                "docker-compose",
            ),
            daemons=("docker",),
        )

    def install(self, password: str) -> ExitCode:
        exit_code = super().install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code

        with console.status("Adding user to docker group"):
            exit_code = self.run_bash(
                self.stdout_path, Command("usermod -aG docker $USER", password)
            )
            if exit_code != ExitCode.SUCCESS:
                return exit_code
        console.log("User added to docker group", style="green")

        return self.enable_daemon(self.daemons[0], password)
