#TODO: Libraries


import json
from functions import *


MEASURE_TIME = False


LIB_DIRECTORY = "lib"

EXAMPLE_NAMES = ["variables.zph", "buildInFunctions.zph", "list.zph", "MathObject.zph", "function.zph", "conditionalObject.zph", "ifStatement.zph", "ifElseStatement.zph", "loop.zph", "rng.zph", "predefVars1.zph", "predefVars2.zph", "libraries.zph"]
PROJECT_NAMES = ["sumCalculator", "guessNumber", "piApproximator"]
CURRENT_ELEMENT = 13 


FILE_DIRECTORY = "Examples" 
FILE_NAME = EXAMPLE_NAMES[CURRENT_ELEMENT-1]


#FILE_DIRECTORY = f"Projects/{PROJECT_NAMES[CURRENT_ELEMENT-1]}/" 
#FILE_DIRECTORY = f"." 
#FILE_NAME = "code.zph"


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
            line = line.lstrip().rstrip()    # remove spaces from start
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


def compiler(filename: str, fileDirectory: str = ".",):
    
    if filename.endswith(".zsrc"):
        filename = filename[: -len(".zsrc")] 
    elif filename.endswith(".zph"):
        filename = filename[: -len(".zph")] 
    
    with open(f"{fileDirectory}/{filename}.zsrc", "r") as file:
        code = json.load(file)
        
        
    currentIndex = 0
    maxIndex = len(code)    
    
    variables = {}
    
    while currentIndex < maxIndex:
        currentCmdName = code.get(list(code)[currentIndex])
        
        name = currentCmdName.get('name')
        base = currentCmdName.get('base')
        function = currentCmdName.get('function')
        paramsList = currentCmdName.get('paramsList')
        
        
        
        
        if function in TYPES:
            match function:
                case "INT"|"PT"|"FLOAT":
                    var = Variable(name, base, function, paramsList, variables)
                    variables.update({var.name: var})
                    
                case "LIST":
                    var = List(name, base, function, paramsList, variables)
                    variables.update({var.name: var})
                
                case "MO":
                    var = MO(name, base, function, paramsList, variables)
                    variables.update({var.name: var})
                    
                case "FUNC":
                    var = FUNC(name, base, function, paramsList, variables)
                    variables.update({var.name: var})
                    
                case "CO":
                    var = CO(name, base, function, paramsList, variables)
                    variables.update({var.name: var})
                    
                case "IF":
                    var = IF(name, base, function, paramsList, variables, currentIndex)
                    variables.update({var.name: var})
                    currentIndex = var.checkCondition(variables)
                    
                case "LOOP":
                    var = LOOP(name, base, function, paramsList, variables, currentIndex)
                    variables.update({var.name: var})
                    
                case "RNG":
                    var = RNG(name, base, function, paramsList, variables)
                    variables.update({var.name: var})
            
        
        elif name == "__":
            match base:
                case "?":
                    match function:
                        case "JUMP":
                            currentIndex = int(paramsList[0]) -1
                            continue
                        case "predefVars":
                            var = PredefVar(name, base, function, paramsList, fileDirectory, variables)
                            variables = var.read()
                        
                        case "dumpVars":
                            var = PredefVar(name, base, function, paramsList, fileDirectory, variables)
                            var.dump()
                        case _:
                            print(f"ERROR: {name} has no function # {function}! | {name} {base} {function}")
                            quit()
        

        elif function == "CT" and variables[name].type not in ["INT", "PT", "FLOAT"]:
            variables = changeType(name, paramsList[0], variables)
            
        else:               
            match variables[name].type:
                case "INT"|"PT"|"FLOAT"|"LIST"|"MO"|"FUNC"|"CO"|"RNG":
                    variables[name].matchFunction(base, function, paramsList, variables)
                case "IF"|"LOOP":
                    currentIndex = variables[name].matchFunction(base, function, paramsList, variables, currentIndex)

        
        
        
        currentIndex += 1
    print("\n\n", variables)


if __name__ == "__main__":
    lexer(FILE_NAME, FILE_DIRECTORY)
    compiler(FILE_NAME, FILE_DIRECTORY)