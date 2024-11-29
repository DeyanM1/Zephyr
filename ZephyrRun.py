import argparse
from main import *


parser = argparse.ArgumentParser(description="Zephyr executable file")

parser.add_argument("-f", "--file", type=str, help="your .zph file path (without extension)")
parser.add_argument("-ld", "--libraryDirectory", type=str, help="Enter if custom library folder (optional, default=lib)")
parser.add_argument("-mt", "--measureTime", action="store_true", help="Enter if it should measure execution time(optional, default=false)")


args = parser.parse_args()


if not args.file:
    raise BaseException("You must specify the file name!")

if args.measureTime:
    if MEASURE_TIME: st = time.time()    

    lexer(FILE_NAME)
    compile(FILE_NAME)
    
    if MEASURE_TIME: et = time.time(); elapsed_time = et - st; print(f"\n Elapsed time: {elapsed_time}s")

else:
    if args.libraryDirectory:
        if MEASURE_TIME: st = time.time()    

        lexer(FILE_NAME, args.libraryDirectory)
        compile(FILE_NAME, args.libraryDirectory)
        
        if MEASURE_TIME: et = time.time(); elapsed_time = et - st; print(f"\n Elapsed time: {elapsed_time}s")
    else:
        if MEASURE_TIME: st = time.time()    

        lexer(FILE_NAME)
        compile(FILE_NAME)
        
        if MEASURE_TIME: et = time.time(); elapsed_time = et - st; print(f"\n Elapsed time: {elapsed_time}s")
