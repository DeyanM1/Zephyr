from pathlib import Path
import subprocess
import re


def checkProjects():
    base_path = Path("/home/deyan/dev/Zephyr/examples/Projects/")
    folders = [f for f in base_path.iterdir() if f.is_dir() and not f.name.startswith(".")]
    folders.sort(key=lambda f: f.name)

    for folder in folders:
        file = folder / "code.zph"
        if file.exists():
            print(f"---------- {folder} ----------")
            subprocess.run(["uv", "run", "./src/zcli.py", file])


def checkExamples():
    base_path = Path("/home/deyan/dev/Zephyr/examples/Examples/")
    files = [f for f in base_path.glob("*.zph") if not f.name.startswith(".")]
    files.sort(key=lambda f: int(re.search(r"\d+", f.stem).group()))  # pyright: ignore[reportOptionalMemberAccess]

    for file in files:
        print(f"---------- {file.name} ----------")
        subprocess.run(["uv", "run", "./src/zcli.py", file])



if __name__ == "__main__":
    print("#################################")
    print("########### Examples ############")
    print("#################################\n")
    checkExamples()
    
    print("\n#################################")
    print("########### Projects ############")
    print("#################################\n")
    checkProjects()