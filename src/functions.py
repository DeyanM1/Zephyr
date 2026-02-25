from __future__ import annotations

import importlib.util
import inspect
import os
import pickle
import platform
import random
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, TypeAlias, List

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
        errors: dict[int, Callable[..., tuple[str, str, int, type[BaseException]]]] = {
            101: lambda: (f"Unknown Base, use  '{ZBase.use}' or '{ZBase.define}'", "UnknownBase", len(cmd.name) + 2, SyntaxError),
            102: lambda: ("Undefined Variable ", "UndefinedVariable", 1, SyntaxError),
            103: lambda: ("Unknown Function.", "UnknownFunction", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            104: lambda: ("Wrong command structure. Missing ':' or ';'? ", "InvalidStructure", 1, SyntaxError),
            105: lambda: ("Variable Type doesn't match given Value ", "ValueError", 1, SyntaxError),
            106: lambda: ("Invalid Boolean type. Allowed: ~0 | ~1 ", "ValueError", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            107: lambda: ("Value cannot be changed. Variable is constant! ", "WriteProtection", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            108: lambda: ("Current Variable type doesnt support new variable type! ", "TypeError", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            109: lambda: ("List doesn't support position 0! ", "ListIndexError", len(f"{cmd.name}")+7, SyntaxError),
            110: lambda: ("Only INT, PT, FLOAT are in- and decrementable! ", "WriteError", 1, SyntaxError),
            111: lambda: ("Error in Condition/Equation. ", "ConditionError",  len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            112: lambda: ("Given variable isnt correct type!", "ParamUnsupportedTypeError", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            113: lambda: ("Given variable isnt defined!", "ParamUndefinedVariable", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            114: lambda: ("Error in arguments!", "ParamError", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            115: lambda: ("Error at jump function! Index out of range!", "JumpOutOfBounds", len("f"), SyntaxError),
            116: lambda: ("file cannot be found!", "MissingFile", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            117: lambda: ("Target file isnt a correct type!", "UnsupportedFile", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            118: lambda: ("", "", 0, SyntaxError),
            119: lambda: ("Error at Listindex. Index out of bounds", "ListOutOfBounds", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            120: lambda: ("Some Value in List doesnt match new Type", "ListTypeError", 0, SyntaxError),
            121: lambda: ("Class error! Variable doesnt have Function Registry!", "ClassMissingFunctionReg", 0, SyntaxError),
        }

        if self.code not in errors:
            raise ValueError(f"Unknown error code: {self.code}")

        message, name, offset, errorType = errors[self.code]()

        raise errorType(
            f"{Back.RED}[{self.code}] <{name}> | {message}{Back.RESET}",
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


    def checkArgs(self, count: int, raiseError: bool = True) -> bool:
        if len(self.args) < count:
            if raiseError:
                raise ZError(114)
            return False
        
        for arg in self.args:
            if arg == "":
                if raiseError:
                    raise ZError(114)
                return False
        return True

@dataclass
class ZBool:
    value: str = field(default_factory=lambda:"~0")

    lookUpTable: dict[str, bool] = field(default_factory=lambda:{
        "~0": False,
        "~1": True,
    })

    lookUpTable2: dict[bool, str] = field(default_factory=lambda:{
        False: "~0",
        True: "~1"
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


    def isFloat(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
    

    def isInt(self, s: str) -> bool:
        if s.endswith(".0") or s == "":
            core = s[:-2]
            return core.isdigit() or (core.startswith("-") and core[1:].isdigit()) or s == ""
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
        isList = False

        if rawValue.startswith("'"):
            #### REPLACE FIRST AND LAST " ' "
            varName = rawValue

            first = varName.find("'")
            last = varName.rfind("'")

            if first != -1 and last != -1 and first != last:
                varName = varName[:first] + varName[first+1:last] + varName[last+1:]
            elif first != -1:  # only one occurrence
                varName = varName[:first] + varName[first+1:]


            if varName.endswith(">"):
                varName, indexRaw = varName.split("<", 1)

                indexRaw = "".join(indexRaw.rsplit(">", 1))

                index = ZValue()
                index.setValue(indexRaw, "INT", activeVars)

                isList = True


            if isList:
                listVar: LIST = activeVars.get(varName)
                returnValue = listVar.getValue(int(index.value)).value # type: ignore

            else:
                var = activeVars.get(varName)
                if not var:
                    raise ZError(113)

                
                returnValue = var.onChange()
        
            
        
        return returnValue # type: ignore


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



def getZephyrPath() -> Path|None:
    system_os = platform.system()

    # Windows: read from registry (user-level environment variable)
    if system_os == "Windows":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key: # type: ignore
                path_str, _ = winreg.QueryValueEx(key, "ZEPHYR_LIB_PATH") # type: ignore
        except FileNotFoundError:
            return None
            #raise RuntimeError("Global environment variable ZEPHYR_LIB_PATH not found.")
    else:
        # Linux/macOS: read from shell config (~/.bashrc or ~/.zshrc)
        shell_config = Path.home() / ".bashrc"
        if os.environ.get("SHELL", "").endswith("zsh"):
            shell_config = Path.home() / ".zshrc"

        if not shell_config.exists():
            return None
            #raise RuntimeError(f"Shell config {shell_config} does not exist.")

        path_str = None
        with shell_config.open("r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("export ZEPHYR_LIB_PATH="):
                    path_str = line.split("=", 1)[1].strip().strip('"')
                    break

        if path_str is None:
            return None 
            #raise RuntimeError("Global environment variable ZEPHYR_LIB_PATH not found in shell config.")

    return Path(path_str) # type: ignore

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

        activeVars[newVar.name] = newVar
        return activeVars

    def debug(self, cmd: ZCommand, activeVars: ActiveVars):
        #pass
        print(self.value)

    
    #def __repr__(self):
    #    return f"This is {self.name}. Its a {self.varType}"

@register()
class INT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["FLOAT", "PT"]

        self.value: ZValue = ZValue()
        
        self.w(cmd, activeVars)
        
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
                self.value.setValue(cmd.args[0] if cmd.args[0] != "" else "0", self.varType, activeVars)

    
@register()
class FLOAT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "PT"]

        self.value: ZValue = ZValue()

        self.w(cmd, activeVars)

        self.registerFunc({self.w: "", self.INPUT: ""})

    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue()
        message.setValue(cmd.args[0], "PT", activeVars)
        newValue = input(message.value)
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
                self.value.setValue(cmd.args[0] if cmd.args[0] != "" else "0", self.varType, activeVars)

@register()
class PT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "FLOAT"]

        self.value: ZValue = ZValue()
        self.w(cmd, activeVars)

        self.registerFunc({self.push: "", self.w: "", self.INPUT: "", self.insertAt: ""})
    
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
        message.setValue(cmd.args[0], "PT", activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, "PT", activeVars)

    def insertAt(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 1 and cmd.args[0] != "" and cmd.args[1] != "":
            valueToInsert = ZValue()
            position = ZValue()

            valueToInsert.setValue(cmd.args[0], "PT", activeVars)
            position.setValue(cmd.args[1], "INT", activeVars)

            newValue = self.value.value[:int(position.value)-1] + valueToInsert.value + self.value.value[int(position.value)-1:]
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
                    newValue = ZValue()

                    var = activeVars.get(varName)

                    if var:
                        if var.varType == "PT":
                            newValue.value = '"' + var.value.value + '"'
                        else:
                            newValue.setValue(var.value.value, "FLOAT", activeVars)
                    else:
                        raise ZError(111)

                    self.compiledCondition += newValue.value
                    inVar = False
                    varName = ""
                    
            
            elif inVar:
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
                    newValue = ZValue()
                    var = activeVars.get(varName)
                    if var:
                        if var.varType == "PT":
                            newNewValue = ""
                            for char in var.value.value:
                                if char in MATH_ALLOWEDCHARS:
                                    newNewValue += char
                            newValue.value = newNewValue
                        else:
                            newValue.setValue(var.value.value, "FLOAT", activeVars)

                        self.compiledEquation += newValue.value

                    inVar = False
                    varName = ""
                    
            
            elif inVar:
                varName += char
                continue
            
            elif char in MATH_ALLOWEDCHARS:
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
        
    
                
        self.registerFunc({self.w: "", self.call: ""})
                
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
                    newValue = ZValue()
                    var = activeVars.get(varName)
                    if var:
                        if var.varType == "PT":
                            newNewValue = ""
                            for char in var.value.value:
                                if char in MATH_ALLOWEDCHARS:
                                    newNewValue += char
                            newValue.value = newNewValue
                        else:
                            newValue.setValue(var.value.value, "FLOAT", activeVars)

                        self.compiledEquation += newValue.value

                    inVar = False
                    varName = ""
                    
            
            elif inVar:
                varName += char
                continue
            
            elif char in MATH_ALLOWEDCHARS:
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
    

@register()
class LIST(Variable):
    def __init__(self, cmd: ZCommand, activeVars: Dict[str, Variable]) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["PT", "INT", "FLOAT"]

        self.pointer: ZValue = ZValue("1")

        self.allowedValueTypes: list[str] = ["INT", "PT", "FLOAT"]
        self.valueType: str = ""

        self.posValues: List[ZValue] = []
        self.negValues: List[ZValue] = []


        # Set Value Type
        cmd.checkArgs(1)
        self.changeValueType(cmd, activeVars)

        if cmd.checkArgs(2, False): # Set value if 2 args
            if cmd.checkArgs(3, False): # Set pointer if 3 args
                self.setPointer(cmd.args[3], activeVars) # Potentially set pointer

            self.setValue(cmd.args[0], activeVars)

        self.registerFunc({self.w: "", self.SET: "SET", self.changeValueType: "CVT"})


    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1)

        self.setValue(cmd.args[0], activeVars)

    def SET(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)

        self.setPointer(cmd.args[0], activeVars)

    def changeValueType(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)

        newType = cmd.args[0]

        match newType:
            case "PT":
                pass
            case "INT":
                for value in self.posValues:
                    if not value.isInt(value.value):
                        raise ZError(120)
                    
                for value in self.negValues:
                    if not value.isInt(value.value):
                        raise ZError(120)
            case "FLOAT":
                for value in self.posValues:
                    if not value.isFloat(value.value):
                        raise ZError(120)
                    
                for value in self.negValues:
                    if not value.isFloat(value.value):
                        raise ZError(120)
            case _:
                raise ZError(114)

        self.valueType = newType


    def onChange(self) -> str:
        return self.getValue(int(self.pointer.value)).value

    def setPointer(self, position: str, activeVars: ActiveVars):
        pointer = ZValue()
        pointer.setValue(position, "INT", activeVars)

        if int(pointer.value) == 0:
            raise ZError(109)

        self.pointer = pointer

    def setValue(self, valueRaw: str, activeVars: ActiveVars):
        if int(self.pointer.value) > 0:
            pointer = int(self.pointer.value) -1

            value = ZValue()
            #print(valueRaw)
            value.setValue(valueRaw, self.valueType, activeVars)

            while len(self.posValues) <= pointer:
                self.posValues.append(ZValue(""))

            self.posValues[pointer] = value

        elif int(self.pointer.value) < 0:
            pointer = abs(int(self.pointer.value)) -1
            value = ZValue()
            value.setValue(valueRaw, self.valueType, activeVars)

            while len(self.negValues) <= pointer:
                self.negValues.append(ZValue(""))

            self.negValues[pointer] = value

    def getValue(self, index: int):
        if index > 0:
            try:
                return self.posValues[index-1]
            except IndexError:
                raise ZError(119)
        elif index < 0:
            try:
                return self.negValues[abs(index)-1] 
            except IndexError:
                raise ZError(119)
        else:
            raise ZError(109)


 

    def debug(self, cmd: ZCommand, activeVars: ActiveVars):
        print(self.posValues, "\n", self.negValues)

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
            userPath = ZValue()
            userPath.setValue(cmd.args[0], "PT", activeVars)
            userPath = Path(userPath.value)


            foundGlobalPath = False
            path = Path()
            module_name = ""

            ### Check for global
            globalPath = getZephyrPath()
            if globalPath is not None:
                foundGlobalPath = True
                globalPath = globalPath / userPath

                globalPath = globalPath.resolve()

                if globalPath.suffix != ".py":
                    raise ZError(117)

                module_name = globalPath.stem
                path = globalPath


            ## Check for cwd path

            localPath = userPath
            
            if not localPath.is_absolute():
                localPath = localPath.cwd() / userPath

            localPath = localPath.resolve()

            if localPath.exists():
                if localPath.suffix == ".py":
                    module_name = localPath.stem

                    path = localPath

                elif not foundGlobalPath:
                    raise ZError(117)
                
            elif not foundGlobalPath:
                raise ZError(116)

            if module_name and path:
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Failed to create spec for {path}")

                self.module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = self.module
                spec.loader.exec_module(self.module)

            
                newTypes: dict[str, type] = self.module.load()   
                
                for name, cls in newTypes.items():
                    register(name)(cls)
            else:
                raise ZError(117)


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