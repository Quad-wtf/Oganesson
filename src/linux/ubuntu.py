import os
import subprocess

HOME = os.path.expanduser("~")

APPS = {
    "apt": ["/var/cache/apt/archives/*"],
    "pip": [os.path.join(HOME, ".cache", "pip", "*")],
    "snap": ["/var/lib/snapd/cache/*"],
}

EXTRA_PATHS_ON_DONE = [
    "/tmp/*",
    os.path.join(HOME, ".cache", "*"),
]

def clear_special(name: str) -> bool:
    if name == "apt":
        subprocess.run(
            ["sudo", "apt", "clean"],
            check=True
        )
        return True
    return False
