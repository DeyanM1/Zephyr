import re
int_reg = "^\d+$" #"^\*\d*\*$"
PT_reg = "^'.*'$"




class INT:
    def __init__(self):
        pass

class PT:
    def __init__(self):
        pass


def check_type_value(type, value):

    match type:
        case "INT" | INT.__class__:
            if not re.search(int_reg, value):
                return False
            return INT
        case "PT" | PT.__class__:
            #if not re.search(PT_reg, value):
            #    return False
            return PT
        
        case _:
            return False
        
def check_existance(vars, name):
    if name not in vars.keys():
        print(f"ERROR: Unknown variable | Name: {name}")
        quit()

def assign_type(type):
    match type:
        case "INT": return INT
        case "PT": return PT



class Error:
    def __init__(self, exception_code:int, details):
        self.exception_code = exception_code
        self.details = details
    
    def as_string(self):
        match self.exception_code:
            case 101: return "ERROR: Value not accepted   | Variable: %s" % self.details
            case 102: return "ERROR: Variable is constant | Variable: %s" % self.details
            case 103: return "ERROR: Result Variable must be int or float | Variable: %s" % self.details
            case 201: return "ERROR: Unknown Function | Name: %s" % self.details

class Variable:
    def __init__(self, name, type, value, const = False):
        self.name = name
        if check_type_value(type, value) :
            check_type_value(type, value)
        else:
            print(Error(101, self.name).as_string())
            quit() 
        self.value = value
        self.const = const
        self.message = ""
        #print("Declaration")

    def change_type(self, type):
        if self.const:
            return False
        
        self.type = assign_type(type)
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
            print(Error(101, self.name).as_string())
            quit()
        if self.type != "INT" or self.type != "FLOAT":
            print(Error(103, f"{self.name} is {self.type}").as_string())
            quit()

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
    def __init__(self, message):
        self.message = message
        
    def print(self):
        return self.message.replace("'", "")