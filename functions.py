import re
int_reg = "^\d+$"
PT_reg = "^'.*'$"

DEBUG = False

global DIGITS; DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
global TYPES; TYPES = ["INT", "PT", "MO", "FUNC", "LOOP", "CO"]
global BOOL; BOOL = ["~1", "~0"]
global CONDITIONS; CONDITIONS = [">", "<", "==", "!=", ">=", "<="]
global TRANSLATE_BOOL; TRANSLATE_BOOL = {"~1":"True", "~0":"False"}

class Token:
    def __init__(self, type_):
        self.type = assign_type(type_) if assign_type(type_) else Error(105, type_).as_string()
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
        quit()

class Debug:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def as_string(self):
        if DEBUG:
            print(f"{self.name}: {self.description}")

def search(code, vars, libs):
    comm, params = code.split(":")
    paramsList = params.split("|")

    name, func, base = comm.split(" ")
    name, base = name.replace(" ", ""), base.replace(" ", "")



def check_type_value(type, value):
    match type:
        case "INT" | Token.INT:
            if not re.search(int_reg, value):
                return False
            return Token.INT
        case "PT" | Token.PT:
            # if not re.search(PT_reg, value):
            #    return False
            return Token.PT
        case _:
            return False
        
def check_existence(vars, name):
    if name not in vars.keys():
        Error(105, name).as_string()

def assign_type(type):
    match type:
        case "INT": return Token.INT
        case "PT": return Token.PT
        case "MO": return Token.MO

def change_type(var, vars, newType):
    check_existence(vars, var.name)

    if not newType in TYPES:
        Error(106, newType).as_string() 

    if var.const:
        Error(102, var.name).as_string()

    if var.type == Token.MO or var.type == Token.FUNC:
        #print("type", assign_type(newType))
        Debug(var.name, f"{var.type} set to: {newType}").as_string()
        vars.update({var.name: Variable(name=var.name, type=newType, value=var.value, const=var.const)})
        

    elif check_type_value(newType, var.value):
        Debug(var.name, f"{var.type} set to: {newType}").as_string()
        var.type = assign_type(newType)
    else:
        Error(107, newType).as_string()

    return vars


def Push(var):
        if var.type != Token.PT:
            Error(104, var.name).as_string()
        print("PUSH: ", var.value)



class Variable:
    def __init__(self, name, type, value, const = False):
        self.name = name
        self.type = assign_type(type) if check_type_value(type, value) else Error(101, self.name).as_string()
        self.value = value
        self.const = const

    def change_type(self, vars, newType):
        check_existence(vars, self.name)

        if self.const:
            Error(102, self.name).as_string()
        
        if not newType in TYPES:
            Error(106, newType).as_string() 
        
        if check_type_value(newType, self.value):
            self.type = assign_type(newType)
        else:
            Error(107, newType).as_string()

        return True
    
    def get_type(self):
        return self.type

    def change_value(self, value):
        if self.const:
            return False
        
        if value == "++":
            self.value = str(int(self.value) + 1)
        else:  
            if check_type_value(self.type, value):
                self.value = value
            else:
                Error(101, self.name).as_string()	

        return True


class MathObject:
    def __init__(self, name, value = 0, equation = ()):
        self.name = name
        self.type = Token.MO  # >> For Consistency
        self.const = False # >> For Consistency
        self.value = value

        self.equation = equation
        self.calculation = ""


    
    def set_equation(self, equation):
        Debug(self.name, "equation set to %s" % equation)
        self.equation = equation

    def prepare(self, vars):
        Debug(self.name, "prepare with calculation: %s" % self.calculation).as_string()

        self.calculation = ""
        in_var = False
        varstr = ""


        
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
                    if vars.get(varstr).type != Token.INT:
                        Error(106, vars.get(varstr).name).as_string()
                    self.calculation += str(vars.get(varstr).value)
                    varstr, in_var = "", False
                else:
                    in_var = True


            elif elem == "}": 
                #varList.update({varstr: vars.get(varstr).value})
                self.calculation += str(vars.get(varstr).value)
                varstr, in_var = "", False

            elif elem.isalpha(): 
                if in_var: varstr += elem
        
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

    def set_function(self, function, vars):
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

    
        self.check_condition()
    
    def check_condition(self):
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
        
    def END(self, endIndex, vars):
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
    def __init__(self, name, lib_name):
        self.name = name
        self.type = Token.Lib
        self.lib_name = lib_name
    
    def search(self):
        pass

"""
class MATH_LEXER:
    def __init__(self, equation):
        self.current_char = None
        self.pos = -1
        self.equation = equation
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.equation[self.pos] if self.pos < len(self.equation) else None 
    
    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in '\t':
                self.advance
"""