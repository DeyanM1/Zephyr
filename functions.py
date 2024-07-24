import re
import importlib

int_reg = r"^\d+$"
PT_reg = r"^'.*'$"

DEBUG = False

global DIGITS; DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
global TYPES; TYPES = ["INT", "PT", "MO", "FUNC", "LOOP", "CO", "LIB"]
global BOOL; BOOL = ["~1", "~0"]
global CONDITIONS; CONDITIONS = [">", "<", "==", "!=", ">=", "<="]
global TRANSLATE_BOOL; TRANSLATE_BOOL = {"~1":"True", "~0":"False"}

class Token:
    def __init__(self, type_):
        self.type = assignType(type_) if assignType(type_) else Error(105, type_).as_string()
        self.value = None
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
    def INT(self):
        return self.type

    def PT(self):
        return self.type
    
    def MO(self):
        return self.type
    
    def CO(self):
        return self.type
    
    def FUNC(self):
        return self.type

    def LOOP(self):
        return self.type
    
    def Lib(self):
        return self.type
     

class Error:
    def __init__(self, exception_code:int, details):
        self.exception_code = exception_code
        self.details = details
    
    def as_string(self):
        match self.exception_code:
            case 101: print("ERROR: Value not accepted | Variable: %s" % self.details)
            case 102: print("ERROR: Variable is constant | Variable: %s" % self.details)
            case 103: print("ERROR: Result Variable must be int or float | Variable: %s" % self.details)
            case 104: print("ERROR: Value not a printable Text | Value: %s" % self.details)
            case 105: print("ERROR: Unknown variable | Variable: %s" % self.details)
            case 106: print("ERROR: Variable type not supported | Value: %s" % self.details)
            case 107: print("ERROR: Variable Value inappropriate for changing to: |  %s" % self.details)
            case 201: print("ERROR: Unknown Function | Name: %s" % self.details)
            case 301: print("ERROR: No Digits in Math equations | Value: %s" % self.details)
            case 401: print("ERROR: Unknown Return function | Function: %s" % self.details)
            case 501: print(f"ERROR: Type {self.details[0]} has no function: {self.details[1]}")
            case 601: print(f"ERROR: Unknown library name: {self.details[0]} in variable: {self.details[1]}")
        quit()

class Debug:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def as_string(self):
        if DEBUG:
            print(f"{self.name}: {self.description}")




def checkTypeForValue(type, value):
    match type:
        case "INT" | Token.INT:
            if not re.search(int_reg, value):
                return False
            return Token.INT
        case "PT" | Token.PT:
            return Token.PT
        case _:
            return False
        
def checkVariableExistence(vars, name):
    if name not in vars.keys():
        Error(105, name).as_string()

def assignType(type):
    match type:
        case "INT": return Token.INT
        case "PT": return Token.PT
        case "MO": return Token.MO

def changeType(var, vars, newType):
    checkVariableExistence(vars, var.name)

    if not newType in TYPES:
        Error(106, newType).as_string() 

    if var.const:
        Error(102, var.name).as_string()

    if var.type == Token.MO or var.type == Token.FUNC:
        #print("type", assign_type(newType))
        Debug(var.name, f"{var.type} set to: {newType}").as_string()
        vars.update({var.name: Variable(name=var.name, type=newType, value=var.value, const=var.const)})
        

    elif checkTypeForValue(newType, var.value):
        Debug(var.name, f"{var.type} set to: {newType}").as_string()
        var.type = assignType(newType) 
    else:
        Error(107, newType).as_string()

    return vars



class Variable:
    def __init__(self, name, type, value, const = False):
        self.name = name
        self.type = assignType(type) if checkTypeForValue(type, value) else Error(101, self.name).as_string()
        self.value = value
        self.const = const

    
    def getType(self):
        return self.type

    def changeValue(self, value):
        if self.const:
            return False
        
        if value == "++":
            self.value = str(int(self.value) + 1)
        else:  
            if checkTypeForValue(self.type, value):
                self.value = value
            else:
                Error(101, self.name).as_string()	

        return True

    def push(self):
        print("PUSH: ", self.value)
    
    def setValueByInput(self, text):
        self.value = input(text)

class MathObject:
    def __init__(self, name, value = 0, equation = ()):
        self.name = name
        self.type = Token.MO  # >> For Consistency
        self.const = False # >> For Consistency
        self.value = value

        self.equation = equation
        self.calculation = ""


    
    def setEquation(self, equation):
        Debug(self.name, "equation set to %s" % equation)
        self.equation = equation

    def prepare(self, vars):
        Debug(self.name, "prepare with calculation: %s" % self.calculation).as_string()

        self.calculation = ""
        in_var = False
        varStr = ""


        
        for elem in self.equation:
            if elem in DIGITS: Error(301, self.equation).as_string()
            elif elem == "+": self.calculation += "+"
            elif elem == "-": self.calculation += "-"
            elif elem == "*": self.calculation += "*"
            elif elem == "/": self.calculation += "/"
            elif elem == "(": self.calculation += "("
            elif elem == ")": self.calculation += ")"
            elif elem == "'": 
                if in_var:
                    if vars.get(varStr).type != Token.INT:
                        Error(106, vars.get(varStr).name).as_string()
                    self.calculation += str(vars.get(varStr).value)
                    varStr, in_var = "", False
                else:
                    in_var = True


            elif elem == "}": 
                #varList.update({varStr: vars.get(varStr).value})
                self.calculation += str(vars.get(varStr).value)
                varStr, in_var = "", False

            elif elem.isalpha(): 
                if in_var: varStr += elem
        
        self.calculate()
        #print(f"Variables: {varList} \nCalculation: {self.calculation}")

    def calculate(self):
        # TODO: make better calculation, because very unsafe: https://stackoverflow.com/questions/9685946/math-operations-from-string
        Debug(self.name, ("calculating: %s" % self.calculation)).as_string()
        self.value = eval(self.calculation)

class Function:
    def __init__(self, name, return_func, call_const = False, function="",  value = 0):
        return_func_commands = ["RES"]

        self.name = name
        self.type = Token.FUNC # >> For Consistency
        self.const = False # >> For Consistency
        self.value = value

        self.call_const = call_const
        self.function = function
        self.MO_equation = None
        self.return_func = return_func if return_func in return_func_commands else Error(401, self.name).as_string()

    def setFunction(self, function, vars):
        Debug(self.name, ("Function set to %s" % function)).as_string()
        self.MO_equation = MathObject(name = self.name, equation=function)
        self.MO_equation.prepare(vars=vars)
        

    def call(self, vars):
        Debug(self.name, "is called").as_string()
        if not self.call_const:
            Debug(self.name, "isn't const").as_string()
            self.MO_equation.prepare(vars=vars)
            self.value = self.MO_equation.value
        else:
            Debug(self.name, "is const") .as_string()
            self.value = self.MO_equation.value

class ConditionObject:
    def __init__(self, name, condition, value = 0):
        self.name = name
        self.type = Token.CO
        self.const = False
        self.value = value
        
        self.condition = condition
        self.edit_condition = ""
        
    
    def prepare(self, vars):
        self.edit_condition = ""
        in_var = False
        varstr = ""

        "'a'>'b'"
        for elem in self.condition:
            if elem in DIGITS: Error(301, self.condition).as_string()
            elif elem == '>': self.edit_condition += elem
            elif elem == '<': self.edit_condition += elem
            elif elem == '!': self.edit_condition += elem
            elif elem == '=': self.edit_condition += elem
            elif elem == '>': self.edit_condition += elem
            elif elem == "'": 
                if in_var:
                    if vars.get(varstr).type != Token.INT:
                        Error(106, vars.get(varstr).name).as_string()
                    self.edit_condition += str(vars.get(varstr).value)
                    varstr, in_var = "", False
                    
                else:
                    in_var = True

            elif elem.isalpha(): 
                if in_var: varstr += elem

    
        self.checkCondition()
    
    def checkCondition(self):
        try:
            if eval(f"{self.edit_condition}"):
                self.value = "~1"
            else:
                self.value = "~0"
        except Exception:
            print(f"ERROR: {self.condition} is not a valid condition!")

class Loop:
    def __init__(self, name, startIndex, vars, conditionObject = None):
        self.name = name
        self.type = Token.LOOP # For consistency
        self.const = False # >> For Consistency
        self.startIndex = startIndex
        self.endIndex = False
        
        self.infinite = False
        
        if conditionObject.isalpha(): 
            self.condition = vars[conditionObject]; 
            
            self.condition.prepare(vars)
            
        elif conditionObject in BOOL:
            self.infinite = True
            
        
        self.repeat_count = 0
        
    def loopEnd(self, endIndex, vars):
        if not self.endIndex:
            self.endIndex = endIndex
        
        if self.infinite:
            if not self.repeat_count >= 65536:
                self.repeat_count += 1
                index = self.startIndex
                return index
            else:
                return endIndex  
            
        self.condition.prepare(vars)
        if self.condition.value != "~1":
            return endIndex
        
          
        index = self.startIndex
        return index

class Library:
    def __init__(self, name, libName):
        self.name = name
        self.type = Token.Lib
        self.value = 0
        
        self.libName = libName
        self.libObject = None
        
        self.setLib()
    
    def setLib(self):
        try:
            module = importlib.import_module("lib.%s" % self.libName)
            self.libObject = module

        except ImportError as e:
            Error(601, (self.libName, self.libObject)).as_string()