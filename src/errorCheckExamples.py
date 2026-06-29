from main import compiler, lexer
from functions import ZFile
from pathlib import Path



def checkProjects():
    base_path = Path("/home/deyan/dev/Zephyr/examples/Projects/")
    for folder in base_path.iterdir():
        if folder.is_dir() and not folder.name.startswith("."):
            code_file = folder / "code.zph"
            if code_file.exists():
                print(folder)
                ZFILE = ZFile(code_file)

                lexer(ZFILE)
                compiler(ZFILE)
                print("-----------")

def checkExamples():
    base_path = Path("/home/deyan/dev/Zephyr/examples/Examples/")
    for file in base_path.glob("*.zph"):
        if not file.name.startswith("."):
            print(file.name)
            ZFILE = ZFile(file)

            lexer(ZFILE)
            compiler(ZFILE)
            print("-----------")


if __name__ == "__main__":
    checkExamples()