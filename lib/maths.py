def search(name, func, base, paramsList, vars):
    match func:
        case "?":
            match base:
                case "add10":
                    vars = add10(vars, vars[paramsList[0]])
    
    return vars


def add10(vars, var):
    a = int(var.value)
    b = a + 10
    var.value = str(b)
    
    vars.update({var.name: var})
    return vars