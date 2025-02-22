from .bash import PackageBash
from .docker import PackageDocker
from .fonts import PackageFonts
from .gnome import PackageGnome
from .nano import PackageNano
from .network_manager import PackageNetworkManager
from .openssh import PackageOpenssh
from .vscode import PackageVscode
from .wifi import PackageWifi
from .wireguard import PackageWireguard
from .xorg import PackageXorg
from .zerotier import PackageZerotier
from .zsh import PackageZsh

__all__ = [
    PackageBash,
    PackageDocker,
    PackageFonts,
    PackageGnome,
    PackageNano,
    PackageNetworkManager,
    PackageOpenssh,
    PackageVscode,
    PackageWifi,
    PackageWireguard,
    PackageXorg,
    PackageZerotier,
    PackageZsh,
]
