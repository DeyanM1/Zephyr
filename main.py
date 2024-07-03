from functions import *



TYPES = ["INT", "FLOAT", "PT"]
USE_COMMANDS = ["?"]
DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

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


        match func:
            case "?":
                match base:
                    case "push": 
                        Push(vars, name).print()
                    
                    case "CT":
    
                        vars.get(name).change_type(vars, paramsList[0]) # [0] = Type to change

                        #check_existance(vars, name)
                        #if not paramsList[0] in TYPES:
                        #    Error(105, paramsList[0]).as_string()
                        #if vars.get(name).change_type(paramsList[0]) != True:
                        #    Error(102, paramsList[0]).as_string()
                        

                
                    case "(":
                        pass

                    case "w":
                        vars.get(name).change_value(paramsList[0])

                        #vars.update({var.name: var})
                    
                    
            
                    case _:
                        Error(201, base).as_string()
            
            case "#":
                match base:
                    case base if base in TYPES:
                        if 0 <= 1 < len(paramsList):
                            if paramsList[1] == "~1":
                                var = Variable(name, base, paramsList[0], True)
                            else:
                                var = Variable(name, base, paramsList[0], False)
                        else:
                            var = Variable(name, base, paramsList[0], False)

                        vars.update({var.name: var})

            
            case "+":
                match base:
                    case "+":
                        match paramsList[0]:
                            case "+":
                                values = []
                                for i in range(2, len(paramsList)):
                                    values.append(paramsList[i])
                                vars.get(name).math(paramsList[0], values)

    print(vars)



if __name__ == "__main__":
    c = convert("code.zl")
    #print(c)
    compile(c)
    #print(compile(c))