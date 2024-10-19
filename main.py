from functions import *
import sys
import time
import json

MEASURE_TIME = True
FILE_NAME = "code"



def lexer(filename: str):
    currentCommand = ""
    
    code = []
    
    bannedChars = ["\n", "\r", "\t"]
    with open(f"{filename}.lys", 'r') as file:
        for line in file:
            line = line.lstrip()    # remove spaces from start
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
            print(f"[{elem}]  missing semicolon")
            quit()

        data.update({f"{elem}::{code[elem]}": {"name": name,"base": base, "function": function, "paramsList": paramsList}})

        
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file, indent=4) 
    
    return data


def compile(filename: str): 
    with open(f"{filename}.json", "r") as file:

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
                
                case "LOOP":
                    var = Loop(name=name, startIndex=index, vars=vars, conditionObject=paramsList[0])
                        
                    vars.update({var.name: var})
                
                case "FUNC":
                    if len(paramsList) == 0:
                        if paramsList[1] == "~1":
                            var = Function(name, paramsList[0], True)
                        else:
                            var = Function(name, paramsList[0], False)
                    else:
                        var = Function(name, paramsList[0])

                    vars.update({var.name: var})
                
                case "CO":
                    var = ConditionObject(name, paramsList[0])
                    var.prepare(vars)
                    vars.update({var.name: var})
                
                case "LIB":
                    var = Library(name, paramsList[0])
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
                            
                        case _:
                            Error(501, ["Token.CO", f"? {function}"]).as_string()
                
                case "#":
                    match function:
                        case "CT":
                            vars = changeType(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", f"# {function}"]).as_string()
    
        elif vars[name].type == Token.Lib:
            vars = vars[name].libObject.search(name, base, function, paramsList, vars)
    
        else:
            pass
    
        index += 1
    print("\n", vars)
        
    

 

if __name__ == "__main__":
    if MEASURE_TIME: st = time.time()
    
    if len(sys.argv) > 1: lexer(sys.argv[1])
    else: lexer(FILE_NAME)
    
    compile(FILE_NAME)
    
    if MEASURE_TIME: et = time.time(); elapsed_time = et - st; print(f"\n Elapsed time: {elapsed_time}s")
