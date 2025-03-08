from functions import *
import sys
import time
import json

MEASURE_TIME = False


LIB_DIRECTORY = "lib"
FILE_DIRECTORY = "./" # folder in current directory
FILE_NAME = "code.zph"



def lexer(filename: str, fileDirectory: str = "."):
    currentCommand = ""
    
    code = []
    
    if filename.endswith(".zph"):
        filename = filename[: -len(".zph")] 

    elif filename.endswith(".zsrc") or filename.endswith(".zpkg"):
        raise BaseException("File must be a .zph file, not a .zscr file")
    
    
    bannedChars = ["\n", "\r", "\t"]
    with open(f"{fileDirectory}/{filename}.zph", 'r') as file:
        for line in file:
            line = line.lstrip()    # remove spaces from start
            if line.startswith("~"):
                continue
            for char in line:
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

        
    with open(f"{fileDirectory}/{filename}.zsrc", "w") as file:
        json.dump(data, file, indent=4) 
    
    return data


def compile(filename: str, libDirectory: str, fileDirectory: str = ".", measureTime:bool = False): 

    if measureTime: st = time.time() 
    
    if filename.endswith(".zsrc"):
        filename = filename[: -len(".zsrc")] 
    elif filename.endswith(".zph"):
        filename = filename[: -len(".zph")] 
        #print(f"[WARNING] Compiling file: {filename}.zsrc")
    
    
    
    with open(f"{fileDirectory}/{filename}.zsrc", "r") as file:
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
                case "LIST":
                    
                    if len(paramsList) > 1:
                        var = List(name, paramsList[0], paramsList[1])
                    else:
                        var = List(name, paramsList[0])
                    vars.update({var.name: var})
                
                case "ALIST":
                    pass
                
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
                
                case "IF":
                    var = IF(name, index, paramsList[1], paramsList[0])
                    vars.update({var.name: var})
                    index = var.checkCondition(vars)
                
                case "LIB":
                    libPath = f"{fileDirectory}.{libDirectory}"
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
                            vars[name].setValueByInput(paramsList[0], vars)
                        
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
                            
                        case "INPUT":
                            vars[name].setValueByInput(paramsList[0], vars)

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
        
        elif vars[name].type == Token.LIST:
            match base:
                case "?":
                    match function:
                        case "SET": 
                            vars[name].set(paramsList[0], paramsList[1], vars)
                case "#":
                    match function:
                        case _:
                            Error(501, ["Token.LIST", f"# {function}"]).as_string()
  
        elif vars[name].type == Token.ALIST:
            pass
        
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
                        
                        case function if function.startswith(""):
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
                            Error(501, ["Token.FUNC", f"? {function}"]).as_string()
                            
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.FUNC", f"# {function}"]).as_string()
        
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
                            Error(501, ["Token.CO", f"# {function}"]).as_string()
    
        elif vars[name].type == Token.IF:
            match base:
                case "?":
                    match function:
                        case "ELSE":
                            vars[name].commandsInELSE = paramsList[0]
                            if vars[name].value == False: 
                                pass
                            elif vars[name].value == True:
                                index = index + int(vars[name].commandsInELSE)
                                
                        case "END":
                            pass
                            
                        case _:
                            Error(501, ["Token.IF", f"? {function}"]).as_string()
                
                case "#":
                    match function:
                        case _:
                            Error(501, ["Token.IF", f"# {function}"]).as_string()
                            
    
        elif vars[name].type == Token.Lib:
            vars = vars[name].libObject.search(name=name, base=base, function=function, paramsList=paramsList, vars=vars)
            print(vars["a"].name, vars["a"].value)
        else:
            pass
    
        index += 1
    #print("\n", vars)

    
    if measureTime: et = time.time(); elapsed_time = et - st; print(f"\n Elapsed time: {elapsed_time}s")
        
    

 

if __name__ == "__main__":
    if len(sys.argv) > 1:
        FILE_NAME = sys.argv[1]
    if len(sys.argv) > 2:
        FILE_DIRECTORY = sys.argv[2]
    lexer(filename=FILE_NAME, fileDirectory=FILE_DIRECTORY)
    compile(filename=FILE_NAME, libDirectory=LIB_DIRECTORY, fileDirectory=FILE_DIRECTORY, measureTime=MEASURE_TIME)