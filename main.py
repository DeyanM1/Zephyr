from functions import *
import sys
import time
import json

MEASURE_TIME = False
EXE_VERSION = True

LIB_FOLDER_NAME = "lib"
FILE_LIBRARY = "." # folder in current directory
FILE_NAME = "code"



def lexer(filename: str, fileLibrary: str = "."):
    currentCommand = ""
    
    code = []
    
    bannedChars = ["\n", "\r", "\t"]
    with open(f"{fileLibrary}/{filename}.zph", 'r') as file:
        for line in file:
            line = line.lstrip()    # remove spaces from start
            for char in line:
                if char == "~":
                    continue
                if char != ";":
                    if char in bannedChars:
                        continue
                    currentCommand += char
                
                if char == ";":
                    code.append(currentCommand)
                    currentCommand = ""
    
    #print(code) 
    
    data = {}
    
    for elem in range(len(code)):
        try:
            command, params = code[elem].split(":")
            name, base, function = command.split(" ")
            
            paramsList = params.split("|")
        except ValueError:
            print(f"[{elem +1}]  code structure is invalid")
            quit()

        data.update({f"{elem}::{code[elem]}": {"name": name,"base": base, "function": function, "paramsList": paramsList}})

        
    with open(f"{fileLibrary}/{filename}.zsrc", "w") as file:
        json.dump(data, file, indent=4) 
    
    return data


def compile(filename: str, fileLibrary: str = "."): 
    with open(f"{fileLibrary}/{filename}.zsrc", "r") as file:

        code = json.load(file)
        
        
    vars = {}
    libs = {}
    index = 0
    
    
    while index <= len(code)-1:
        currentCmdName = code.get(list(code)[index])
        
        name = currentCmdName.get('name')
        base = currentCmdName.get('base')
        function = currentCmdName.get('function')
        paramsList = currentCmdName.get('paramsList')
    
        

        
        if name == "__":
            match base:
                case "?":
                    match function:
                        case "JUMP":
                            index = int(paramsList[0]) -1
                            continue
                        
                        case "predefVars":
                            var = PredefVar(name, paramsList[0], vars)
                            vars = var.read()
                        
                        case "dumpVars":
                            var = PredefVar(name, paramsList[0], vars)
                            var.dump()


        elif function in TYPES:
            match function:
                case "MO":
                    var = MathObject(name)
                    vars.update({var.name: var})
                    
                    if len(paramsList) == 1:
                        if paramsList[0].startswith("("):
                            vars[name].setEquation(paramsList[0])
                            vars[name].prepare(vars)
                    
                
                case "LOOP":
                    var = Loop(name=name, startIndex=index, vars=vars, conditionObject=paramsList[0])
                        
                    vars.update({var.name: var})
                
                case "FUNC":
                    if len(paramsList) == 2:
                        if paramsList[1] == "~1":
                            var = Function(name, paramsList[0], True)
                        else:
                            var = Function(name, paramsList[0], False)
                    else:
                        var = Function(name, False)

                    vars.update({var.name: var})
                
                case "CO":
                    var = ConditionObject(name)
                    var.setCondition(paramsList[0])
                    var.prepare(vars)
                    vars.update({var.name: var})
                
                case "LIB":
                    libPath = f"{fileLibrary}.{LIB_FOLDER_NAME}"
                    var = Library(name, libPath, paramsList[0])
                    vars.update({var.name: var})
                
                case  "RNG":
                    var = RNG(name, paramsList[0], paramsList[1])
                    vars.update({var.name:var})
                
                    
                
                case _:

                    if 0 <= 1 < len(paramsList):
                        if paramsList[1] == "~1":
                            var = Variable(name, function, paramsList[0], vars, True)
                        else:
                            var = Variable(name, function, paramsList[0], vars, False)
                    else:
                        var = Variable(name, function, paramsList[0], vars, False)

                        vars.update({var.name: var})


        elif vars[name].type == Token.PT:
            match base:
                case "?":
                    match function:
                        case "push": 
                            vars[name].push()
                        case "w":
                            vars[name].changeValue(paramsList[0], vars)
                            
                        case "INPUT":
                            vars[name].setValueByInput(paramsList[0])
                        
                        case _:
                            Error(501, ["Token.PT", f"? {function}"]).as_string()
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", f"# {function}"]).as_string()

        elif vars[name].type == Token.INT:
            match base:
                case "?":
                    match function:
                        case "w":
                            vars[name].changeValue(paramsList[0], vars)

                        case _:
                            Error(501, ["Token.INT", f"? {function}"]).as_string()
                            
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.INT", f"# {function}"]).as_string()
                            
        elif vars[name].type == Token.FLOAT:
            match base:
                case "?":
                    match function:
                        case "w":
                            vars[name].changeValue(paramsList[0], vars)

                        case _:
                            Error(501, ["Token.FLOAT", f"? {function}"]).as_string()
                            
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.FLOAT", f"# {function}"]).as_string()
        
        elif vars[name].type == Token.RNG:
            match base:
                case "?":
                    match function:
                        case "CR":
                            vars[name].setRange(paramsList[0])

                        case _:
                            Error(501, ["Token.RNG", f"? {function}"]).as_string()
                            
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.RNG", f"# {function}"]).as_string()
                        
        elif vars[name].type == Token.MO:
            match base:
                case "?":
                    match function:
                        case "w":
                            vars[name].setEquation(paramsList[0])
                        
                        case function if function.startswith("("):
                            vars[name].setEquation(function)
                            vars[name].prepare(vars)

                        case _:
                            Error(501, ["Token.MO", f"? {function}"]).as_string()
                            
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", f"# {function}"]).as_string()
        
        elif vars[name].type == Token.FUNC:
            match base:
                case "?":
                    match function:                        
                        case function if function.startswith("("):
                            if vars[name].type == Token.FUNC:
                                vars[name].setFunction(function, vars)
                        
                        case "call":
                            vars[name].call(vars)
                            
                        case _:
                            Error(501, ["Token.MO", f"? {function}"]).as_string()
                            
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", f"# {function}"]).as_string()
        
        elif vars[name].type == Token.LOOP:
            match base:
                case "?":
                    match function:
                        case "END":
                            index = vars[name].loopEnd(index, vars)
                        case _:
                            Error(501, ["Token.LOOP", f"? {function}"]).as_string()          
                case "#":
                    match function:
                        case _:
                            Error(501, ["Token.LOOP", f"# {function}"]).as_string()
    
        elif vars[name].type == Token.CO:
            match base:
                case "?":
                    match function:
                        case function if function.startswith("("):
                            if vars[name].type == Token.CO:
                                vars[name].setCondition(function)
                            
                        case _:
                            Error(501, ["Token.CO", f"? {function}"]).as_string()
                
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", f"# {function}"]).as_string()
    
        elif vars[name].type == Token.Lib:
            vars = vars[name].libObject.search(name=name, base=base, function=function, paramsList=paramsList, vars=vars)
            print(vars["a"].name, vars["a"].value)
        else:
            pass
    
        index += 1
    print("\n", vars)
        
    

 

if __name__ == "__main__":
    if EXE_VERSION:
        args = sys.argv[1:]
        options = {}
        
        for i in range(len(args)):
            key = args[i][2:]

            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                options[key] = args[i + 1]  # The value is the next argument
            
            else:
                options[key] = True  # If no value, assume it's a flag
        
        try:
            FILE_NAME = options["fileName"]
        except KeyError:
            print("Please provide a filename \nUsage: main.exe <filename>\n")
            sys.exit()
        try:
            MEASURE_TIME = options.get("measureTime")
        except KeyError:
            pass
            

    if MEASURE_TIME: st = time.time()    

    lexer(FILE_NAME, FILE_LIBRARY)
    compile(FILE_NAME, FILE_LIBRARY)
    
    if MEASURE_TIME: et = time.time(); elapsed_time = et - st; print(f"\n Elapsed time: {elapsed_time}s")
