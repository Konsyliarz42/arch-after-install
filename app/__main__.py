import shutil
from typing import Optional

import questionary

from app.constants import STDOUT_PATH

from . import console, packages
from .enums import ExitCode
from .package import Package


def get_packages() -> dict[str, Package]:
    pkgs: dict[str, Optional[Package]] = {}

    pkgs["wifi"] = packages.PackageWifi.install_ask()
    pkgs["network_manager"] = packages.PackageNetworkManager.install_ask()
    pkgs["openssh"] = packages.PackageOpenssh.install_ask()
    pkgs["xorg"] = packages.PackageXorg.install_ask()
    pkgs["fonts"] = packages.PackageFonts.install_ask()

    pkgs["gnome"] = packages.PackageGnome.install_ask()
    if pkgs.get("gnome") and not pkgs.get("network_manager"):
        console.print(
            f"{packages.PackageNetworkManager.NAME} is required by {packages.PackageGnome.NAME}"
        )
        pkgs["network_manager"] = packages.PackageNetworkManager()
    if pkgs.get("gnome") and not pkgs.get("fonts"):
        console.print(
            f"{packages.PackageFonts.NAME} is recommended to use with {packages.PackageGnome.NAME}"
        )
        pkgs["fonts"] = packages.PackageFonts.install_ask()

    pkgs["vscode"] = packages.PackageVscode.install_ask()
    pkgs["docker"] = packages.PackageDocker.install_ask()

    pkgs["wireguard"] = packages.PackageWireguard.install_ask()
    if pkgs.get("wireguard") and not pkgs.get("network_manager"):
        console.print(
            f"{packages.PackageNetworkManager.NAME} is required by {packages.PackageWireguard.NAME}"
        )
        pkgs["network_manager"] = packages.PackageNetworkManager()

    pkgs["zerotier"] = packages.PackageZerotier.install_ask()

    print()

    pkgs["bash"] = packages.PackageBash.install_ask()
    pkgs["zsh"] = packages.PackageZsh.install_ask()
    pkgs["nano"] = packages.PackageNano.install_ask()

    return pkgs


def main() -> ExitCode:
    # Get packages list to install
    pkgs = get_packages()
    print()
    confirm = questionary.confirm("Confirm installation:").unsafe_ask()
    if not confirm:
        return ExitCode.CANCELED

    # Recreate bash output files
    if STDOUT_PATH.exists():
        shutil.rmtree(STDOUT_PATH)
    STDOUT_PATH.mkdir()

    # Install packages
    password = questionary.password("User password:").unsafe_ask()
    for pkg in pkgs.values():
        if pkg is None:
            continue
        print()
        exit_code = pkg.install(password)
        if exit_code != ExitCode.SUCCESS:
            return exit_code
        console.log("Finished", style="bold bright_green")

    console.print("\n==== All packages installed ====", style="bold green")

    return ExitCode.SUCCESS


if __name__ == "__main__":
    console.print("==== Welcome in Arch After Install (AAI) ====\n", style="bold cyan")

    try:
        exit(main())
    except KeyboardInterrupt:
        exit(ExitCode.CANCELED)
