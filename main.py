import subprocess
import os
from packages.colorama import Fore, Style
from operating.linux.ubuntu import Ubuntu
from operating.linux.arch import Arch

apps = [
    "Pip",
    "MSYS2",
    "Capcut",
    "npm",
    "scoop",
    "War Thunder (only if installed on Steam)" 
]

def clear_cache(app_name, user_home):
    """ Deletes cache files for the specified application. """
    
    if app_name == "capcut":
        paths = [
            os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "log", "*"),
            os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "cache", "*"),
            os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Cache", "*")
        ]
    elif app_name == "pip":
        result = subprocess.run(["pip", "cache", "purge"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(Fore.RED + f"Error deleting Pip cache: {result.stderr}" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Successfully cleared Pip cache." + Style.RESET_ALL)
        return  # Prevents running the `for` loop
    elif app_name == "msys2":
        paths = [os.path.join("C:", "msys64", "var", "cache", "pacman", "pkg", "*")]
    elif app_name == "npm":
        paths = [os.path.join(user_home, "AppData", "Local", "npm-cache", "*")]
    elif app_name == "scoop":
        result1 = subprocess.run(["scoop", "cleanup", "*"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result2 = subprocess.run(["scoop", "cache", "rm", "*"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elif app_name == "war thunder":
        paths = [os.path.join("C:", "Program Files (x86)", "Steam", "steamapps", "common", "War Thunder", "cache", "*")]
        
        if result1.returncode != 0 or result2.returncode != 0:
            print(Fore.RED + f"Error clearing Scoop cache: {result1.stderr} {result2.stderr}" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Successfully cleared Scoop cache." + Style.RESET_ALL)
        return
    else:
        print(Fore.YELLOW + f"App '{app_name}' is not supported." + Style.RESET_ALL)
        return

    # Process file deletion for paths
    for path in paths:
        command = f'del /f /q "{path}"'  # Wrap in quotes to handle spaces
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(Fore.RED + f"Error deleting files at {path}: {result.stderr}" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Successfully deleted files at {path}" + Style.RESET_ALL)

def main():
    user_home = os.path.expandvars("%USERPROFILE%")  # Gets C:\Users\CurrentUser
    
    while True:
        app_name = input(Fore.CYAN + "Enter an app to clear its cache ('done' to delete files, 'exit' to quit, 'help' for supported apps): " + Style.RESET_ALL).strip().lower()

        if not app_name:
            print(Fore.RED + "Invalid input. Please enter an app name or a command." + Style.RESET_ALL)
            continue

        if app_name == "exit":
            print(Fore.YELLOW + "Exiting program." + Style.RESET_ALL)
            break

        if app_name == "help":
            print(Fore.BLUE + "Supported apps: " + ", ".join(apps) + Style.RESET_ALL)
            continue

        if app_name == "done":
            temp_paths = [
                "C:\\Windows\\Temp\\*",
                os.path.join(user_home, "AppData", "Local", "CrashDumps", "*"),
                os.path.join(user_home, "AppData", "Local", "Temp", "*"),
                os.path.join(user_home, ".cache", "*"),
                "C:\\Windows\\Prefetch\\*",
                "C:\\Windows\\SoftwareDistribution\\Download\\*"
            ]
            
            for temp_path in temp_paths:
                os.system(f'del /f /q "{temp_path}"')
            
            print(Fore.GREEN + "Temp files cleared." + Style.RESET_ALL)
            exit(0)

        clear_cache(app_name, user_home)

if __name__ == "__main__":
    main()
