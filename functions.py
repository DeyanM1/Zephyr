import re
import json
import random
import os
import time
import importlib
from functools import wraps
import signal


INT_reg = r"^\d+$"
FLOAT_reg = r'^\d+\.\d+$'
PT_reg = r"^'.*'$"



TYPES = ["PT", "INT", "FLOAT", "LIST", "MO", "FUNC", "CO", "IF", "LOOP", "RNG", "PredefVar", "LIB"]


DIGITS = "0123456789"

RETURN_FUNCION_COMMANDS = ["RES", "VC"]
RANDOM_NUMBER_TYPES = ["INT"]

BOOL_TRANSFORM = {"~0": False, "~1": True}


class Error(Exception):
    ERROR_MESSAGES = {
        101: "ERROR: {type} has no function # {function}! ({name})   | {name} {base} {function}", # *
        102: "ERROR: {unknownName} -> Unknown Variable! {description} | {name} {base} {function}", # *
        103: "ERROR: Keyboard interrupt! | Stopping...",
        110: "ERROR: {type} != {descriptionChild} -> unsupported type! \n{description} | {name} {base} {function}", # *
        201: "ERROR: {type} != PT -> Only PT type is pushable! | {name} {base} {function}", # Variable
        202: "ERROR: {index} -> Invalid positional Value! \n{description} | {name} {base} {function}", # Variable, LIST
        203: "ERROR: {returnFunction} -> Invalid return function! | {name} {base} {function}", # FUNC
        204: "ERROR: {descriptionChild} -> {description} | {name} {base} {function}", # CO
        205: "ERROR: {libName} -> cant import library! ({libPath}.{libName}) | {name} {base} {function}", # RNG
    }

    def __init__(self, errorCode, **kwargs):
        """
        101: "ERROR: {type} has no function # {function}! ({name})   | {name} {base} {function}", # *\n
        102: "ERROR: {unknownName} -> Unknown Variable! {description} | {name} {base} {function}", # *\n
        103: "ERROR: keyboard interrupt! | [{index}] {name} {base} {function}",
        110: "ERROR: {type} != {descriptionChild} -> unsupported type! \n{description} | {name} {base} {function}", # *\n
        201: "ERROR: {type} != PT -> Only PT type is pushable! | {name} {base} {function}", # Variable\n
        202: "ERROR: {index} -> Invalid positional Value! \n{description} | {name} {base} {function}", # Variable, LIST\n
        203: "ERROR: {returnFunction} -> Invalid return function! | {name} {base} {function}", # FUNC\n
        204: "ERROR: {descriptionChild} -> {description} | {name} {base} {function}", # CO\n
        205: "ERROR: {libName} -> cant import library! ({libPath}.{libName}) | {name} {base} {function}", # RNG\n


        Args:
            error_code (_type_): _description_
        """
        self.errorCode = errorCode
        self.message = self.ERROR_MESSAGES.get(errorCode, "Unknown error.").format(**kwargs)
        self.handle()

    def handle(self):
        print(f"\n[{self.errorCode}]  {self.message}")
        quit(self.errorCode)


def handle_keyboard_interrupt(signal_number, frame):
    raise Error(103)

def measureTime(func):
    @wraps(func)  # Keeps function metadata
    def wrapper(*args, measureTime=False, **kwargs):  # New keyword argument
        if measureTime:
            start_time = time.time()
            result = func(*args, **kwargs)  # Call the actual function
            end_time = time.time()
            print(f"Execution time ({func.__name__}): {end_time - start_time:.7f}s")

        else:
            result = func(*args, **kwargs)  # Just call the function without measuring time
        return result
    return wrapper



def checkValueForType(value: str, type: str):
    """_summary_
    This function checks if a value is compatible specific type

    Args:
        value (_type_): _description_
        type (_type_): _description_

    Returns:
        _type_: _description_
    """

    match type:
        case "PT":
            return value
        case "INT":
            if re.search(INT_reg, value) != None:
                return value
        case "FLOAT":
            if re.search(FLOAT_reg, value) != None:
                return value

    return None


def changeType(name: str, newType: str, variables: dict):

    """_summary_

    Args:
        name (_type_): name of the variable
        newType (_type_): newType for the Variable
        variables (_type_): current Variables
    Returns:
        _type_: variables
    """


    match variables[name].type:
        case "MO"|"FUNC"|"CO"|"RNG":
            compatibleTypes = ["PT", "INT", "FLOAT"]
            if newType not in compatibleTypes:
                raise Error(110, type=variables[name].type, descriptionChild=newType, description="new Type not supported", name=variables[name].name, base=variables[name].base, function=variables[name].function)


            var = Variable(variables[name].name, variables[name].base, newType, [variables[name].value, False], variables)
            variables.update({variables[name].name: var})

    return variables


signal.signal(signal.SIGINT, handle_keyboard_interrupt)
class Variable:
    def __init__(self, name, base, function, paramsList, variables):
        self.const = paramsList[1] if len(paramsList) < 1 else False
        self.name = name
        self.type = function
        self.value = None

        self.base = base    # FOR ERRORS
        self.function = function    # FOR ERRORS

        self.write(paramsList[0], variables)

        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const: ": self.const}


    def matchFunction(self, base, function, paramsList, variables):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:
                    case "CT":
                        self.changeType(paramsList[0])
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

            case "?":
                match function:
                    case "push":
                        self.push()

                    case "INPUT":
                        self.INPUT(paramsList[0], variables)

                    case "w":
                        self.write(paramsList[0], variables)
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)


    def changeType(self, newType):
        compatibleTypes = ["PT", "INT", "FLOAT"]

        if newType not in compatibleTypes:
            raise Error(110, type=self.type, descriptionChild=newType, description="new Type not supported",
                  name=self.name, base=self.base, function=self.function)


        if checkValueForType(str(self.value), newType) == None:
            raise Error(110, type=self.value, descriptionChild=newType, description="Value not compatible with new Type",
                  name=self.name, base=self.base, function=self.function)

        self.type = newType

    def push(self):
        if self.type == "PT":
            print(f"PUSH: {self.value}")
        else:
            raise Error(201, type=self.type, name=self.name, base=self.base, function=self.function)


    def write(self, newValue, variables):
        newValue = str(newValue)
        if self.const:
            return False

        if newValue.startswith("'"):
            var = newValue.replace("'", "")
            if "<" in var and ">" in var:
                varName, varIndex = var.split("<")
                varIndex = varIndex.replace(">", "")

                if varName not in variables.keys():
                    raise Error(202, index=varName, description="Index Variable not found!",
                                name=self.name, base=self.base, function=self.function)

                if variables[varName].type != "LIST":
                    raise Error(202, index=varName, description="Index Variable not a LIST!",
                                name=self.name, base=self.base, function=self.function)

                self.value = str(variables[varName].getValue(varIndex, variables))
                self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const: ": self.const}
            else:
                self.value = str(variables.get(var).value)
                self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const: ": self.const}

        elif newValue == "++":
            match self.type:
                case "INT":
                    self.value = str(int(self.value) + 1)
                case "FLOAT":
                    self.value = str(float(self.value) + 1.0)
                case "PT":
                    self.value = self.value + self.value
            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const: ": self.const}

        elif newValue == "--":
            match self.type:
                case "INT":
                    self.value = str(int(self.value) - 1)
                case "FLOAT":
                    self.value = str(float(self.value) - 1.0)
            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const: ": self.const}


        else:
            if checkValueForType(newValue, self.type) != None:
                self.value = newValue
                self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const: ": self.const}

            else:
                raise Error(110, type=self.value, descriptionChild=self.type, description="Value not compatible with new Type",
                  name=self.name, base=self.base, function=self.function)

    def INPUT(self, message, variables):
        value = input(message)
        self.write(value, variables)

class LIST:
    def __init__(self, name, base, function, paramsList, variables):
        self.name = name
        self.type = function

        self.elementsType = paramsList[0]

        self.data = []
        self.negData = []

        if len(paramsList) > 1:
            dataToAdd = paramsList[1].split(",")
            for pos in range(0, len(dataToAdd)):
                self.setValue(pos+1, dataToAdd[pos], variables)

        self.dumpConfig = {"name": self.name, "type": self.type, "elementsType": self.elementsType, "data": self.data, "negData: ": self.negData}


    def matchFunction(self, base, function, paramsList, variables):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:
                    case "SET":
                        self.setValue(paramsList[0], paramsList[1], variables)
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

    def setValue(self, pos, value, variables):
        pos = str(pos)
        if checkValueForType(value, self.elementsType) != None:
            if pos.startswith("'"):
                try:
                    name = pos.replace("'", "")
                    posVar = variables[name]
                    pos = int(posVar.value)
                except Exception as e:
                    raise Error(102, unknownName=name, name=self.name, base=self.base, function=self.function, description="Postion variable")

            else:
                pos = int(pos)

            pos = int(pos)


            if int(pos) == 0:
                raise Error(202, index=pos, description="Position cant be 0", name=self.name, base=self.base, function=self.base)

            elif pos >= 0:
                pos = pos-1
                # Treat as a positive index for self.data
                if pos < len(self.data):
                    self.data[pos] = value
                else:
                    self.data.extend([None] * (pos - len(self.data) + 1))
                    self.data[pos] = value
            else:
                # Treat as a positive index for self.negData (remove negative sign)
                pos = abs(pos+2)  # Convert negative index to positive index
                if pos < len(self.negData):
                    self.negData[pos] = value
                else:
                    self.negData.extend([None] * (pos - len(self.negData) + 1))
                    self.negData[pos] = value

        self.dumpConfig = {"name": self.name, "type": self.type, "elementsType": self.elementsType, "data": self.data, "negData: ": self.negData}


    def getValue(self, pos, variables):
        if pos.startswith("'"):
            try:
                name = pos.replace("'", "")
                posVar = variables[name]
                pos = int(posVar.value)
            except Exception as e:
                raise Error(102, unknownName=name, name=self.name, base=self.base, function=self.function, description="Postion variable")
        if int(pos) == 0:
            raise Error(202, index=pos, description="Position cant be 0", name=self.name, base=self.base, function=self.base)

        elif int(pos) > 0:
            pos = int(pos)-1
            try:
                return self.data[pos]

            except IndexError:
                raise Error(202, index=pos, description="Index is out of range", name="", base="", function="")


        else:
            pos = abs(int(pos)+1)
            try:
                return self.negData[pos]

            except IndexError:
                raise Error(202, index=pos, description="Index is out of range", name="", base="", function="")

class MO:
    def __init__(self, name, base, function, paramsList, variables):
        """
        name = name
        base = base
        function = Type
        paramsList[0] = equation

        """
        self.const = False
        self.name = name
        self.type = function
        self.value = 0

        self.equation = ""
        self.calculation = ""


        if len(paramsList) == 1:
            if paramsList[0] != "":
                self.equation = paramsList[0]
                self.prepare(variables)



        self.base = base    # FOR ERRORS
        self.function = function    # FOR ERRORS

        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "equation": self.equation, "calculation": self.calculation}



    def matchFunction(self, base, function, paramsList, variables):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:
                    case function if function.startswith("("):

                        self.setEquation(function)
                        self.prepare(variables)
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

    def setEquation(self, equation):
        self.equation = equation
        self.dumpConfig = {self.name: {"name": self.name, "type": self.type, "value": self.value, "equation": self.equation, "calculation": "None"}}

    def prepare(self, variables):
        self.calculation = ""
        in_var = False
        variablestr = ""


        for elem in self.equation:
            if elem in DIGITS and in_var == False: self.calculation += elem
            elif elem == "+": self.calculation += "+"
            elif elem == "-": self.calculation += "-"
            elif elem == "*": self.calculation += "*"
            elif elem == "/": self.calculation += "/"
            elif elem == "(": self.calculation += "("
            elif elem == ")": self.calculation += ")"
            elif elem == "'":
                if in_var:
                    try:
                        if variables.get(variablestr).type not in ["INT", "FLOAT"]:
                            raise Error(110, type=variables.get(variablestr).type, descriptionChild="INT/FLOAT", description="incompatible variable for calculation!", name=self.name, base=self.base, function=self.function)

                        self.calculation += str(variables.get(variablestr).value)
                        variablestr, in_var = "", False
                    except Exception as e:
                        raise Error(102, unknownName=variablestr, name=self.name, base="?", function="()", description="variable for calculation")
                else:
                    in_var = True


            elif elem == "'":
                #varList.update({variablestr: variables.get(variablestr).value})
                self.calculation += str(variables.get(variablestr).value)
                variablestr, in_var = "", False

            elif elem.isalpha() or isinstance(int(elem), int):
                if in_var: variablestr += elem

        self.calculate()

    def calculate(self):
        # TODO: make better calculation, because very unsafe: https://stackoverflow.com/questions/9685946/math-operations-from-string
        self.value = eval(self.calculation)
        self.dumpConfig = {self.name: {"name": self.name, "type": self.type, "value": self.value, "equation": self.equation, "calculation": "None"}}

class FUNC:
    def __init__(self, name, base, function, paramsList, variables):
        self.const = paramsList[1] if len(paramsList) < 1 else False

        self.const = False
        self.name = name
        self.type = function
        self.value = 0

        if len(paramsList) == 2:
            if paramsList[1] != "":
                self.const = BOOL_TRANSFORM[paramsList[1]]

        if paramsList[0] in RETURN_FUNCION_COMMANDS:
            self.return_func = paramsList[0]
        else:
            raise Error(203, returnFunction=paramsList[0], name=self.name, base=base, function=function)


        self.MathObject = None

        self.base = base    # FOR ERRORS
        self.function = function    # FOR ERRORS

        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const": self.const, "MO": "None"}

    def matchFunction(self, base, function, paramsList, variables):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:
                    case function if function.startswith("("):
                        self.setEquation(function, variables)


                    case "call":
                        self.call(variables)
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)


    def setEquation(self, equation, variables):
        self.MathObject = MO(self.name, "#", "MO", [equation], variables)
        self.MathObject.prepare(variables=variables)
        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const": self.const, "MO": {"name": self.MathObject.name, "type": self.MathObject.type, "value": self.MathObject.value, "equation": self.MathObject.equation, "calculation": self.MathObject.calculation}}

    def VC(self, variables):
        self.MathObject.prepare(variables=variables)
        self.value = self.MathObject.value
        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const": self.const, "MO": {"name": self.MathObject.name, "type": self.MathObject.type, "value": self.MathObject.value, "equation": self.MathObject.equation, "calculation": self.MathObject.calculation}}


    def call(self, variables):
        if not self.const:
            self.MathObject.prepare(variables=variables)
            self.value = self.MathObject.value
        else:
            self.value = self.MathObject.value
        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "const": self.const, "MO": {"name": self.MathObject.name, "type": self.MathObject.type, "value": self.MathObject.value, "equation": self.MathObject.equation, "calculation": self.MathObject.calculation}}

class CO:
    def __init__(self, name, base, function, paramsList, variables):
        self.name = name
        self.type = function
        self.value = None

        self.rawCondition = ""
        self.condition = None

        self.base = base    # FOR ERRORS
        self.function = function    # FOR ERRORS


        if paramsList[0] != "":
            self.setCondition(paramsList[0], variables)

        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "condition": self.condition}

    def matchFunction(self, base, function, paramsList, variables):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:
                    case function if function.startswith("("):
                        self.setCondition(function, variables)
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

    def setCondition(self, condition, variables):
        self.rawCondition = condition
        self.prepare(variables)

    def prepare(self, variables):
        editCondition = ""
        in_var = False
        variablestr = ""


        for elem in self.rawCondition:
            if elem in DIGITS and in_var == False: editCondition += elem
            elif elem == '>': editCondition += elem
            elif elem == '<': editCondition += elem
            elif elem == '!': editCondition += elem
            elif elem == '=': editCondition += elem
            elif elem == '>': editCondition += elem
            elif elem == "'":
                if in_var:
                    if variables[variablestr].type != "INT" and variables[variablestr].type != "FLOAT":
                        raise Error(110, type=variables[variablestr].type, descriptionChild="INT/FLOAT",
                              description="incompatible variable for condition!", name=self.name, base=self.base, function=self.function)
                    editCondition += str(variables[variablestr].value)
                    variablestr, in_var = "", False

                else:
                    in_var = True

            elif elem.isalpha():
                if in_var: variablestr += elem

        self.condition = editCondition
        self.checkCondition()

    def checkCondition(self):
        try:
            if eval(f"{self.condition}"):
                self.value = "~1"
            else:
                self.value = "~0"

            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "condition": self.condition}


        except Exception:
            raise Error(204, descriptionChild=self.condition, description="Invalid condition!", name=self.name, base=self.base, function=self.function)

class IF:
    def __init__(self, name, base, function, paramsList, variables, startIndex):
        """
        paramsList[0] = conditionObjectName
        paramsList[1] = commandsInIF
        """

        self.name = name
        self.type = function
        self.value = None


        self.startIndex = startIndex

        self.conditionObjectName = paramsList[0]
        self.commandsInIF = paramsList[1]
        self.commandsInELSE = 0


        self.base = base    # FOR ERRORS
        self.function = function    # FOR ERRORS

        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "conditionalObjectName": self.conditionObjectName, "commandsInIF": self.commandsInIF, "self.commandsInELSE": self.commandsInELSE}

    def matchFunction(self, base, function, paramsList, variables, currentIndex):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:

                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:
                    case "ELSE":
                        self.commandsInELSE = paramsList[0]
                        if self.value == False:
                            pass
                        elif self.value == True:
                            currentIndex = currentIndex + int(self.commandsInELSE)
                        return currentIndex

                    case "END":
                        return currentIndex
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

    def checkCondition(self, variables):
        if variables.get(self.conditionObjectName).value == "~1":
            self.value = True
            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "conditionalObjectName": self.conditionObjectName, "commandsInIF": self.commandsInIF, "self.commandsInELSE": self.commandsInELSE}
            return self.startIndex
        else:
            self.value = False
            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "conditionalObjectName": self.conditionObjectName, "commandsInIF": self.commandsInIF, "self.commandsInELSE": self.commandsInELSE}
            return int(self.startIndex)+int(self.commandsInIF)

class LOOP:
    def __init__(self, name, base, function, paramsList, variables, startIndex):
        self.name = name
        self.type = function
        self.value = None

        self.startIndex = startIndex
        self.endIndex = False

        self.conditionObject = None

        self.infinite = False

        self.setCondition(paramsList[0], variables)



        self.base = base    # FOR ERRORS
        self.function = function    # FOR ERRORS

        if self.infinite == False:
            self.dumpConfig = {"name": self.name,
                            "type": self.type,
                            "value": self.value,
                            "startIndex": self.startIndex,
                            "EndIndex": self.endIndex,
                            "Infinite": self.infinite,
                            "conditionObject": {
                                    "name": self.conditionObject.name,
                                    "type": self.conditionObject.type,
                                    "value": self.conditionObject.value,
                                    "condition": self.conditionObject.condition
                            }}

    def matchFunction(self, base, function, paramsList, variables, currentIndex):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:
                    case "END":
                        index = self.loopEnd(currentIndex, variables)
                        return index
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

    def setCondition(self, conditionObjectName, variables):
        if conditionObjectName.isalpha():
            self.conditionObject = variables[conditionObjectName]
        elif conditionObjectName in BOOL_TRANSFORM.keys():
            self.infinite = True
            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value,"startIndex": self.startIndex, "EndIndex": self.endIndex, "Infinite": self.infinite}
    def loopEnd(self, endIndex, variables):
        if not self.endIndex:
            self.endIndex = endIndex

        if self.infinite:
            index = self.startIndex
            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value,"startIndex": self.startIndex, "EndIndex": self.endIndex, "Infinite": self.infinite}
            return index


        self.conditionObject.prepare(variables)
        if self.conditionObject.value != "~1":
            self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value,"startIndex": self.startIndex, "EndIndex": self.endIndex, "Infinite": self.infinite, "conditionObject": {"name": self.conditionObject.name, "type": self.conditionObject.type, "value": self.conditionObject.value, "condition": self.conditionObject.condition}}
            return endIndex



        index = self.startIndex
        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value,"startIndex": self.startIndex, "EndIndex": self.endIndex, "Infinite": self.infinite, "conditionObject": {"name": self.conditionObject.name, "type": self.conditionObject.type, "value": self.conditionObject.value, "condition": self.conditionObject.condition}}
        return index

class RNG:
    def __init__(self, name, base, function, paramsList, variables):
        self.name = name
        self.type = function
        self.value = None

        self.rngType = paramsList[0]
        self.rngRange = None

        self.base = base    # FOR ERRORS
        self.function = function  # FOR ERRORS

        self.setRange(paramsList[1])
        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "rngType": self.rngType, "rngRange": self.rngRange}

    def matchFunction(self, base, function, paramsList, variables):
        self.base = base
        self.function = function

        match base:
            case "#":
                match function:
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:
                    case "CR":
                        self.setRange(paramsList[0])
                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

    def setRange(self, rngRange):
        try:
            rangeMin, rangeMax = rngRange.replace(" ", "").split("->")
            rangeMin, rangeMax = int(rangeMin), int(rangeMax)
            self.rngRange = [rangeMin, rangeMax]
        except Exception as e:
            raise Error(204, descriptionChild=rngRange, description="Invalid RNG-Range!", name=self.name, base=self.base, function=self.function)



        self.generateRNG()

    def generateRNG(self):
        #self.value = np.random.randint(self.rngRange[0], self.rngRange[1], size=1).item()
        self.value = random.randint(self.rngRange[0], self.rngRange[1])
        self.dumpConfig = {"name": self.name, "type": self.type, "value": self.value, "rngType": self.rngType, "rngRange": self.rngRange}

class PredefVar:
    def __init__(self, name, base, function, paramsList, fileDirectory, variables):
        self.name = name
        self.type = function
        self.value = None

        self.fileName = paramsList[0]
        self.fileDirectory = fileDirectory

        self.variablesDump = variables
        self.variablesRead = {}

        self.base = base    # FOR ERRORS
        self.function = function  # FOR ERRORS

    def read(self):
        with open(f"{self.fileDirectory}/lib/{self.fileName}.zpkg", "r") as file:
            data = json.load(file)
            for var in data:
                self.compile(data[var])


        return self.variablesRead


    def compile(self, data):
        name = data["name"]
        base = "#"
        function = data["type"]
        paramsList = [data["value"], ""]
        variables = self.variablesRead


        match function:
            case "INT"|"PT"|"FLOAT":
                var = Variable(name, base, function, paramsList, variables)
                self.variablesRead.update({var.name: var})

            case "LIST":
                var = LIST(name, base, function, paramsList, variables)
                self.variablesRead.update({var.name: var})

            case "MO":
                var = MO(name, base, function, paramsList, variables)
                self.variablesRead.update({var.name: var})

            case "FUNC":
                var = FUNC(name, base, function, paramsList, variables)
                self.variablesRead.update({var.name: var})

            case "CO":
                var = CO(name, base, function, paramsList, variables)
                self.variablesRead.update({var.name: var})

            case "RNG":
                paramsList[1] = f"{data['rngRange'][0]}->{data['rngRange'][1]}"
                var = RNG(name, base, function, paramsList, variables)
                self.variablesRead.update({var.name: var})

    def dump(self):
        data = {}

        for var in self.variablesDump.values():
            name = var.dumpConfig["name"]
            dump = var.dumpConfig

            data[name] = dump


        os.makedirs(os.path.dirname(f"{self.fileDirectory}/lib/"), exist_ok=True)
        file = open(f"{self.fileDirectory}/lib/{self.fileName}.zpkg", "w")
        json.dump(data, file, indent=4)

class LIB:
    def __init__(self, name, base, function, paramsList, libPath, variables):
        self.const = paramsList[1] if len(paramsList) < 1 else False
        self.name = name
        self.type = function
        self.value = None

        self.libPath = libPath
        self.libName = paramsList[0]
        self.libObject = None

        self.base = base    # FOR ERRORS
        self.function = function    # FOR ERRORS

        self.setLib()

    def matchFunction(self, base, function, paramsList, variables) -> dict:
        self.base = base
        self.function = function

        return self.libObject.matchFunction(self.name, base, function, paramsList, variables)

        match base:
            case "#":
                match function:

                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)
            case "?":
                match function:

                    case _:
                        raise Error(101, name=self.name, function=function, type=self.type, base=self.base)

    def setLib(self):
        try:
            module = importlib.import_module(f"{self.libPath}.{self.libName}")
            self.libObject = module
            self.dumpConfig = {"name": self.name,
                            "type": self.type,
                            "libFolderName": self.libPath,
                            "libName": self.libName}

        except ImportError as e:
            raise Error(205, libName=self.libName, libPath=self.libPath, name=self.name, base=self.base, function=self.function)
