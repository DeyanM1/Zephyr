import RPi.GPIO as GPIO


def matchFunction(self, base, function, paramsList, variables):
    match base:
        case "#":
            match function:
                case "INIT":
                    match paramsList[0]:
                        case "BCM":
                            GPIO.setmode(GPIO.BCM)
                        case "BOARD":
                            GPIO.setmode(GPIO.BOARD)
                case _:
                    pass
        case "?":
            match function:
                case "SETUP":
                    match paramsList[1]:
                        case "OUT":
                            GPIO.setup(int(paramsList[0]), GPIO.OUT)
                        case "IN":
                            GPIO.setup(int(paramsList[0]), GPIO.IN)
                case "SET":
                    set(variables, paramsList[0], paramsList[1])
                            
                case "READ":
                    variables = read(variables, int(paramsList[0]), paramsList[1])
                
                case "RESET":
                    GPIO.cleanup()
                case _:
                    pass
    return variables

def set(variables, pin, valueToSet):
    value = valueToSet
    
    if valueToSet.startswith("'"):
        valueVarName = valueToSet.replace("'", "")
        value = variables[valueVarName].value

    match value:
        case "LOW"|"0"|"~0"|0:
            GPIO.output(pin, GPIO.LOW)
        case "HIGH"|"1"|"~1"|1:
            GPIO.output(pin, GPIO.HIGH)

def read(variables, pin, outputVar):
    value = GPIO.input(pin)
    variables[outputVar].value = value
    
    return variables