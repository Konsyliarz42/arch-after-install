import subprocess
from pathlib import Path
from typing import Optional

import questionary

from app import console
from app.constants import AUR_PATH, STDOUT_PATH
from app.enums import ExitCode


class Command:
    def __init__(self, cmd: str, sudo: Optional[str] = None) -> None:
        self.cmd = cmd
        self.password = sudo

    @property
    def _cmd(self) -> str:
        return self.cmd if not self.password else f'echo "{self.password}" | sudo -S {self.cmd}'


class Package:
    @classmethod
    def _install_ask(cls, msg: str) -> bool:
        return questionary.confirm(msg).unsafe_ask()

    @classmethod
    def install_ask(cls) -> Optional["Package"]:
        raise Exception("Method not overwritten")

    @classmethod
    def run_bash(cls, stdout_path: Path, cmd: Command, stdin: Optional[str] = None) -> ExitCode:
        command_stdin = f"[INPUT] Execute command: {stdin or cmd.cmd}\n"
        try:
            # Because subprocess revert order of lines
            with stdout_path.open("a") as file:
                file.write(command_stdin)
            with stdout_path.open("a") as file:
                result = subprocess.run(cmd._cmd, shell=True, stderr=subprocess.STDOUT, stdout=file)
            return_code = ExitCode(result.returncode)
            if return_code != ExitCode.SUCCESS:
                stdout_text = stdout_path.read_text()
                cmd_index = stdout_text.find(command_stdin)
                console.log("ERROR:", style="red bold")
                console.log(stdout_text[cmd_index:])
                return return_code
        except KeyboardInterrupt:
            return ExitCode.CANCELED

        return ExitCode.SUCCESS

    @classmethod
    def run_bash_sequence(
        cls, stdout_path: Path, cmds: tuple[Command, ...], break_when_fail: bool = True
    ) -> ExitCode:
        operator = " && " if break_when_fail else "; "
        stdin = operator.join((cmd.cmd for cmd in cmds))
        cmd = Command(operator.join((cmd._cmd for cmd in cmds)))

        return cls.run_bash(stdout_path, cmd, stdin)

    def __init__(
        self,
        name: str,
        pacman_pkgs: Optional[tuple[str, ...]] = None,
        aur_urls: Optional[tuple[str, ...]] = None,
        daemons: Optional[tuple[str, ...]] = None,
    ) -> None:
        self.name = name
        self.pacman_pkgs = pacman_pkgs
        self.aur_urls = aur_urls
        self.daemons = daemons

        self.stdout_path = STDOUT_PATH.joinpath(f"{self.__class__.__name__}.txt")

    def install_pacman(self, password: str) -> ExitCode:
        with console.status("Installing official packages"):
            cmd = Command(f"pacman -Syu --noconfirm {' '.join(self.pacman_pkgs)}", password)
            exit_code = self.run_bash(self.stdout_path, cmd)

        if exit_code == ExitCode.SUCCESS:
            console.log("Official packages installed", style="green")

        return exit_code

    def install_aur(self, password: str) -> ExitCode:
        if not AUR_PATH.exists():
            with console.status("Creating AUR directory"):
                AUR_PATH.mkdir()
            console.log(f"Aur directory created: {AUR_PATH}", style="green")

        with console.status("Installing AUR packages"):
            for url in self.aur_urls:
                name = url.rsplit("/", 1)[-1].removesuffix(".git")
                pkg_path = AUR_PATH.joinpath(name).absolute()

                # Download and build
                cmds = (
                    Command(f"git clone {url} {pkg_path}"),
                    Command(f"cd {pkg_path}"),
                    Command(f"makepkg -s"),
                )
                exit_code = self.run_bash_sequence(self.stdout_path, cmds)
                if exit_code != ExitCode.SUCCESS:
                    return exit_code

                # Find package
                pkg_file = next(pkg_path.glob("*.pkg.tar.zst"), None)
                if not pkg_file:
                    return ExitCode.NOT_FOUND

                # Install package
                exit_code = self.run_bash(
                    self.stdout_path,
                    Command(f"pacman -U --noconfirm {pkg_file.absolute()}", password),
                )
                if exit_code != ExitCode.SUCCESS:
                    return exit_code

        if exit_code == ExitCode.SUCCESS:
            console.log("AUR packages installed", style="green")

        return ExitCode.SUCCESS

    def enable_daemon(self, name: str, password: str, now: bool = False) -> ExitCode:
        with console.status(f"Enabling daemon: {name}"):
            cmd = Command(f"systemctl enable{' --now ' if now else ' '}{name}", password)
            exit_code = self.run_bash(self.stdout_path, cmd)
        console.log("Daemon enabled", style="green")

        return exit_code

    def install(self, password: str) -> ExitCode:
        console.rule(self.name)
        console.print(
            f"For full process output check: {self.stdout_path.absolute()}\n",
            style="bright_black",
        )

        if self.pacman_pkgs:
            exit_code = self.install_pacman(password)
            if exit_code != ExitCode.SUCCESS:
                return exit_code

        if self.aur_urls:
            exit_code = self.install_aur(password)
            if exit_code != ExitCode.SUCCESS:
                return exit_code

        return ExitCode.SUCCESS
