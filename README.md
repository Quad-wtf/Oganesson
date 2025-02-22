# ![Oganesson Logo](./assets/Oganesson.png)

Oganesson is a free, open-source, cache deleter for Windows and Linux. (see end of README for further information). It suports a wide range of applications. 

| Version | Support |
|---------|---------|
|  1.0.0  |  Active |

# Installing

## Windows

You need to have atleast Python 3.12 installed.
First, install all the dependencies.
Colorama:
```
pip install -U colorama
```
Then, on GitHub, go to releases, latest stable, scroll down and click the .exe file. The file will guide you through the installation.
(for me, https://www.youtube.com/watch?v=WlBLnNd2DNU)

> [!NOTE]
> Oganesson is not supported on Linux distributions now. You can compile it, but the program wont work.
## Linux
First, install all the dependencies.
### Arch
Update the system.
```
sudo pacman -Syu
```
Pipx:
```
sudo pacman -S python-pipx
```
Install PyInstaller through pipx:
```
pipx install pyinstaller
```
Ensure your PATH:
```
pipx ensurepath
```
Then, run:
```
make
make run
```
### Ubuntu
Update the system.
```
sudo apt update && sudo apt upgrade
```
If it says this: "24 packages can be upgraded. Run 'apt list --upgradable' to see them." after typing in that command, type in:
```
sudo apt upgrade
```
Install pipx:
```
sudo apt install pipx
```
Install PyInstaller through pipx:
```
pipx install pyinstaller
```
Ensure your PATH:
```
pipx ensurepath
```
Then, run:
```
make
make run
```
# Supported Apps
Pip,
MSYS2,
CapCut,
npm,
scoop,
War Thunder

# Operating systems that Oganesson supports

1. Windows

2. ArchLinux

3. Ubuntu

For further questions read "FAQ.md"

colorama module: https://github.com/tartley/colorama
