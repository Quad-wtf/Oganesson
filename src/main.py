import os
import subprocess
import platform
import glob
from colorama import init, Fore, Style


def expand_paths(path):
    # Expand wildcards for files/directories
    return glob.glob(path)


class CacheCleaner:
    def __init__(self):
        init(autoreset=True)
        self.os_impl = None

        if platform.system().lower() == "linux":
            with open("/etc/os-release") as f:
                os_info = f.read().lower()

            if "arch" in os_info:
                from linux import arch

                self.os_impl = arch
            elif "ubuntu" in os_info or "debian" in os_info:
                from linux import ubuntu

                self.os_impl = ubuntu

        if platform.system().lower() == "windows":
            self.user_home = os.path.expandvars("%USERPROFILE%")
        else:  # Linux / macOS
            self.user_home = os.path.expanduser("~")

        self.deferred_paths = []
        self.apps = {
            "pip": ["pip_cache"],
            "msys2": [
                os.path.join("C:", "msys64", "var", "cache", "pacman", "pkg", "*")
            ],
            "capcut": [
                os.path.join(
                    self.user_home,
                    "AppData",
                    "Local",
                    "CapCut",
                    "User Data",
                    "Log",
                    "alog",
                    "log",
                    "*",
                ),
                os.path.join(
                    self.user_home,
                    "AppData",
                    "Local",
                    "CapCut",
                    "User Data",
                    "Log",
                    "alog",
                    "cache",
                    "*",
                ),
                os.path.join(
                    self.user_home,
                    "AppData",
                    "Local",
                    "CapCut",
                    "User Data",
                    "Cache",
                    "*",
                ),
            ],
            "npm": [os.path.join(self.user_home, "AppData", "Local", "npm-cache", "*")],
            "scoop": ["scoop_cache"],
            "war thunder": [
                os.path.join(
                    "C:",
                    "Program Files (x86)",
                    "Steam",
                    "steamapps",
                    "common",
                    "War Thunder",
                    "cache",
                    "*",
                )
            ],
            "minecraft": [
                os.path.join(
                    self.user_home, "AppData", "Roaming", ".minecraft", ".cache", "*"
                )
            ],
            "balenaetcher": [
                os.path.join(
                    self.user_home, "AppData", "Roaming", "balenaEtcher", "Cache", "*"
                )
            ],
            "vscode": [
                os.path.join(self.user_home, "AppData", "Roaming", "Code", "Cache", "*")
            ],
            "itunes": [
                os.path.join(
                    self.user_home,
                    "AppData",
                    "Local",
                    "Apple",
                    "Apple Software Update",
                    "DistCache",
                    "*",
                )
            ],
        }
        if self.os_impl:
            self.apps.update(self.os_impl.APPS)  # merge Linux apps into the same dict

    def get_size(self, path):
        total_size = 0
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except OSError:
                        pass
        return total_size

    def add_cache_paths(self, app_name):
        if app_name in self.apps:
            self.deferred_paths.extend(self.apps[app_name])
            print(
                f"{Fore.YELLOW}Added cache paths for {app_name} to the cleanup list.{Fore.RESET}"
            )
        else:
            print(f"{Fore.RED}App '{app_name}' is not supported.{Fore.RESET}")

    def delete_deferred_paths(self):
        total_reclaimed = 0

        for path_pattern in self.deferred_paths:
            for path in expand_paths(path_pattern):
                size_before = self.get_size(path)

                # ===== LINUX HANDLER =====
                if self.os_impl and self.os_impl.clear_special(path):
                    print(
                        f"{Fore.GREEN}Successfully cleared {path} (Linux handler).{Fore.RESET}"
                    )
                    total_reclaimed += size_before
                    continue
                # =====================================

                # ===== WINDOWS LOGIC =====
                if path == "pip_cache":
                    try:
                        subprocess.run(
                            ["pip", "cache", "purge"], shell=True, check=True
                        )
                        print(
                            f"{Fore.GREEN}Successfully cleared Pip cache.{Fore.RESET}"
                        )
                    except subprocess.CalledProcessError:
                        print(f"{Fore.RED}Failed to clear Pip cache.{Fore.RESET}")

                elif path == "scoop_cache":
                    try:
                        subprocess.run(
                            ["scoop", "cleanup", "*"], shell=True, check=True
                        )
                        subprocess.run(
                            ["scoop", "cache", "rm", "*"], shell=True, check=True
                        )
                        print(
                            f"{Fore.GREEN}Successfully cleared Scoop cache.{Fore.RESET}"
                        )
                    except subprocess.CalledProcessError:
                        print(f"{Fore.RED}Failed to clear Scoop cache.{Fore.RESET}")

                else:
                    try:
                        subprocess.run(f'del /f /q "{path}"', shell=True, check=True)
                        print(f"{Fore.GREEN}Deleted files at {path}{Fore.RESET}")
                    except subprocess.CalledProcessError:
                        print(f"{Fore.RED}Failed to delete files at {path}{Fore.RESET}")
                # =====================================

                total_reclaimed += size_before

            if self.os_impl and self.os_impl.clear_special(path):
                print(
                    f"{Fore.GREEN}Successfully cleared {path} (Linux handler).{Fore.RESET}"
                )
                total_reclaimed += self.get_size(path)
                continue

        print(
            f"{Fore.GREEN}Total space reclaimed: {total_reclaimed / (1024 * 1024):.2f} MB{Fore.RESET}"
        )
        self.deferred_paths.clear()

    def run(self):
        while True:
            app_name = (
                input(
                    f"{Fore.CYAN}Enter an app to clear its cache ('done' to delete files, 'exit' to quit, 'help' for supported apps): {Fore.RESET}"
                )
                .strip()
                .lower()
            )
            if app_name == "exit":
                print(f"{Fore.YELLOW}Exiting program.{Fore.RESET}")
                break
            elif app_name == "help":
                print(
                    f"{Fore.BLUE}Supported apps: {', '.join(self.apps.keys())}{Style.RESET_ALL}"
                )
            elif app_name == "done":
                if platform.system().lower() == "windows":
                    self.deferred_paths.extend(
                        [
                            "C:\\Windows\\Temp\\*",
                            os.path.join(
                                self.user_home, "AppData", "Local", "CrashDumps", "*"
                            ),
                            os.path.join(
                                self.user_home, "AppData", "Local", "Temp", "*"
                            ),
                            os.path.join(self.user_home, ".cache", "*"),
                            "C:\\Windows\\Prefetch\\*",
                            "C:\\Windows\\SoftwareDistribution\\Download\\*",
                        ]
                    )

                else:
                    self.deferred_paths.extend(
                        ["/tmp/*", os.path.join(self.user_home, ".cache", "*")]
                    )
            else:
                self.add_cache_paths(app_name)
                
            self.delete_deferred_paths()
            break


if __name__ == "__main__":
    cleaner = CacheCleaner()
    cleaner.run()
