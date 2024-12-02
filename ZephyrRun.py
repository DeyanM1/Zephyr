import argparse
from main import *




def compileFunc(fileName: str, fileDirectory: str, libDirectory: str, measureTime: bool, flagRun: bool):
    print(f"Compiling: {fileName}")
    lexedData = lexer(fileName, fileDirectory)
    
    if flagRun:
        runFunc(fileName, fileDirectory, libDirectory, measureTime)
    
def runFunc(fileName, fileDirectory, libDirectory, measureTime: bool):
    compile(fileName, libDirectory, fileDirectory, measureTime)






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific functions with arguments")

    subparsers = parser.add_subparsers(dest="function", required=True, help="Choose a function to run")

 
    compileParser = subparsers.add_parser("compile", help="compile a file")
    compileParser.add_argument("file", type=str, help="File name to Pars")
    compileParser.add_argument("-d", "--dir", type=str, default=".", help="Custom fileDirectory; default: currentDir (Optional)")
    compileParser.add_argument("-l", "--lib", type=str, default="lib", help="Custom libraryDirectory; default: lib (Optional)")
    compileParser.add_argument("-r", "--run", action="store_true", help="combined run command")
    compileParser.add_argument("-t", "--time", action="store_true", help="Boolean flag for exampleFunction")
    
    runParser = subparsers.add_parser("run", help="Run a compiled file (.zscr)")
    runParser.add_argument("file", type=str, help="File name to run")
    runParser.add_argument("-d", "--dir", type=str, default=".", help="Custom fileDirectory; default: currentDir (Optional)")
    runParser.add_argument("-l", "--lib", type=str, default="lib", help="Custom libraryDirectory; default: lib (Optional)")
    runParser.add_argument("-t", "--time", action="store_true", help="Boolean flag for exampleFunction")


    args = parser.parse_args()

    
    
    if args.function == "compile":
        compileFunc(args.file, args.dir, args.lib, args.time, args.run)
        
    if args.function == "run":
        runFunc(args.file, args.dir, args.lib, args.time)