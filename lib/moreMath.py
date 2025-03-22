def matchFunction(self, base, function, paramsList, variables):
    match base:
        case "#":
            match function:
                case _:
                    pass
        case "?":
            match function:
                case "exponentiation":
                    variables = exponentiation(variables, paramsList[0], paramsList[1])
                case "root":
                    variables = root(variables, paramsList[0], paramsList[1])
                case "factorial":
                    variables = factorial(variables, paramsList[0])

                    
                case _:
                    pass
    return variables


def exponentiation(variables, baseVar, exponentVar):
    base = int(variables[baseVar].value)
    exponent = int(variables[exponentVar].value)
    result = base ** exponent
    variables[baseVar].value = result
    
    return variables


def root(variables, baseVar, exponentVar):
    base = int(variables[baseVar].value)
    exponent = int(variables[exponentVar].value)
    result = base ** (1/exponent)
    variables[baseVar].value = result
    
    return variables

def factorial(variables, baseVar):
    base = int(variables[baseVar].value)
    
    result = 1
    for i in range(2, base + 1):
        result *= i
    
    variables[baseVar].value = result
    return variables
    
    

