import subprocess
import os
from packages.colorama import Fore, Style

apps = [
    "Pip",
    "MSYS2",
    "Capcut",
    "npm",
    "scoop",
    "War Thunder (only if installed on Steam)",
    "Minecraft",
    "iTunes",
    "BakkesMod",
    "BalenaEtcher",
    "VSCode"
]

deferred_paths = []

def clear_cache(app_name, user_home):
    """ Adds cache file paths for the specified application to deferred_paths. """
    global deferred_paths
    
    if app_name == "capcut":
        deferred_paths.extend([
            os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "log", "*"),
            os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "cache", "*"),
            os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Cache", "*")
        ])
    elif app_name == "pip":
        deferred_paths.append("pip_cache")
    elif app_name == "msys2":
        deferred_paths.append(os.path.join("C:", "msys64", "var", "cache", "pacman", "pkg", "*"))
    elif app_name == "npm":
        deferred_paths.append(os.path.join(user_home, "AppData", "Local", "npm-cache", "*"))
    elif app_name == "scoop":
        deferred_paths.append("scoop_cache")
    elif app_name == "war thunder":
        deferred_paths.append(os.path.join("C:", "Program Files (x86)", "Steam", "steamapps", "common", "War Thunder", "cache", "*"))
    elif app_name == "minecraft":
        deferred_paths.append(os.path.join(user_home, "AppData", "Roaming", ".minecraft", ".cache", "*"))
    elif app_name == "balenaetcher":
        deferred_paths.append(os.path.join(user_home, "AppData", "Roaming", "balenaEtcher", "Cache", "*"))
    elif app_name == "vscode":
        deferred_paths.append(os.path.join(user_home, "AppData", "Roaming", "Code", "Cache", "*"))
    elif app_name == "itunes":
        deferred_paths.append(os.path.join(user_home, "AppData", "Local", "Apple", "Apple Software Update", "DistCache", "*"))
    else:
        print(f"{Fore.RED}App '{app_name}' is not supported.{Fore.RESET}")
        return
    
    print(f"{Fore.YELLOW}Added cache paths for {app_name} to the cleanup list.{Fore.RESET}")

def delete_deferred_paths():
    """ Deletes all paths stored in deferred_paths. """
    global deferred_paths
    
    for path in deferred_paths:
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
    
    deferred_paths.clear()

def main():
    user_home = os.path.expandvars("%USERPROFILE%")
    
    while True:
        app_name = input(f"{Fore.CYAN}Enter an app to clear its cache ('done' to delete files, 'exit' to quit, 'help' for supported apps): {Fore.RESET}").strip().lower()

        if not app_name:
            print(f"{Fore.RED}Invalid input. Please enter an app name or a command.{Style.RESET_ALL}")
            continue

        if app_name == "exit":
            print(f"{Fore.YELLOW}Exiting program.{Fore.RESET}")
            break

        if app_name == "help":
            print(f"{Fore.BLUE}Supported apps: {', '.join(apps)}{Style.RESET_ALL}")
            continue

        if app_name == "done":
            deferred_paths.extend([
                "C:\\Windows\\Temp\\*",
                os.path.join(user_home, "AppData", "Local", "CrashDumps", "*"),
                os.path.join(user_home, "AppData", "Local", "Temp", "*"),
                os.path.join(user_home, ".cache", "*"),
                "C:\\Windows\\Prefetch\\*",
                "C:\\Windows\\SoftwareDistribution\\Download\\*"
            ])
            delete_deferred_paths()
            continue

        clear_cache(app_name, user_home)

if __name__ == "__main__":
    main()
