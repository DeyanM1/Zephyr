# Zephyr Library Manager

import argparse
from pathlib import Path
from typing import Any
import requests
from colorama import Fore
import os
import platform
import subprocess

def install(args: Any, path: Path):  
    url = "https://raw.githubusercontent.com/DeyanM1/ZephyrLibraries/refs/heads/main/lib/"


    args.libraries.append("base.py")
    for library in args.libraries:
        if library != "base.py":
            print(f"{Fore.MAGENTA}[INSTALL] Installing {library}{Fore.RESET}")
        newPath = path / library

        response = requests.get(url + library)
        
        if response.status_code == 200:
            # Get the content of the file
            file_content = response.text
            with newPath.open("w") as w:
                w.writelines(file_content)

            if library != "base.py":
                print(f"{Fore.GREEN}[COMPLETE] Installed {library}{Fore.RESET}")
        else:
            print(f"{Fore.RED}[ERROR] Failed to install {library}. Status code: {response.status_code}{Fore.RESET}")

def remove(args: Any):
    globalPath = getZephyrPath()


    for library in args.libraries:
        fileToRemove = globalPath / library


        if fileToRemove.exists():
            fileToRemove.unlink()
            print(f"{Fore.GREEN}[COMPLETE] Removed {library}{Fore.RESET}")
        else:
            print(f"{Fore.RED}[ERROR] Failed to remove {library}. library not found{Fore.RESET}")



def setPath():
    # Detect OS
    system_os = platform.system()

    # Windows: check if global/user environment variable already exists
    if system_os == "Windows":
        import winreg

        def env_var_exists(name: str):
            try:
                # Check user environment variables
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key: # type: ignore
                    winreg.QueryValueEx(key, name) # type: ignore
                    return True
            except FileNotFoundError:
                return False

    else:
        # Linux/macOS: check if variable already set in shell config
        shell_config = Path.home() / ".bashrc"
        if os.environ.get("SHELL", "").endswith("zsh"):
            shell_config = Path.home() / ".zshrc"

        def env_var_exists(name: str):
            if not shell_config.exists():
                return False
            with shell_config.open("r") as f:
                for line in f:
                    if line.strip().startswith(f"export {name}="):
                        return True
            return False

    # Only set the variable if it does not exist globally
    if not env_var_exists("ZEPHYR_LIB_PATH"):

        # Determine Zephyr library path
        if system_os == "Windows":
            username = os.getlogin()
            zephyr_lib_path = Path(f"C:/Users/{username}/AppData/local/Zephyr/libraries")
        else:
            zephyr_lib_path = Path.home() / ".config" / "Zephyr" / "libraries"

        # Create the directory if missing
        if not zephyr_lib_path.exists():
            zephyr_lib_path.mkdir(parents=True, exist_ok=True)

        # Set environment variable globally
        if system_os == "Windows":
            subprocess.run(
                ["setx", "ZEPHYR_LIB_PATH", str(zephyr_lib_path)],
                shell=True,
                check=True
            )
            print(f"{Fore.GREEN}[COMPLETE] Zephyr Path set successfully {Fore.RESET}")
        else:
            line = f'export ZEPHYR_LIB_PATH="{zephyr_lib_path}"\n'
            with shell_config.open("a") as fa: # type: ignore
                fa.write(line)
            print(f"Added ZEPHYR_LIB_PATH to {shell_config}") # type: ignore

    else:
        pass

def getZephyrPath() -> Path:
    system_os = platform.system()

    # Windows: read from registry (user-level environment variable)
    if system_os == "Windows":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key: # type: ignore
                path_str, _ = winreg.QueryValueEx(key, "ZEPHYR_LIB_PATH") # type: ignore
        except FileNotFoundError:
            pass
            #raise RuntimeError("Global environment variable ZEPHYR_LIB_PATH not found.")
    else:
        # Linux/macOS: read from shell config (~/.bashrc or ~/.zshrc)
        shell_config = Path.home() / ".bashrc"
        if os.environ.get("SHELL", "").endswith("zsh"):
            shell_config = Path.home() / ".zshrc"

        if not shell_config.exists():
            raise RuntimeError(f"Shell config {shell_config} does not exist.")

        path_str = None
        with shell_config.open("r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("export ZEPHYR_LIB_PATH="):
                    path_str = line.split("=", 1)[1].strip().strip('"')
                    break

        if path_str is None:
            pass
            #raise RuntimeError("Global environment variable ZEPHYR_LIB_PATH not found in shell config.")

    return Path(path_str) # type: ignore


def start():
    parser = argparse.ArgumentParser(description="Install or remove libraries with optional parameters.")
    
    parser.add_argument('action', choices=['install', 'remove'], help="Specify whether to install or remove libraries.") 
    parser.add_argument('--path', type=str, default=None, help="Specify a custom path. Default is None.")
    parser.add_argument('--global', dest='global_flag', action='store_true', help="Include this flag if you want the operation to be global.")
    parser.add_argument('libraries', nargs='*', help="List of libraries to install or remove.")

    args = parser.parse_args()



    
    if args.path:
        path = Path(args.path)
        if not path.is_absolute():
            path = Path.cwd() / path

            path = path.resolve()

            if not path.exists():
                print(Fore.RED, "[ERROR] Path doesnt exist", Fore.RESET)
                return
    
    else:
        path = Path.cwd() / "lib"
            
    
    if args.global_flag:
        setPath()
        path = getZephyrPath()


    match args.action:
        case "install":   
            setPath()
            install(args, path)
        case "remove":
            setPath()
            remove(args)
        case _:
            pass





if __name__ == "__main__":
    start()