import os
import subprocess

HOME = os.path.expanduser("~")

APPS = {
    "pacman": ["/var/cache/pacman/pkg/*"],
    "pip": [os.path.join(HOME, ".cache", "pip", "*")],
    "npm": [os.path.join(HOME, ".npm", "*")],
}

EXTRA_PATHS_ON_DONE = [
    "/tmp/*",
    os.path.join(HOME, ".cache", "*"),
]

def clear_special(name: str) -> bool:
    if name == "pacman":
        subprocess.run(
            ["sudo", "pacman", "-Sc", "--noconfirm"],
            check=True
        )
        return True
    return False
