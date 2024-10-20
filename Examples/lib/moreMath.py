def search(name, base, function, paramsList, vars):
    match function:
        case "?":
            match base:
                case "add5":
                    vars = add10(vars, vars[paramsList[0]])
                    
                case "add10":
                    vars = add10(vars, vars[paramsList[0]])
    return vars

def add5(vars, var):
    a = int(var.value)
    b = a + 5
    var.value = str(b)
    vars.update({var.name: var})
    return vars

def add10(vars, var):
    a = int(var.value)
    b = a + 5
    var.value = str(b)
    vars.update({var.name: var})
    return vars