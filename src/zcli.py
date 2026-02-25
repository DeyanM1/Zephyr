import argparse
from pathlib import Path
from main import execute, lexer, compiler
from functions import ZFile, ZError, ZCommand, ZIndex, ZBase, typeRegistry, ActiveVars





def zcli():
    zfile = ZFile(Path(".temp.zph"))
    zfile.zphPath.open("w")

    cmd = ZCommand(-1, "", "", "", [""])
    activeVars: ActiveVars = {}
    activeVars.update({"__": typeRegistry["__"](ZCommand(0, "__", ZBase.define, "", [""]), activeVars, zfile)})
    index: ZIndex = 0
    
    while True:
        try:
            rawCMD = input(">-->> ")


            if rawCMD.lower() == "exit":
                try:
                    zfile.zphPath.unlink()
                    zfile.zsrcPath.unlink()
                except FileNotFoundError:
                    pass
                print("Exiting...")
                quit()
            
            with zfile.zphPath.open(mode="a", encoding="utf-8") as f:
                rawCMD += "\n"
                f.write(rawCMD)


            ZCommandData = lexer(zfile)
            cmd: ZCommand = ZCommandData[-1]
            activeVars, index = execute(cmd, activeVars, index)
                    
            
        except ZError as e:
            e.process(cmd, zfile)
        
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            quit()




def start():
    parser = argparse.ArgumentParser(description="Run .zph files")
    parser.add_argument("filepath", default="", nargs="?", type=str, help="Path to the file")
    args = parser.parse_args()

    file_path = Path(args.filepath)

    if args.filepath:
        # Validate file
        if not file_path.exists() or not file_path.is_file() or file_path.suffix != ".zph":
            print(f"Error: {file_path} does not exist or is not a zph file")
            return
        
        zfile = ZFile(file_path)


        ### RUN ###

        lexer(zfile)
        compiler(zfile)

    else:
        zcli()


if __name__ == "__main__":
    start()