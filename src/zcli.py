import argparse
from pathlib import Path
import main
from functions import ZFile



def start():
    parser = argparse.ArgumentParser(description="Run .zph files")
    parser.add_argument("filepath", type=str, help="Path to the file")
    args = parser.parse_args()

    file_path = Path(args.filepath)
    
    # Validate file
    if not file_path.exists() or not file_path.is_file() or file_path.suffix != ".zph":
        print(f"Error: {file_path} does not exist or is not a zph file")
        return
    
    zfile = ZFile(file_path)


    ### RUN ###

    main.lexer(zfile)
    main.compile(zfile)


if __name__ == "__main__":
    start()