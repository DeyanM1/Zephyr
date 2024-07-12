from functions import *


def convert(filename: str):

    replaceList = ["\n", "\r", "\t"]

    converted_code = []
    current_function = ""
    with open(filename, "r") as file:
        for line in file:  
            for char in line: 
                if char == ";":
                    converted_code.append(current_function)
                    current_function = ""
                    continue
                elif char in replaceList:
                    continue
                else:
                    current_function = current_function + char
    return converted_code

def compile(code):
    vars = {}
    index = 0
    while index <= len(code)-1:
        comm, params = code[index].split(":")
        paramsList = params.split("|")

        name, func, base = comm.split(" ")
        name, base = name.replace(" ", ""), base.replace(" ", "")


        if name.startswith("#"):
            continue

        if base in TYPES:
            match base:
                case "MO":
                    var = MathObject(name)
                    vars.update({var.name: var})
                
                case "FUNC":
                    if 0 <= 1 < len(paramsList):
                        if paramsList[1] == "~1":
                            var = Function(name, paramsList[0], True)
                        else:
                            var = Function(name, paramsList[0], False)
                    else:
                        var = Function(name, paramsList[0])

                    vars.update({var.name: var})
                
                case _:
                    if 0 <= 1 < len(paramsList):
                        if paramsList[1] == "~1":
                            var = Variable(name, base, paramsList[0], True)
                        else:
                            var = Variable(name, base, paramsList[0], False)
                    else:
                        var = Variable(name, base, paramsList[0], False)

                        vars.update({var.name: var})

        if vars[name].type == Token.PT:
            match func:
                case "?":
                    match base:
                        case "push": 
                            Push(vars[name])
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case _:
                            Error(501, ["Token.PT", base]).as_string()
                case "#":
                    match base:
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", base]).as_string()


        elif vars[name].type == Token.INT:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change

                        case _:
                            Error(501, ["Token.INT", base]).as_string()

        elif vars[name].type == Token.MO:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        
                        case base if base.startswith("("):
                            vars[name].set_equation(base)
                            vars[name].prepare(vars)

                        case _:
                            Error(501, ["Token.MO", base]).as_string()
        
        elif vars[name].type == Token.FUNC:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].change_value(paramsList[0])
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case base if base.startswith("("):
                            if vars[name].type == Token.FUNC:
                                vars[name].set_function(base, vars)
                        
                        case "call":
                            vars[name].call(vars)
                            
                        case _:
                            Error(501, ["Token.MO", base]).as_string()
        index += 1
    
    print("\n", vars)




"""
def compile(code):
    vars = {}
    for func in code:
        comm, params = func.split(":")
        paramsList = params.split("|")

        name, func, base = comm.split(" ")
        name, base = name.replace(" ", ""), base.replace(" ", "")


        if name.startswith("#"):
            continue

        if base in TYPES:
            match base:
                case "MO":
                    var = MathObject(name)
                    vars.update({var.name: var})
                
                case "FUNC":
                    if 0 <= 1 < len(paramsList):
                        if paramsList[1] == "~1":
                            var = Function(name, paramsList[0], True)
                        else:
                            var = Function(name, paramsList[0], False)
                    else:
                        var = Function(name, paramsList[0])

                    vars.update({var.name: var})
                
                case _:
                    if 0 <= 1 < len(paramsList):
                        if paramsList[1] == "~1":
                            var = Variable(name, base, paramsList[0], True)
                        else:
                            var = Variable(name, base, paramsList[0], False)
                    else:
                        var = Variable(name, base, paramsList[0], False)

                        vars.update({var.name: var})

        if vars[name].type == Token.PT:
            match func:
                case "?":
                    match base:
                        case "push": 
                            Push(vars[name])
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case _:
                            Error(501, ["Token.PT", base]).as_string()
                case "#":
                    match base:
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", base]).as_string()


        elif vars[name].type == Token.INT:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change

                        case _:
                            Error(501, ["Token.INT", base]).as_string()

        elif vars[name].type == Token.MO:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        
                        case base if base.startswith("("):
                            vars[name].set_equation(base)
                            vars[name].prepare(vars)

                        case _:
                            Error(501, ["Token.MO", base]).as_string()
        
        elif vars[name].type == Token.FUNC:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].change_value(paramsList[0])
                        case "CT":
                            change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case base if base.startswith("("):
                            if vars[name].type == Token.FUNC:
                                vars[name].set_function(base, vars)
                        
                        case "call":
                            vars[name].call(vars)
                            
                        case _:
                            Error(501, ["Token.MO", base]).as_string()

    
    print("\n", vars)"""




if __name__ == "__main__":
    c = convert("code.lys")
    compile(c)