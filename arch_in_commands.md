# Arch Linux Installation Guide - In Commands

## WiFi

```bash
iwctl station wlan0 connect <network>
```

## Partitioning

```bash
fdisk -l
fdisk <disk>
```

> a - bootable \
> d - delete \
> n - new \
> t - type

| nr  | type  | bootable | size | mount     | file system |
| --- | ----- | -------- | ---- | --------- | ----------- |
| 1   | uefi  | yes      | +1G  | /mnt/boot | fat32       |
| 2   | swap  | no       | +4G  | -         | -           |
| 3   | linux | no       | rest | /mnt      | ext4        |

```bash
mkfs.fat -F 32 <partition 1>
mkfs.ext4 <partition 3>
mkswap <partition 2>
```

```bash
mount /mnt <partition 3>
mount --mkdir /mnt/boot <partition 1>
swapon <partition 2>
```

## Installing

```bash
pacstrap -K /mnt base base-devel linux linux-firmware git nano networkmanager intel-ucode grub efibootmgr sudo
```

## Configuring

```bash
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
```

```bash
ln -sf /usr/share/zoneinfo/Poland /etc/localtime
hwclock --systohc
echo archlinux > /etc/hostname
mkinitcpio -P
```

```bash
useradd -m -G wheel <name>
passwd <name>
echo "<name> ALL=(ALL:ALL) ALL" > /etc/sudoers.d/<name>
```

## Bootloader

```bash
grub-install --target x86_64-efi --efi-directory /boot --bootloader-id GRUB
grub-mkconfig -o /boot/grub/grub.cfg
```

## Finishing

```bash
systemctl enable NetworkManager
exit
umount -R /mnt
reboot
nmtui
```

## Gnome

```bash
sudo pacman -Syu gdm gnome-browser-connector gnome-calculator gnome-control-center gnome-disk-utility gnome-firmware gnome-font-viewer gnome-keyring gnome-menus gnome-session gnome-settings-daemon gnome-shell gnome-terminal gnome-tweaks nautilus epiphany noto-fonts noto-fonts-emoji resources gnome-console gst-plugin-pipewire
sudo systemctl enable --now gdm
```

## OpenSSH

```bash
sudo pacman -Syu openssh
sudo systemctl enable --now sshd
```

## Docker

```bash
sudo pacman -Syu docker docker-compose docker-buildx
sudo groupadd docker
sudo usermod -aG docker $USER
reboot
```