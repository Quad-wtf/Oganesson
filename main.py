import os
import subprocess
from packages.colorama import init, Fore, Style

class CacheCleaner:
    def __init__(self):
        init(autoreset=True)
        self.user_home = os.path.expandvars("%USERPROFILE%")
        self.deferred_paths = []
        self.allowed_extensions = [".log"]
        self.apps = {
            "pip": ["pip_cache"],
            "msys2": [os.path.join("C:", "msys64", "var", "cache", "pacman", "pkg", "*")],
            "capcut": [
                os.path.join(self.user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "log", "*"),
                os.path.join(self.user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "cache", "*"),
                os.path.join(self.user_home, "AppData", "Local", "CapCut", "User Data", "Cache", "*")
            ],
            "npm": [os.path.join(self.user_home, "AppData", "Local", "npm-cache", "*")],
            "scoop": ["scoop_cache"],
            "war thunder": [os.path.join("C:", "Program Files (x86)", "Steam", "steamapps", "common", "War Thunder", "cache", "*")],
            "minecraft": [os.path.join(self.user_home, "AppData", "Roaming", ".minecraft", ".cache", "*")],
            "balenaetcher": [os.path.join(self.user_home, "AppData", "Roaming", "balenaEtcher", "Cache", "*")],
            "vscode": [os.path.join(self.user_home, "AppData", "Roaming", "Code", "Cache", "*")],
            "itunes": [os.path.join(self.user_home, "AppData", "Local", "Apple", "Apple Software Update", "DistCache", "*")]
        }

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
            print(f"{Fore.YELLOW}Added cache paths for {app_name} to the cleanup list.{Fore.RESET}")
        else:
            print(f"{Fore.RED}App '{app_name}' is not supported.{Fore.RESET}")

    def delete_deferred_paths(self):
        total_reclaimed = 0
        for path in self.deferred_paths:
            size_before = self.get_size(path)
            if path == "pip_cache":
                try:
                    subprocess.run(["pip", "cache", "purge"], shell=True, check=True)
                    print(f"{Fore.GREEN}Successfully cleared Pip cache.{Fore.RESET}")
                except subprocess.CalledProcessError:
                    print(f"{Fore.RED}Failed to clear Pip cache.{Fore.RESET}")
            elif path == "scoop_cache":
                try:
                    subprocess.run(["scoop", "cleanup", "*"], shell=True, check=True)
                    subprocess.run(["scoop", "cache", "rm", "*"], shell=True, check=True)
                    print(f"{Fore.GREEN}Successfully cleared scoop cache.{Fore.RESET}")
                except subprocess.CalledProcessError:
                    print(f"{Fore.RED}Failed to clear Scoop cache.{Fore.RESET}")
            else:
                try:
                    subprocess.run(f'del /f /q "{path}"', shell=True, check=True)
                    print(f"{Fore.GREEN}Deleted files at {path}{Fore.RESET}")
                except subprocess.CalledProcessError:
                    print(f"{Fore.RED}Failed to delete files at {path}{Fore.RESET}")
            total_reclaimed += size_before
        
        print(f"{Fore.GREEN}Total space reclaimed: {total_reclaimed / (1024 * 1024):.2f} MB{Fore.RESET}")
        self.deferred_paths.clear()

    def delete_specific_log_files(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                filename, extension = os.path.splitext(file)
                if extension.lower() == ".log":
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"{Fore.GREEN}Deleted: {file_path}{Fore.RESET}")
                    except PermissionError:
                        print(f"{Fore.RED}Permission error, skipping: {file_path}{Fore.RESET}")
                    except Exception as e:
                        print(f"{Fore.RED}Error deleting {file_path}: {str(e)}{Fore.RESET}")

    def run(self):
        while True:
            app_name = input(f"{Fore.CYAN}Enter an app to clear its cache ('done' to delete files, 'exit' to quit, 'help' for supported apps): {Fore.RESET}").strip().lower()
            if app_name == "exit":
                print(f"{Fore.YELLOW}Exiting program.{Fore.RESET}")
                break
            elif app_name == "help":
                print(f"{Fore.BLUE}Supported apps: {', '.join(self.apps.keys())}{Style.RESET_ALL}")
            elif app_name == "done":
                self.deferred_paths.extend([
                    "C:\\Windows\\Temp\\*",
                    os.path.join(self.user_home, "AppData", "Local", "CrashDumps", "*"),
                    os.path.join(self.user_home, "AppData", "Local", "Temp", "*"),
                    os.path.join(self.user_home, ".cache", "*"),
                    "C:\\Windows\\Prefetch\\*",
                    "C:\\Windows\\SoftwareDistribution\\Download\\*"
                ])
                self.delete_deferred_paths()
                self.delete_specific_log_files("C:\\")
                break
            else:
                self.add_cache_paths(app_name)

if __name__ == "__main__":
    cleaner = CacheCleaner()
    cleaner.run()
