from typing import Optional

from ..package import Package


class PackageFonts(Package):
    NAME = "Fonts"

    @classmethod
    def install_ask(cls) -> Optional["PackageFonts"]:
        if cls._install_ask(f"Install {cls.NAME}:"):
            return PackageFonts()

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            pacman_pkgs=(
                "noto-fonts",
                "noto-fonts-emoji",
                "adobe-source-code-pro-fonts"
            ),
        )
