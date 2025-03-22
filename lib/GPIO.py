#import RPi.GPIO as GPIO

GPIO = ""

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
                    match paramsList[1]:
                        case "LOW"|"0"|"~0":
                            GPIO.output(paramsList[0], GPIO.LOW)
                        case "HIGH"|"1"|"~1":
                            GPIO.output(paramsList[0], GPIO.HIGH)
                case "READ":
                    variables = read(variables, paramsList[0], paramsList[1])

                case _:
                    pass
    return variables


def read(variables, pin, outputVar):
    value = GPIO.input(pin)
    variables[outputVar].value = value
    
    return variables