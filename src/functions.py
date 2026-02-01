from __future__ import annotations

import importlib.util
import inspect
import pickle
import random
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, TypeAlias

from colorama import Back

typeRegistry: dict[str, type] = {}


ActiveVars: TypeAlias = dict[str, "Variable"]
ZIndex: TypeAlias = int

MATH_ALLOWEDCHARS: str = "+-*/%=()1234567890."
CO_ALLOWEDCHARS: str = "()=!><1234567890."


class ZError(Exception):
    def __init__(self, code: int) -> None:
        self.code = code
    
    def process(self, cmd: ZCommand, zfile: ZFile) -> None:
        path: Path = zfile.zphPath
        context: str = path.read_text().splitlines()[cmd.lineNum - 1]

        # errorCode: (message, offset_function)
        errors: dict[int, Callable[..., tuple[str, int, type[BaseException]]]] = {
            101: lambda: (f"[101]  Unknown Base, use  '{ZBase.use}' or '{ZBase.define}'", len(cmd.name) + 2, SyntaxError),
            102: lambda: ("[102]  Undefined Variable ", 1, SyntaxError),
            103: lambda: ("[103]  Unknown Function. Maybe your type is wrong?", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            104: lambda: ("[104]  Wrong command structure. Missing ':' or ';'? ", 1, SyntaxError),
            105: lambda: ("[105]  Variable Type doesn't match given Value ", 1, SyntaxError),
            106: lambda: ("[106]  Invalid Boolean type. Allowed: b0 | b1 ", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            107: lambda: ("[107]  Value cannot be changed. Variable is constant! ", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            108: lambda: ("[108]  Current Variable type doesnt support new variable type! ", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            109: lambda: (f"[109]  List ({cmd.name}) doesn't support position 0! ", len(f"{cmd.name}")+7, SyntaxError),
            110: lambda: ("[110]  Only INT, PT, FLOAT are in- and decrementable! ", 1, SyntaxError),
            111: lambda: ("[111]  Error in Condition. ", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            112: lambda: ("[112] Given variable isnt correct type!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            113: lambda: ("[113] Given variable isnt defined!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            114: lambda: ("[114] Error in arguments!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            115: lambda: ("[115] Error at jump function! Index out of range!", len("f"), SyntaxError),
            116: lambda: ("[116] file cannot be found!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            117: lambda: ("[117] Target file isnt a correct type!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
        }

        if self.code not in errors:
            raise ValueError(f"Unknown error code: {self.code}")

        message, offset, errorType = errors[self.code]()

        raise errorType(
            f"{Back.RED}{message}{Back.RESET}",
            (str(path), cmd.lineNum, offset, context)
        )



@dataclass
class ZFile:
    """
    Represents a Zephyr file with automatically computed paths for
    .zph, .zsrc, and .zpkg files. Accepts relative or absolute paths
    with or without the .zph extension.
    """
    
    path: Path = field(default_factory=Path)
    
    zphPath: Path = field(init=False)
    zsrcPath: Path = field(init=False)
    zpkgPath: Path = field(init=False)
    rawName: str = field(init=False)
    
    def __post_init__(self):
        self.path = Path(self.path).expanduser().resolve() # Convert to absolute path

        if self.path.suffix == ".zph":
            self.zphPath = self.path
        else:
            self.zphPath = self.path.with_suffix(".zph")


        # create other paths from the base path
        self.rawName = self.zphPath.stem
        self.zsrcPath = self.zphPath.with_suffix(".zsrc")
        self.zpkgPath = self.zphPath.with_suffix(".zpkg")

    """@classmethod
    def from_json(cls, data: Dict[str, Any]) -> "ZFile":
        raw: str = data.get("rawName", "")
        base: Optional[str] = data.get("basePath")
        base_path: Optional[Path] = Path(base) if base else None

        obj: "ZFile" = cls(rawName=raw, basePath=base_path)

        if "zphPath" in data:
            obj.zphPath = Path(data["zphPath"])
        if "zsrcPath" in data:
            obj.zsrcPath = Path(data["zsrcPath"])
        if "zpkgPath" in data:
            obj.zpkgPath = Path(data["zpkgPath"])

        return obj"""

@dataclass
class ZBase:
    define: str = "#"
    use: str = "?"

@dataclass
class ZCommand:
    """
    Represents a parsed command from a .zph file.

    Attributes:
        lineNum (int): The line number in the .zph file where the command is located.
        name (str): The name of the command.
        base (str): The base of the command.
        func (str): The function specified by the command.
        args (list[str]): The arguments provided to the command.
    """
    lineNum: int
    name: str
    base: str
    func: str
    args: list[str]

@dataclass
class ZBool:
    value: str = field(default_factory=lambda:"b0")

    lookUpTable: dict[str, bool] = field(default_factory=lambda:{
        "b0": False,
        "b1": True,
    })

    lookUpTable2: dict[bool, str] = field(default_factory=lambda:{
        False: "b0",
        True: "b1"
    })



    @property
    def compiledValue(self) -> bool:
        return self.lookUpTable[self.value]

    def setCompileValue(self, newRawValue: bool) -> None:
        "This function takes a Python bool converts it into ZBool and sets it to current value"
        newValue = self.lookUpTable2[newRawValue]
        self.setValue(newValue)

    def getZBool(self) -> str:
        """Returns the current value in ZBool format"""
        return self.value
    def getBool(self) -> bool:
        """Returns the current value in Python Bool format"""
        return self.lookUpTable[self.value]


    def setValue(self, value: str) -> None:
        if value not in self.lookUpTable:
            raise ZError(106)
        self.value = value

@dataclass
class ZValue:
    value: str = ""

    def supportedTypes(self, value: str) -> dict[str, bool]:
        return {
            "PT": True,
            "INT": self.isInt(value),
            "FLOAT": self.isFloat(value),

        }

    @staticmethod
    def isFloat(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def isInt(s: str) -> bool:
        if s.endswith(".0"):
            core = s[:-2]
            return core.isdigit() or (core.startswith("-") and core[1:].isdigit())
        return s.isdigit() or (s.startswith("-") and s[1:].isdigit())

    def setValue(self, newValue: str, targetType: str, activeVars: ActiveVars) -> None:
        compiledValue = self.compileValue(newValue, activeVars)
        try:
            if not self.supportedTypes(compiledValue)[targetType]:
                raise ZError(105)
        except KeyError:
            pass
            
        self.value = compiledValue

    def compileValue(self, rawValue: str, activeVars: ActiveVars) -> str:
        # This function ignores the type of the variable!
        # This function returns the raw Value
        returnValue: str = rawValue

        if rawValue.startswith("'"):
            varName = rawValue.replace("'", "")

            var = activeVars.get(varName)
            if not var:
                raise ZError(113)
            
            returnValue = var.onChange()
        
        return returnValue


    def getValueIfVarType(self, targetType: str) -> str|bool:
        # Return value if current Value is supported by target Type
        if self.supportedTypes(self.value)[targetType]:
            return self.value
        else:
            return False

    def increment(self, incrementValueRaw: str, currentType: str, activeVars: ActiveVars) -> None:
        if not self.supportedTypes(incrementValueRaw)[currentType]:
            raise ZError(105)
        
        # Long and complicated statement. Dont know what it does#
        if currentType == "PT":
            if incrementValueRaw == "":
                incrementValueRaw = "1"

            incrementValue = ZValue()
            incrementValue.setValue(incrementValueRaw, "PT", activeVars)

            
            
            self.value = f"{self.value}{incrementValue.value}"

            #self.setValue(self.value + (self.value)*int(incrementValue), currentType, activeVars)



        else:
            newValue = float(self.value) + float(incrementValueRaw)
            if currentType == "INT":
                self.setValue(str(newValue).split(".")[0], currentType, activeVars)
            elif currentType == "FLOAT":
                self.setValue(str(newValue), currentType, activeVars)
            else:
                raise ZError(110)

    def decrement(self, decrementValue: str, currentType: str, activeVars: ActiveVars) -> None:
        if not self.supportedTypes(decrementValue)[currentType]:
            raise ZError(105)

        if currentType == "PT":
            self.setValue("", currentType, activeVars)

        else:
            newValue = float(self.value) - float(decrementValue)
            if currentType == "INT":
                self.setValue(str(newValue).split(".")[0], currentType, activeVars)
            elif currentType == "FLOAT":
                self.setValue(str(newValue), currentType, activeVars)
            else:
                raise ZError(110)



def getRequiredArgs(function: Callable[..., Any]):
    sig = inspect.signature(function)
    params = sig.parameters

    required_args = [
        name for name, param in params.items()
        if param.default == inspect.Parameter.empty
    ]
    return required_args

def register(name: str = ""):
    def wrapper(cls: type):
        typeRegistry[name or cls.__name__] = cls
        return cls
    return wrapper




class Variable:
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.varType = cmd.func
        self.name = cmd.name

        self.value: Any


        self.supportedVars: list[str] = [] # Supported Variables to change to

        self.functionRegistry: dict[str, Callable[..., Any]] = {}
        self.registerFunc({self.CT: "", self.debug: ""})


    def registerFunc(self, funcList: dict[Callable[..., Any], str]) -> None:
        """
        Register a function for a type. Its added to the functionRegistry

        Args:
            func (Callable[..., Any]): The function to generate the docstring for.
            name (Optional[str]): The name to use in the docstring. If not provided, the function's name will be used.

        """
        for func, name in funcList.items():
            if name:
                self.functionRegistry[name] = func
            else:
                self.functionRegistry[func.__name__] = func
    
    def onChange(self) -> str:
        """
        Returns the value that is being used for typechanging
        """
        return self.value.value
        
    def CT(self, cmd: ZCommand, activeVars: ActiveVars) -> ActiveVars:
        targetVarType: str = cmd.args[0]

        if targetVarType not in self.supportedVars:
            raise ZError(108)

        targetVarType: str = cmd.args[0]

        oldVar: Variable = activeVars[cmd.name]


        newVarCmd: ZCommand = ZCommand(cmd.lineNum, cmd.name, ZBase.define, targetVarType, [oldVar.onChange()])
        newVar = typeRegistry[targetVarType](newVarCmd, activeVars)

        activeVars.update({newVar.name: newVar})

        return activeVars

    def debug(self, cmd: ZCommand, activeVars: ActiveVars):
        pass
        #print(self.value)

    
    #def __repr__(self):
    #    return f"This is {self.name}. Its a {self.varType}"

@register()
class INT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["FLOAT", "PT"]

        self.value: ZValue = ZValue()
        self.value.setValue(cmd.args[0], self.varType, activeVars)
        
        self.registerFunc({self.w: "", self.INPUT: ""})

    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue()
        message.setValue(cmd.args[0], "PT", activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, "INT", activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """        if self.const.compiledValue:
                    raise ZError(107)
        """

        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)

            case _:
                self.value.setValue(cmd.args[0], self.varType, activeVars)

@register()
class FLOAT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "PT"]

        self.value: ZValue = ZValue()
        self.value.setValue(cmd.args[0], self.varType, activeVars)

        self.registerFunc({self.w: "", self.INPUT: ""})

    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue()
        newValue = input(message.setValue(cmd.args[0], "PT", activeVars))
        self.value.setValue(newValue, "FLOAT", activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """if self.const.compiledValue:
            raise ZError(107)"""


        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)

            case _:
                self.value.setValue(cmd.args[0], self.varType, activeVars)

@register()
class PT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "FLOAT"]

        self.value: ZValue = ZValue()
        self.value.setValue(cmd.args[0], self.varType, activeVars)

        self.registerFunc({self.push: "", self.w: "", self.INPUT: ""})
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """if self.const.compiledValue:
            raise ZError(107)"""


        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)

            case _:
                self.value.setValue(cmd.args[0], self.varType, activeVars)
    
    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue()
        newValue = input(message.setValue(cmd.args[0], "PT", activeVars))
        self.value.setValue(newValue, "PT", activeVars)
        
    def push(self, cmd: ZCommand) -> None:
        print(self.value.value)

@register()
class CO(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT"]

        self.value: ZBool = ZBool()
        self.rawCondition: ZValue = ZValue()
        self.compiledCondition: str = ""


        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.w(cmd, activeVars)



        self.registerFunc({self.w: ""})

        
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.rawCondition.setValue(cmd.args[0], "PT", activeVars)
        self.compile(activeVars)

    
    def compile(self, activeVars: ActiveVars) -> None:
        self.compiledCondition = ""
        inVar = False
        varName = ""
        
        for char in self.rawCondition.value:
            if char == "'":
                if not inVar:
                    inVar = True
                    
                else:
                    varValue = ZValue()
                    varValue.setValue(varName, "FLOAT", activeVars)
                    self.compiledCondition += varValue.value
                    inVar = False
                    varName = ""
                    
            
            if inVar:
                varName += char
                continue
            
            if char in CO_ALLOWEDCHARS:
                self.compiledCondition += char

        self.evaluate()

    
    def evaluate(self) -> None:
        result: bool = False

        try:
            result = eval(self.compiledCondition)
        except Exception: 
            raise ZError(111)
        
        self.value.setCompileValue(result)

    def onChange(self) -> str:
        return self.value.value

@register()
class IF(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = []

        self.value: ZValue = ZValue()


        self.conditionalObjectName: ZValue = ZValue()
        self.conditionalObjectValue: ZBool = ZBool()

        self.countCommandsInIf: ZValue = ZValue()
        self.countCommandsInElif: ZValue = ZValue()
        

        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.w(cmd, activeVars) # Set if optional conditionObjectName is set
            
        self.registerFunc({self.START: "", self.ELSE: "", self.END: "", self.w: ""})


    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        if len(cmd.args) > 0:
            self.conditionalObjectName.setValue(cmd.args[0], "PT", activeVars)
            conditionalObject = activeVars.get(self.conditionalObjectName.value)

            if isinstance(conditionalObject, CO):
                self.conditionalObjectValue = conditionalObject.value # type: ignore
            else:
                raise ZError(112)
        else:
            raise ZError(114)
  
    
    def START(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.countCommandsInIf.setValue(cmd.args[0], "INT", activeVars)
        else:
            raise ZError(114)
        
        newIndex: ZIndex = 0
        if self.conditionalObjectValue.getBool():
            newIndex = index
        elif not self.conditionalObjectValue.getBool():
            newIndex = index + int(self.countCommandsInIf.value)
        
        return activeVars, newIndex

    def ELSE(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        self.countCommandsInElif.setValue(cmd.args[0], "INT", activeVars)
        newIndex: ZIndex = 0
        if not self.conditionalObjectValue.getBool():
            newIndex = index
        elif self.conditionalObjectValue.getBool():
            newIndex = index + int(self.countCommandsInElif.value)
        
        return activeVars, newIndex

    def END(self, cmd: ZCommand):
        pass

@register()
class MO(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["PT", "INT", "FLOAT"]

        self.value: ZValue = ZValue()
        self.rawEquation: ZValue = ZValue()
        self.compiledEquation: str = ""

        if len(cmd.args) > 0:
            if cmd.args[0] != "":
                self.w(cmd, activeVars)
        
        self.registerFunc({self.w: ""})

    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.rawEquation.setValue(cmd.args[0], "PT", activeVars)
        self.compile(activeVars)
    
    def compile(self, activeVars: ActiveVars) -> None:
        self.compiledEquation = ""
        inVar = False
        varName = ""

        for char in self.rawEquation.value:
            if char == "'":
                if not inVar:
                    inVar = True
                    
                else:
                    varValue = ZValue()
                    varValue.setValue(varName, "FLOAT", activeVars)
                    self.compiledEquation += varValue.value

                    inVar = False
                    varName = ""
                    
            
            if inVar:
                varName += char
                continue
            
            if char in MATH_ALLOWEDCHARS:
                self.compiledEquation += char

        self.calculate(activeVars)
    
    def calculate(self, activeVars: ActiveVars) -> None:
        result: float = 0

        try:
            result = eval(self.compiledEquation)
        except Exception: 
            raise ZError(111)
        
        self.value.setValue(str(result), "FLOAT", activeVars)

@register()
class FUNC(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "PT", "FLOAT"]


        self.returnType: str = ""
        self.disableVariableChange: ZBool = ZBool()

        self.value: ZValue = ZValue("0")
        self.rawEquation: str = ""
        self.compiledEquation: str = ""

        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.returnType = cmd.args[0]
        if len(cmd.args) > 1 and cmd.args[1] != "":
            self.disableVariableChange.setValue(cmd.args[1])
        if len(cmd.args) > 2 and cmd.args[2]:
            mathObject: MO = activeVars.get(cmd.args[2])
            if not mathObject:
                raise ZError(113)
            if isinstance(mathObject, MO):
                self.rawEquation = mathObject.rawEquation.value # type: ignore
            else:
                raise ZError(112)

            self.autoCall(activeVars)
        
    
                
        self.registerFunc({self.w: "", self.call: "call"})
                
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        moName = ZValue()
        moName.setValue(cmd.args[0], "PT", activeVars)
        mathObject: MO = activeVars.get(moName.value)
        if not mathObject:
            raise ZError(113)
        if isinstance(mathObject, MO):
            self.rawEquation = mathObject.rawEquation.value # type: ignore
        else:
            raise ZError(112)

        self.autoCall(activeVars)

    
    def autoCall(self, activeVars: ActiveVars) -> None:
        """This function is called after the equation is set and calculates the equation if diasbleVariableChange is True
           The normal call function is the one called using    fun ? call:;
        """
        if self.disableVariableChange.getBool():
            self.compile(activeVars)
    
    def call(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if not self.disableVariableChange.getBool():
            self.compile(activeVars)
        
    def compile(self, activeVars: ActiveVars) -> None:
        self.compiledEquation = ""
        inVar = False
        varName = ""

        for char in self.rawEquation:
            if char == "'":
                if not inVar:
                    inVar = True
                    
                else:
                    varValue = ZValue()
                    varValue.setValue(varName, "FLOAT", activeVars)
                    self.compiledEquation += varValue.value
                    inVar = False
                    varName = ""
                    
            
            if inVar:
                varName += char
                continue
            
            if char in MATH_ALLOWEDCHARS:
                self.compiledEquation += char

        self.calculate(activeVars)
    
    def calculate(self, activeVars: ActiveVars) -> None:
        result: float = 0

        try:
            result = eval(self.compiledEquation)
        except Exception: 
            raise ZError(111)
        
        self.value.setValue(str(result), "FLOAT", activeVars)

@register()
class RNG(Variable):
    def __init__(self, cmd: ZCommand, activeVars: Dict[str, Variable]) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT"]


        self.value: ZValue = ZValue()

        self.randomNumberType: ZValue = ZValue()
        self.allowedTypes: list[str] = ["INT", "FLOAT"]
        self.rangeMin: ZValue = ZValue()
        self.rangeMax: ZValue = ZValue()

        if len(cmd.args) > 2 and cmd.args[0] != "" and cmd.args[1] != "" and cmd.args[2] != "":
            self.w(cmd, activeVars)
        
        self.registerFunc({self.w: ""})

    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        # Check if all arguments are available
        if not len(cmd.args) > 2 or cmd.args[0] == "" or cmd.args[1] == "" or cmd.args[2] == "":
            raise ZError(114)
        

        self.randomNumberType.setValue(cmd.args[2], "PT", activeVars)
        if self.randomNumberType.value not in self.allowedTypes:
            print("HO")
            raise ZError(114)


        self.rangeMin.setValue(cmd.args[0], self.randomNumberType.value, activeVars)
        self.rangeMax.setValue(cmd.args[1], self.randomNumberType.value, activeVars)

        self.generate(activeVars)

    def generate(self, activeVars: ActiveVars):
        newValue = 0
        match self.randomNumberType.value:
            case "INT":
                newValue = random.randint(int(self.rangeMin.value), int(self.rangeMax.value))
            case "FLOAT":
                newValue = random.uniform(float(self.rangeMin.value), float(self.rangeMax.value))
            case _:
                pass

        self.value.setValue(str(newValue), self.randomNumberType.value, activeVars)

@register()
class LOOP(Variable):
    def __init__(self, cmd: ZCommand, activeVars: Dict[str, Variable], index: ZIndex) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT"]

        self.startIndex: ZIndex = index
        self.countCommandsInLoop: ZValue = ZValue()
        self.active: bool = False
        self.countLooped: int = 1

        self.conditionalObjectName: ZValue = ZValue()
        self.conditionalObject: CO
        


        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.w(cmd, activeVars)
        
        self.registerFunc({self.w: "", self.START: "", self.END: ""})

    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.conditionalObjectName.setValue(cmd.args[0], "PT", activeVars)

            self.conditionalObject: CO = activeVars.get(self.conditionalObjectName.value)

            if isinstance(self.conditionalObject, CO): # type: ignore
                self.conditionalObjectValue = self.conditionalObject.value # type: ignore
            else:
                raise ZError(112)
        else:
            raise ZError(114)
        
        self.checkCondition(activeVars)
        
    def checkCondition(self, activeVars: ActiveVars):
        self.conditionalObject.compile(activeVars) # type: ignore
        if self.conditionalObject.value.getBool(): # type: ignore
            self.active = True
        else:
            self.active = False



    def START(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex):
        self.startIndex = index

        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.countCommandsInLoop.setValue(cmd.args[0], "INT", activeVars)
        else:
            raise ZError(114)


        self.checkCondition(activeVars)
        if not self.active:
            return activeVars, self.startIndex + int(self.countCommandsInLoop.value)
        
        
        return activeVars, index

    def END(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex):
        self.checkCondition(activeVars)

        if self.active:
            self.countLooped += 1
            return activeVars, self.startIndex
        else:
            return activeVars, index

    def onChange(self) -> str:
        return str(self.countLooped)


@register()
class FILE(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = []

        self.value: ZValue = ZValue()

        self.path: Path = Path()


        if len(cmd.args) > 0:
            self.w(cmd, activeVars)
        

        self.registerFunc({self.w: ""})
        self.registerFunc({self.cSET: "", self.cFLUSH: ""})
        self.registerFunc({self.gRENAME: "", self.gDEL: ""})

    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """
        Only sets the filePath
        
        """
        if len(cmd.args) > 0 and cmd.args[0] == "":
            self.path = Path.cwd() / "unnamed_file.txt"

        elif len(cmd.args) > 0 and cmd.args[0] != "":
            rawPath = ZValue()
            rawPath.setValue(cmd.args[0], "PT", activeVars)
            path = Path(rawPath.value)

            if not path.is_absolute():
                path = (Path.cwd() / path).resolve()
            
            self.path = path
        
        else:
            raise ZError(114)


        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

        self.value.value = self.path.as_posix()


    def cSET(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) < 0 and cmd.args[0] == "":
            raise ZError(14)
        
        text = ZValue()
        text.setValue(cmd.args[0], "PT", activeVars)

        with self.path.open("w") as openFile:
            openFile.write(text.value)

    def cFLUSH(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        with self.path.open("w"):
            pass

    def gRENAME(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            newName = ZValue()
            newName.setValue(cmd.args[0], "PT", activeVars)
            self.path.rename(newName.value)
        else:
            raise ZError(114)

    def gDEL(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.path.unlink()

    def onChange(self) -> str:
        ret = ""
        with self.path.open("r") as openFile:
            ret = openFile.readlines()
        
        return str(*ret)
    


@register(name="__")
class BUILD_IN(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars, zfile: ZFile) -> None:
        super().__init__(cmd, activeVars)

        self.zfile: ZFile = zfile

        self.registerFunc({self.wait: "", self.jump: "", self.jumpTo: "", self.export: "", self.load: "", self.LIB: ""})

    
    def wait(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        waitTime: ZValue = ZValue()
        waitTime.setValue(cmd.args[0], "FLOAT", activeVars)

        time.sleep(float(waitTime.value))

    def jump(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex] :
        indexToAdd: ZValue = ZValue()
        if len(cmd.args[0]):
            if cmd.args[0] == "":
                raise ZError(114)
            
            indexToAdd.setValue(cmd.args[0], "INT", activeVars)

            if indexToAdd.value.startswith("-"):
                return activeVars, ZIndex(index-int(indexToAdd.value.replace("-", ""))-1)
            else:
                return activeVars, ZIndex(index+(int(indexToAdd.value)))

        raise ZError(114)
    
    def jumpTo(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        indexToJump: ZValue = ZValue()
        if len(cmd.args[0]):
            if cmd.args[0] == "":
                raise ZError(114)
            
            indexToJump.setValue(cmd.args[0], "INT", activeVars)

            return activeVars, int(indexToJump.value)-2

        raise ZError(114)
 

    def LIB(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args[0]) > 0 and cmd.args[0] != "":
            path = Path(cmd.args[0])

            if not path.is_absolute():
                path = Path.cwd() / path

            path = path.resolve()

            if not path.exists():
                raise ZError(116)

            if path.suffix != ".py":
                raise ZError(117)

            module_name = path.stem

            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Failed to create spec for {path}")

            self.module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = self.module
            spec.loader.exec_module(self.module)

            
            newTypes: dict[str, type] = self.module.load()   
            
            for name, cls in newTypes.items():
                register(name)(cls)


    def export(self, cmd: ZCommand, activeVars: ActiveVars):
        if len(cmd.args) > 0 and cmd.args[0] != "":
            fileName = ZValue()
            fileName.setValue(cmd.args[0], "PT", activeVars)

            zfile = ZFile(Path(fileName.value))

            zfile.zphPath.parent.mkdir(parents=True, exist_ok=True)

            with zfile.zpkgPath.open("wb") as f:
                pickle.dump(activeVars, f)
        else:
            with self.zfile.zpkgPath.open("wb") as f:
                pickle.dump(activeVars, f)

    def load(self, cmd: ZCommand, activeVars: ActiveVars) -> ActiveVars:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            fileName = ZValue()
            fileName.setValue(cmd.args[0], "PT", activeVars)

            zfile = ZFile(Path(fileName.value))

            if not zfile.zphPath.is_file():
                raise ZError(116)
            
            with zfile.zpkgPath.open("rb") as f:
                newActiveVars = pickle.load(f)

        else:
            with self.zfile.zpkgPath.open("rb") as f:
                newActiveVars = pickle.load(f)


        return activeVars|newActiveVars



if __name__ == "__main__":
    import subprocess
    subprocess.call(["python3", "src/main.py"])