from typing import Optional

import questionary

from ..package import Package


class PackageXorg(Package):
    NAME = "X.Org"

    @classmethod
    def install_ask(cls) -> Optional["PackageXorg"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageXorg()

    def __init__(self) -> None:
        driver = questionary.select(
            "Graphic driver:",
            choices=(
                questionary.Choice("xorg-drivers", "xorg-drivers"),
                questionary.Choice("xf86-video-amdgpu (AMD)", "xf86-video-amdgpu"),
                questionary.Choice("xf86-video-ati (ATI)", "xf86-video-ati"),
                questionary.Choice("xf86-video-intel (Intel)", "xf86-video-intel"),
                questionary.Choice("xf86-video-nouveau (NVIDIA Open Source)", "xf86-video-nouveau"),
                questionary.Choice("nvidia (NVIDIA Proprietary)", "nvidia"),
            ),
            qmark="  -",
        ).unsafe_ask()
        super().__init__(
            name=self.NAME,
            pacman_pkgs=("xorg", driver),
        )
