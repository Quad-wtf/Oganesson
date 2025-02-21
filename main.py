import subprocess
import os
from operating.linux.ubuntu import Ubuntu
from operating.linux.arch import Arch

apps = [
    "Pip",
    "Chrome",
    "Opera",
    "Opera GX",
    "MSYS2",
    "Capcut",
    "npm",
    "scoop"
]

def main():
    user_home = os.path.expandvars("%USERPROFILE%")  # Gets C:\Users\CurrentUser

    app_name = input("What app do you use that you want the cache deleted? (type 'done' to delete the files, 'exit' to exit, 'help' for list of programs we support) ").strip().lower()

    if app_name == "done":

        os.system("del /s /q C:\\Windows\\Temp\\*")
        os.system("del /s /q %temp%\\*")
        os.system("del /s /q C:\\Windows\\Prefetch\\*")
        os.system("del /s /q C:\\Windows\\SoftwareDistribution\\Download\\*")

        if app_name == "capcut":

            paths1 = [
                os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "log", "*"),
                os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Log", "alog", "cache", "*"),
                os.path.join(user_home, "AppData", "Local", "CapCut", "User Data", "Cache", "*")
            ]

            for path in paths1:
                command = f'del /f /q "{path}"'  # Wrap in quotes to handle spaces
                result1 = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if result1.returncode != 0:
                    print(f"Error deleting files at {path}: {result1.stderr}")
                else:
                    print(f"Successfully deleted files at {path}")
        elif app_name == "pip":
            result_2 = subprocess.run(["pip", "cache", "purge"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  text=True)

            if result_2.returncode != 0:
                print(f"Error deleting files! {result_2.stderr}")
        elif app_name == "chrome":
            result_3 = subprocess.run(["del", "/f", "/q", "C:\Users\marci\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result_3.returncode != 0:
                print(f"Error deleting files! {result_3.stderr}")

if __name__ == "__main__":
    main()
