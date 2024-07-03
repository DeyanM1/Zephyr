from functions import *



TYPES = ["INT", "Float", "PT"]
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


        match func:
            case "?":
                match base:
                    case "push": 
                        check_existance(vars, name)
                        if vars.get(name).type != PT:
                            print("ERROR: Value not a printable text!!")
                            quit()
                        push = Push(vars.get(name).value).print()
                        print(push)
                    
                    case "CH":
                        check_existance(vars, name)
                        if not paramsList[0] in TYPES:
                            print("ERROR: Type is not supported")
                            quit()
                        if vars.get(name).change_type(paramsList[0]) != True:
                            print("ERROR: Cannot change - Variable is constant")
                        

                    case base if base in TYPES:
                        if 0 <= 1 < len(paramsList):
                            if paramsList[1] == "~1":
                                var = Variable(name, base, paramsList[0], True)
                            else:
                                var = Variable(name, base, paramsList[0], False)
                        else:
                            var = Variable(name, base, paramsList[0], False)

                        vars.update({var.name: var})

                    case "w":
                        vars.get(name).change_value(paramsList[0])

                        #vars.update({var.name: var})
                    
                    case "M":
                        
                    
            
                    case _:
                        print(print(Error(201, func).as_string()))
                        quit()
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