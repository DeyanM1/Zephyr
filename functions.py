import re
int_reg = "^\d+$" #"^\*\d*\*$"
PT_reg = "^'.*'$"


TT_INT = "TT_INT"
TT_FLOAT = "TT_FLOAT"

TYPES = ["INT", "FLOAT", "PT"]

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
            case 201: print("ERROR: Unknown Function | Name: %s" % self.details)
        quit()


def check_type_value(type, value):
    #if value is Token.__class__:
    #    pass
    #else:
    match type:
        case "INT" | Token.INT:
            if not re.search(int_reg, value):
                return False
            return Token.INT
        case "PT" | Token.PT:
            #if not re.search(PT_reg, value):
            #    return False
            return Token.PT
        case _:
            return False
        
def check_existance(vars, name):
    if name not in vars.keys():
        Error(105, name).as_string()

def assign_type(type):
    match type:
        case "INT": return Token.INT
        case "PT": return Token.PT




class Variable:
    def __init__(self, name, type, value, const = False):
        self.name = name
        if check_type_value(type, value) :
            self.type = assign_type(type)
        else:
            Error(101, self.name).as_string()
        self.value = value
        self.const = const
        self.message = ""
        #print("Declaration")

    def change_type(self, vars, type):
        check_existance(vars, self.name)

        if self.const:
            return False
        
        if not type in TYPES:
            Error(106, type).as_string() 
        
        if check_type_value(type, self.value):
            self.type = assign_type(type)
        else:
            Error(101, self.name).as_string()

        return True
    
    def get_type(self):
        return self.type

    def change_value(self, value):
        if self.const:
            return False
        
        self.value = value
        return True
    
    def Push(self):
        return


    def math(self, operator, values: list):
        if self.const:
            Error(101, self.name).as_string()
        if self.type != "INT" or self.type != "FLOAT":
            Error(103, f"{self.name} is {self.type}").as_string()

        match operator:
            case "+":
                result = 0
                for elem in values:
                    result += values[elem]
                self.value = result
                
                return True
        
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

    



class Push():
    def __init__(self, vars, name):
        self.var = vars.get(name)

        self.name = name
        self.type = self.var.type
        self.message = self.var.value
        self.prepare()
    
    def prepare(self):
        if self.type != Token.PT:
            Error(104, self.name).as_string()
        return True
        
    def get(self):
        return self.message

    def print(self):
        if self.prepare():
            print(self.message)