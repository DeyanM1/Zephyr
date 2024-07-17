def __init__(name, func, base, paramsList):
    pass




def adder_10(vars, var):
    a = var.value
    b = a + 10
    var.value = b
    
    vars.update({var.name: var})
    return vars