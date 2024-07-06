from functions import *



TYPES = ["INT", "PT"]
USE_COMMANDS = ["?"]


"""
    PT = Printable Text
    Int = Integer
    Float = Float


    True: ~1, 
    False: ~0

    a ? Int:551|~1;
    a ? w:123
    a ? w:+<Variable Name>
"""

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
    for func in code:
        comm, params = func.split(":")
        paramsList = params.split("|")

        name, func, base = comm.split(" ")
        name, base = name.replace(" ", ""), base.replace(" ", "")


        if name.startswith("#"):
            continue

        match func:
            case "?":
                match base:
                    case "push": 
                        Push(vars.get(name))
                    
                    case base if base.startswith("("):
                        vars.get(name).set_equation(base)
                        vars.get(name).prepare(vars)

                    case "w":
                        vars.get(name).change_value(paramsList[0])              
                    
            
                    case _:
                        Error(201, base).as_string()
            
            case "#":
                match base:
                    case "CT":
                        print(vars.get(name))
                        change_type(vars.get(name), vars, paramsList[0]) # [0] = Type to change

                    case "MO":
                        var = MathObject(name)
                        vars.update({var.name: var})

                    case base if base in TYPES:
                        if 0 <= 1 < len(paramsList):
                            if paramsList[1] == "~1":
                                var = Variable(name, base, paramsList[0], True)
                            else:
                                var = Variable(name, base, paramsList[0], False)
                        else:
                            var = Variable(name, base, paramsList[0], False)

                        vars.update({var.name: var})
                    
                    case _:
                        Error(201, base).as_string()

    
    #print(vars.get("a").type)
    print(vars)



if __name__ == "__main__":
    c = convert("code.lys")
    #print(c)
    compile(c)
    #print(compile(c))