# Zephyr Library Manager

import argparse
from pathlib import Path
from typing import Any
import requests


def install(args: Any, path: Path):
    
    url = "https://raw.githubusercontent.com/DeyanM1/ZephyrPackages/refs/heads/main/"

    for library in args.libraries:
        response = requests.get(url + library)
        
        if response.status_code == 200:
            # Get the content of the file
            file_content = response.text
            with path.open("w") as w:
                w.writelines(file_content)
        else:
            print(f"Failed to retrieve the file. Status code: {response.status_code}")

def remove(args: Any):
    pass




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
                print("ERROR! Path doesnt exist")
                return
    
    else:
        path = Path.cwd() / "lib"
            
    
    if args.global_flag:
        pass


    match args.action:
        case "install":
            install(args, path)
        case "uninstall":
            remove(args)
        case _:
            pass





if __name__ == "__main__":
    start()