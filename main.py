import os
import subprocess
import sys
from packages.colorama import init, Fore, Style

class CacheCleaner:
    def __init__(self):
        init(autoreset=True)  # Initialize colorama to work properly in Windows terminal
        self.user_home = os.path.expandvars("%USERPROFILE%")
        self.deferred_paths = []
        self.allowed_extensions = [".txt", ".log", ".zip", ".tar.gz"]  # Files with these extensions will be deleted
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

    def add_cache_paths(self, app_name):
        if app_name in self.apps:
            self.deferred_paths.extend(self.apps[app_name])
            print(f"{Fore.YELLOW}Added cache paths for {app_name} to the cleanup list.{Fore.RESET}")
        else:
            print(f"{Fore.RED}App '{app_name}' is not supported.{Fore.RESET}")

    def delete_deferred_paths(self):
        for path in self.deferred_paths:
            if path == "pip_cache":
                subprocess.run(["pip", "cache", "purge"], shell=True)
                print(f"{Fore.GREEN}Successfully cleared Pip cache.{Fore.RESET}")
            elif path == "scoop_cache":
                subprocess.run(["scoop", "cleanup", "*"], shell=True)
                subprocess.run(["scoop", "cache", "rm", "*"], shell=True)
                print(f"{Fore.GREEN}Successfully cleared scoop cache.{Fore.RESET}")
            else:
                subprocess.run(f'del /f /q "{path}"', shell=True)
                print(f"{Fore.GREEN}Deleted files at {path}{Fore.RESET}")
        self.deferred_paths.clear()

    def delete_log_and_txt_files(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                # Check if the file ends with one of the allowed extensions
                if not any(file.endswith(ext) for ext in self.allowed_extensions):
                    continue  # Skip files that don't have .txt or .log extensions
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    def run(self):
        while True:
            app_name = input(f"{Fore.CYAN}Enter an app to clear its cache ('done' to delete files, 'exit' to quit, 'help' for supported apps): {Fore.RESET}").strip().lower()
            
            if not app_name:
                print(f"{Fore.RED}Invalid input. Please enter an app name or a command.{Style.RESET_ALL}")
                continue

            if app_name == "exit":
                print(f"{Fore.YELLOW}Exiting program.{Fore.RESET}")
                break

            if app_name == "help":
                print(f"{Fore.BLUE}Supported apps: {', '.join(self.apps.keys())}{Style.RESET_ALL}")
                continue

            if app_name == "done":
                self.deferred_paths.extend([ 
                    "C:\\Windows\\Temp\\*", 
                    os.path.join(self.user_home, "AppData", "Local", "CrashDumps", "*"), 
                    os.path.join(self.user_home, "AppData", "Local", "Temp", "*"), 
                    os.path.join(self.user_home, ".cache", "*"), 
                    "C:\\Windows\\Prefetch\\*", 
                    "C:\\Windows\\SoftwareDistribution\\Download\\*"
                ])
                self.delete_deferred_paths()
                self.delete_log_and_txt_files("C:\\")
                continue

            self.add_cache_paths(app_name)

if __name__ == "__main__":
    cleaner = CacheCleaner()
    cleaner.run()
