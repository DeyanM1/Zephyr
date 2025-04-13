import argparse
import requests
import os



def installLibrary(args):
    """
    Function to install a library from a given URL
    :param args: Arguments containing the library name
    """
    zephyrEnvPath = os.getenv("ZEPHYR_PATH")
    if zephyrEnvPath is None:
        print("ZEPHYR_PATH environment variable not set.")
        return

    url = f"https://raw.githubusercontent.com/DeyanM1/ZephyrPackages/refs/heads/main/{args.libraryName}.py"
    path = os.path.join(zephyrEnvPath, "lib", args.libraryName + ".py")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Write the content to a local file
        with open(path, "wb") as file:
            file.write(response.content)

        print(f"File downloaded successfully and saved as '{path}'")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def uninstallLibrary(args):
    """
    Function to uninstall a library by removing its file
    :param args: Arguments containing the library name
    """
    zephyrEnvPath = os.getenv("ZEPHYR_PATH")
    if zephyrEnvPath is None:
        print("ZEPHYR_PATH environment variable not set.")
        return

    path = os.path.join(zephyrEnvPath, "lib", args.libraryName + ".py")
    if not os.path.exists(path):
        print(f"The library '{args.libraryName}' does not exist at '{path}'.")
        return

    confirmation = input(f"Are you sure you want to uninstall '{args.libraryName}'? This action cannot be undone. (yes/no): ").strip().lower()
    if confirmation == "yes":
        try:
            os.remove(path)
            print(f"The library '{args.libraryName}' has been successfully uninstalled.")
        except OSError as e:
            print(f"An error occurred while trying to uninstall the library: {e}")
    else:
        print("Uninstallation canceled.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific functions with arguments")

    subparsers = parser.add_subparsers(dest="function", required=True, help="Choose a function to run")


    installParser = subparsers.add_parser("install", help="Install a library from my github")
    installParser.add_argument("libraryName", type=str, help="name of the library to install")

    uninstallParser = subparsers.add_parser("uninstall", help="Unistall a library from my github")
    uninstallParser.add_argument("libraryName", type=str, help="name of the library to uninstall")

    args = parser.parse_args()


    if args.function == "install":
        installLibrary(args)
    elif args.function == "uninstall":
        uninstallLibrary(args)
