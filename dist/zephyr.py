import argparse
import time
import main
import functions 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific functions with arguments")

    subparsers = parser.add_subparsers(dest="function", required=True, help="Choose a function to run")

 
    compileParser = subparsers.add_parser("compile", help="compile a file")
    compileParser.add_argument("file", type=str, help="File name to Pars")
    compileParser.add_argument("-d", "--dir", type=str, default=".", help="Custom fileDirectory; default: currentDir (Optional)")
    compileParser.add_argument("-l", "--lib", type=str, default="lib", help="Custom libraryDirectory; default: lib (Optional)")
    compileParser.add_argument("-r", "--run", action="store_true", help="combined run command")
    compileParser.add_argument("-t", "--time", action="store_true", help="Boolean flag for measureing Time")
    
    runParser = subparsers.add_parser("run", help="Run a compiled file (.zscr)")
    runParser.add_argument("file", type=str, help="File name to run")
    runParser.add_argument("-d", "--dir", type=str, default=".", help="Custom fileDirectory; default: currentDir (Optional)")
    runParser.add_argument("-l", "--lib", type=str, default="lib", help="Custom libraryDirectory; default: lib (Optional)")
    runParser.add_argument("-t", "--time", action="store_true", help="Boolean flag for measureing Time")


    updateParser = subparsers.add_parser("update", help="Opens the installer file")

    args = parser.parse_args()

    
    
    if args.function == "compile":
        if args.time: t1 = time.time()
        
        main.lexer(args.file, args.dir)
        if args.run:
            main.compiler(args.file, args.dir)
        
        if args.time: t2 = time.time(); print(f"Time: {t2 - t1} seconds")
        
    elif args.function == "run":
        if args.time: t1 = time.time()
        
        main.compiler(args.file, args.dir)
        
        if args.time: t2 = time.time(); print(f"Time: {t2 - t1} seconds")
