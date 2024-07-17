from functions import *
import time

MEASURE_TIME = False

def convert(filename: str):

    replaceList = ["\n", "\r", "\t"]

    converted_code = []
    current_function = ""
    with open(filename, "r") as file:
        for line in file:  
            for char in line: 
                if char == ";":
                    if current_function.startswith(" "):
                        current_function = current_function[1:]
                        while current_function.startswith(" "):
                            current_function = current_function[1:]
                    converted_code.append(current_function)
                    current_function = ""
                    continue
                elif char in replaceList:
                    continue
                else:
                    current_function = current_function + char
    print(converted_code)
    return converted_code



def compile(code):
    vars = {}
    libs = {}
    index = 0
    while index <= len(code)-1:
        if '\n' in code[index]: 
            index += 1
            continue
        
        comm, params = code[index].split(":")
        paramsList = params.split("|")

        name, func, base = comm.split(" ")
        name, base = name.replace(" ", ""), base.replace(" ", "")


        if name.startswith("#"):
            index += 1
            continue

        elif name == "__":
            match func:
                case "?":
                    match base:
                        case "JUMP":
                            index = int(paramsList[0]) -1
                            continue

        elif func == "@": # Libraries
            libs.update({name, base})
            
            #var = Library(name, base)
            #vars.update({var.name: var})

        elif base in TYPES:
            match base:
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
                
                case _:
                    if 0 <= 1 < len(paramsList):
                        if paramsList[1] == "~1":
                            var = Variable(name, base, paramsList[0], True)
                        else:
                            var = Variable(name, base, paramsList[0], False)
                    else:
                        var = Variable(name, base, paramsList[0], False)

                        vars.update({var.name: var})


        elif vars[name].type == Token.PT:
            match func:
                case "?":
                    match base:
                        case "push": 
                            Push(vars[name])
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case _:
                            Error(501, ["Token.PT", f"? {base}"]).as_string()
                case "#":
                    match base:
                        case "CT":
                            vars = change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        case _:
                            Error(501, ["Token.PT", f"# {base}"]).as_string()

        elif vars[name].type == Token.INT:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].change_value(paramsList[0])
                        
                        case "CT":
                            vars = change_type(vars[name], vars, paramsList[0]) # [0] = Type to change

                        case _:
                            Error(501, ["Token.INT", f"? {base}"]).as_string()

        elif vars[name].type == Token.MO:
            match func:
                case "?":
                    match base:
                        case "w":
                            vars[name].set_equation(paramsList[0])
                        
                        case "CT":
                            vars = change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                        
                        case base if base.startswith("("):
                            vars[name].set_equation(base)
                            vars[name].prepare(vars)

                        case _:
                            Error(501, ["Token.MO", f"? {base}"]).as_string()
        
        elif vars[name].type == Token.FUNC:
            match func:
                case "?":
                    match base:
                        case "CT":
                            vars = change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                            
                        case base if base.startswith("("):
                            if vars[name].type == Token.FUNC:
                                vars[name].set_function(base, vars)
                        
                        case "call":
                            vars[name].call(vars)
                            
                        case _:
                            Error(501, ["Token.MO", f"? {base}"]).as_string()
                case "#":
                    match base:    
                        case _:
                            Error(501, ["Token.MO", f"# {base}"]).as_string()
        
        elif vars[name].type == Token.LOOP:
            match func:
                case "?":
                    match base:
                        case "END":
                            index = vars[name].END(index, vars)
                        case _:
                            Error(501, ["Token.LOOP", f"? {base}"]).as_string()          
                case "#":
                    match base:
                        case _:
                            Error(501, ["Token.LOOP", f"# {base}"]).as_string()
    
        elif vars[name].type == Token.CO:
            match func:
                case "?":
                    match base:
                        case "CT":
                            vars = change_type(vars[name], vars, paramsList[0]) # [0] = Type to change
                            
                        case _:
                            Error(501, ["Token.CO", f"? {base}"]).as_string()
                
                case "#":
                    match base:
                        case _:
                            Error(501, ["Token.CO", f"# {base}"]).as_string()
    
        else:
            search(code[index], vars, libs)
        index += 1
    
    print("\n", vars)






if __name__ == "__main__":
    if MEASURE_TIME: st = time.time()
    
    c = convert("code.lys")
    compile(c)
    
    if MEASURE_TIME: et = time.time(); elapsed_time = et - st; print(f"\n Elapsed time: {elapsed_time}s")