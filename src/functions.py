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
from typing import Any, Callable, List, TypeAlias, Literal

from colorama import Back

typeRegistry: dict[str, type] = {}


ActiveVars: TypeAlias = dict[str, "Variable"]
ZIndex: TypeAlias = int

MATH_ALLOWEDCHARS: str = "+-*/%=()1234567890."
CO_ALLOWEDCHARS: str = "()=!><1234567890.~"


class ZError(Exception):
    def __init__(self, code: int) -> None:
        self.code = code
    
    def process(self, cmd: ZCommand, zfile: ZFile, exit: bool = True) -> None:
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
            118: lambda: ("Error at first line of .zph file", "SyntaxError", 0, SyntaxError),
            119: lambda: ("Error at Listindex. Index out of bounds", "ListOutOfBounds", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            120: lambda: ("Some Value in List doesnt match new Type", "ListTypeError", 0, SyntaxError),
            121: lambda: ("Class error! Variable doesnt have Function Registry!", "ClassMissingFunctionReg", 0, SyntaxError),
            122: lambda: ("PT insertion Error! Index can't be smaller than 1", "InvalidIndexError", 0, SyntaxError),
            123: lambda: ("PT insertion Error! Index out of bounds!", "IndexOutoFBounds", 0, SyntaxError)
        }

        if self.code not in errors:
            raise ValueError(f"Unknown error code: {self.code}")

        message, name, offset, errorType = errors[self.code]()

        if exit:
            try:
                path: Path = zfile.zphPath
                context: str = path.read_text().splitlines()[cmd.lineNum - 1]

                raise errorType(
                    f"{Back.RED}[{self.code}] <{name}> | {message}{Back.RESET}",
                    (str(path), cmd.lineNum, offset, context)
                )
            except IndexError:
                raise ZError(118)
            
        else:
            print(f"{Back.RED}[{self.code}] <{name}> | {message}{Back.RESET}",)

ZValueType = Literal["INT", "FLOAT", "PT", "BOOL"]
ZBOOLValues: TypeAlias = Literal["~1", "~0"]

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
class ZValue:
    value: str
    valueType: ZValueType



    def isFloat(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def isInt(self, value: str) -> bool:
        if value.endswith(".0") or value == "":
            core = value[:-2]
            return core.isdigit() or (core.startswith("-") and core[1:].isdigit()) or value == ""
        return value.isdigit() or (value.startswith("-") and value[1:].isdigit())

    def isBool(self, value: str) -> bool:
        if value in ("1", "0", "1.0", "0.0", "", "~0", "~1", True, False):
            return True

        return False


    @property
    def asPythonBOOL(self):
        if self.valueType == "BOOL":
            match self.value:
                case "~1":
                    return True
                case "~0":
                    return False

        return False

    @property
    def asZBOOl(self) -> bool | ZBOOLValues:
        if self.valueType == "BOOL":
            return self.value # type:ignore

        return False

    @property
    def asNumBOOL(self):
        match self.value:
            case "~0": 
                return 0
            case "~1": 
                return 1

        return 0


    def isValueCompatibleWithType(self, value) -> bool:
        match self.valueType:
            case "FLOAT":
                if self.isFloat(value):
                    return True
            case "INT":
                if self.isInt(value):
                    return True
            case "PT":
                return True

            case "BOOL":
                if self.isBool(value):
                    return True
                
        return False

    def formatValueToMatchType(self, newValue: str|bool):
        match self.valueType:
            case "FLOAT":
                try:
                    self.value = str(float(newValue))
                except ValueError:
                    raise ZError(105)

            case "INT":
                try:
                    self.value = str(newValue).split(".")[0]
                except ValueError:
                    raise ZError(105)

            case "BOOL":
                match newValue:
                    case "0"|"0.0"|"~0"|False:
                        self.value = "~0"
                    case "1"|"1.0"|"~1"|True:
                        self.value = "~1"

            case "PT":
                self.value = str(newValue)
                


    def setValue(self, newValue: str, activeVars: ActiveVars) -> None:
        compiledValue = self.compileValue(newValue, activeVars)

        if not self.isValueCompatibleWithType(compiledValue):
            raise ZError(105)

        self.formatValueToMatchType(compiledValue)
       

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

                index = ZValue("0", "INT")
                index.setValue(indexRaw, activeVars)

                isList = True


            if isList:
                listVar: LIST = activeVars.get(varName)
                returnValue = listVar.getValue(int(index.value)).value # type: ignore

            else:
                var = activeVars.get(varName)
                if not var:
                    raise ZError(113)

                
                returnValue = var.onChange("")
        
            
        
        return returnValue # type: ignore


    def increment(self, incrementValueRaw: str, activeVars: ActiveVars) -> None:
        match self.valueType:
            case "PT":
                if incrementValueRaw == "":
                    incrementValueRaw = "1"
    
                incrementValue = ZValue("", "PT")
                incrementValue.setValue(incrementValueRaw, activeVars)
    
                
                
                self.value = f"{self.value}{incrementValue.value}"

            case "BOOL":
                match self.value:
                    case "~0":
                        self.value = "~1"
                    case "~1":
                        self.value = "~0"

            case "INT"|"FLOAT":
                self.setValue(str(float(self.value)+float(incrementValueRaw)), activeVars)


    def decrement(self, decrementValue: str, activeVars: ActiveVars) -> None:
        newValue = float(self.value) - float(decrementValue)

        match self.valueType:   
            case "PT":
                self.value = ""
            case "BOOL":
                match self.value:
                    case "~0":
                        self.value = "~1"
                    case "~1":
                        self.value = "~0"
                
            case "INT"|"FLOAT":
                self.setValue(str(newValue), activeVars)



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
    
    def onChange(self, targetType: str) -> str:
        """
        Returns the value that is being used for typechanging
        """
        return self.value.value
        
    def CT(self, cmd: ZCommand, activeVars: ActiveVars) -> ActiveVars:
        targetVarType: str = cmd.args[0]

        if targetVarType not in self.supportedVars:
            raise ZError(108)

            
        oldVar: Variable = activeVars[cmd.name]

        args: List|str = oldVar.onChange(targetVarType)

        if not isinstance(args, list):
            args = [args]
            
        newVarCmd: ZCommand = ZCommand(cmd.lineNum, cmd.name, ZBase.define, targetVarType, args)
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

        self.value: ZValue = ZValue("0", "INT")
        
        self.w(cmd, activeVars)
        
        self.registerFunc({self.w: "", self.INPUT: ""})

    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """        if self.const.compiledValue:
                    raise ZError(107)
        """

        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)

            case _:
                self.value.setValue(cmd.args[0] if cmd.args[0] != "" else "0", activeVars)

@register()
class FLOAT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "PT"]

        self.value: ZValue = ZValue("0.0", "FLOAT")
        self.maxFloatingPointNumbers: ZValue = ZValue("1", "INT")

        self.w(cmd, activeVars)

        self.registerFunc({self.w: "", self.INPUT: ""})

    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """if self.const.compiledValue:
            raise ZError(107)"""


        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)

            case _:
                self.value.setValue(cmd.args[0] if cmd.args[0] != "" else "0", activeVars)

@register()
class PT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "FLOAT", "LIST"]

        self.value: ZValue = ZValue("", "PT")
        self.w(cmd, activeVars)

        self.registerFunc({self.push: "", self.w: "", self.INPUT: "", self.insertAt: ""})
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """if self.const.compiledValue:
            raise ZError(107)"""


        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)

            case _:
                self.value.setValue(cmd.args[0], activeVars)

    def onChange(self, targetType: str) -> str:
        if targetType == "LIST":
            params = ["PT"]
            for char in self.value.value:
                params.append(f"{char}")

            return params  # pyright: ignore[reportReturnType]
        return self.value.value
    
    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)

    def insertAt(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 1 and cmd.args[0] != "" and cmd.args[1] != "":
            # try:
            valueToInsert = ZValue("", "PT")
            position = ZValue("0", "INT")
        

            valueToInsert.setValue(cmd.args[0], activeVars)
            position.setValue(cmd.args[1], activeVars)

            if int(position.value) < 1:
                raise ZError(122)

            if len(self.value.value)+1 < int(position.value):
                raise ZError(123)

            newValue = self.value.value[:int(position.value)-1] + valueToInsert.value + self.value.value[int(position.value)-1:]
            self.value.setValue(newValue, activeVars)
            # except Exception:
            #     raise ZError(122)


    def push(self, cmd: ZCommand) -> None:
        print(self.value.value)

@register()
class BOOL(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["FLOAT", "PT", "INT"]

        self.value: ZValue = ZValue("0", "BOOL")
        
        self.w(cmd, activeVars)
        
        self.registerFunc({self.w: "", self.INPUT: ""})

    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", activeVars)

            case _:
                self.value.setValue(cmd.args[0] if cmd.args[0] != "" else "0", activeVars)

    def onChange(self, targetType: str) -> str:
        match targetType:
            case "PT":
                return self.value.value
            case _:
                return str(self.value.asNumBOOL)



@register()
class CO(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT", "BOOL"]

        self.value: ZValue = ZValue("~0", "BOOL")
        self.rawCondition: ZValue = ZValue("", "PT")
        self.compiledCondition: str = ""


        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.w(cmd, activeVars)



        self.registerFunc({self.w: ""})

        
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.rawCondition.setValue(cmd.args[0], activeVars)
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
                    newValue = ZValue("", "PT")

                    # var = activeVars.get(varName)

                    newValue.setValue(f"'{varName}'", activeVars)
                    
                    if not newValue.isFloat(newValue.value):
                        newValue.value = f'"{newValue.value}"'

                    # if var:
                    #     if var.varType == "PT":
                    #         newValue.value = '"' + var.value.value + '"'
                    #     else:
                    #         newValue.setValue(var.value.value, activeVars)
                    # else:
                    #     raise ZError(111)

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
        
        self.value.formatValueToMatchType(result)

    def onChange(self, targetType: str) -> str:
        return self.value.value

@register()
class IF(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = []

        self.value: ZValue = ZValue("", "PT") # UNUSED HERE


        self.conditionalObjectName: ZValue = ZValue("", "PT")
        self.conditionalObjectValue: ZValue = ZValue("~0", "BOOL")

        self.countCommandsInIf: ZValue = ZValue("0", "INT")
        self.countCommandsInElif: ZValue = ZValue("0", "INT")
        

        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.w(cmd, activeVars) # Set if optional conditionObjectName is set
            
        self.registerFunc({self.START: "", self.ELSE: "", self.END: "", self.w: ""})


    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        if len(cmd.args) > 0:
            self.conditionalObjectName.setValue(cmd.args[0], activeVars)
            conditionalObject = activeVars.get(self.conditionalObjectName.value)

            if isinstance(conditionalObject, CO):
                self.conditionalObjectValue = conditionalObject.value # type: ignore
            else:
                raise ZError(112)
        else:
            raise ZError(114)
  
    
    def START(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.countCommandsInIf.setValue(cmd.args[0], activeVars)
        else:
            raise ZError(114)
        
        newIndex: ZIndex = 0
        if self.conditionalObjectValue.asPythonBOOL:
            newIndex = index
        elif not self.conditionalObjectValue.asPythonBOOL:
            newIndex = index + int(self.countCommandsInIf.value)
        
        return activeVars, newIndex

    def ELSE(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        self.countCommandsInElif.setValue(cmd.args[0], activeVars)
        newIndex: ZIndex = 0
        if not self.conditionalObjectValue.asPythonBOOL:
            newIndex = index
        elif self.conditionalObjectValue.asPythonBOOL:
            newIndex = index + int(self.countCommandsInElif.value)
        
        return activeVars, newIndex

    def END(self, cmd: ZCommand):
        pass

@register()
class MO(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["PT", "INT", "FLOAT"]

        self.value: ZValue = ZValue("0.0", "FLOAT")
        self.rawEquation: ZValue = ZValue("", "PT")
        self.compiledEquation: str = ""

        if len(cmd.args) > 0:
            if cmd.args[0] != "":
                self.w(cmd, activeVars)
        
        self.registerFunc({self.w: ""})

    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.rawEquation.setValue(cmd.args[0], activeVars)
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
                    newValue = ZValue("0.0", "FLOAT")
                    
                    newValue.setValue(f"'{varName}'", activeVars)
                    
                    # var = activeVars.get(varName)
                    # if var:
                    #     if var.varType == "PT":
                    #         newNewValue = ""
                    #         for char2 in var.value.value:
                    #             if char2 in MATH_ALLOWEDCHARS:
                    #                 newNewValue += char2
                    #         newValue.value = newNewValue
                    #     else:
                    #         newValue.setValue(var.value.value, activeVars)

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
        
        self.value.setValue(str(result), activeVars)

@register()
class FUNC(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "PT", "FLOAT"]


        self.returnType: str = ""
        self.disableVariableChange: ZValue = ZValue("~0", "BOOL")

        self.value: ZValue = ZValue("0.0", "FLOAT")
        self.rawEquation: str = ""
        self.compiledEquation: str = ""

        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.returnType = cmd.args[0]
        if len(cmd.args) > 1 and cmd.args[1] != "":
            self.disableVariableChange.setValue(cmd.args[1], activeVars)
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
        moName = ZValue("", "PT")
        moName.setValue(cmd.args[0], activeVars)
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
        if self.disableVariableChange.asPythonBOOL:
            self.compile(activeVars)
    
    def call(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if not self.disableVariableChange.asPythonBOOL:
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
                    newValue = ZValue("0.0", "FLOAT")
                    var = activeVars.get(varName)
                    if var:
                        if var.varType == "PT":
                            newNewValue = ""
                            for char in var.value.value:
                                if char in MATH_ALLOWEDCHARS:
                                    newNewValue += char
                            newValue.value = newNewValue
                        else:
                            newValue.setValue(var.value.value, activeVars)

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
        
        self.value.setValue(str(result), activeVars)

@register()
class RNG(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT", "BOOL"]


        

        self.randomNumberType: ZValueType = "FLOAT"
        self.allowedTypes: list[str] = ["INT", "FLOAT"]

        self.value: ZValue = ZValue("0", self.randomNumberType) # type:ignore
        self.rangeMin: ZValue = ZValue("0", self.randomNumberType)  # type:ignore
        self.rangeMax: ZValue = ZValue("0", self.randomNumberType)  # type:ignore


        if len(cmd.args) > 2 and cmd.args[0] != "" and cmd.args[1] != "" and cmd.args[2] != "":
            self.w(cmd, activeVars)


        self.registerFunc({self.w: ""})

    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        # Check if all arguments are available
        if not len(cmd.args) > 2 or cmd.args[0] == "" or cmd.args[1] == "" or cmd.args[2] == "":
            raise ZError(114)
        
        newRandomNumberType = ZValue("", "PT")
        newRandomNumberType.setValue(cmd.args[2], activeVars)
        if newRandomNumberType.value not in self.allowedTypes:
            raise ZError(114)
        self.randomNumberType = newRandomNumberType.value # type:ignore

        
        self.value: ZValue = ZValue("0", self.randomNumberType) 
        self.rangeMin: ZValue = ZValue("0", self.randomNumberType) 
        self.rangeMax: ZValue = ZValue("0", self.randomNumberType)  


        self.rangeMin.setValue(cmd.args[0], activeVars)
        self.rangeMax.setValue(cmd.args[1], activeVars)

        self.generate(activeVars)

    def generate(self, activeVars: ActiveVars):
        newValue = 0
        match self.randomNumberType:
            case "INT":
                newValue = random.randint(int(self.rangeMin.value), int(self.rangeMax.value))
            case "FLOAT":
                newValue = random.uniform(float(self.rangeMin.value), float(self.rangeMax.value))
            case _:
                pass

        self.value.setValue(str(newValue), activeVars)

@register()
class LOOP(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT"]

        self.startIndex: ZIndex = index
        self.countCommandsInLoop: ZValue = ZValue("0", "INT")
        self.active: bool = False
        self.countLooped: int = 1

        self.conditionalObjectName: ZValue = ZValue("", "PT")
        


        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.w(cmd, activeVars)
        
        self.registerFunc({self.w: "", self.START: "", self.END: "", self.STOP: ""})

    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.conditionalObjectName.setValue(cmd.args[0], activeVars)

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
        if self.conditionalObject.value.asPythonBOOL:
            self.active = True
        else:
            self.active = False

    def STOP(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex):
        index = self.startIndex + int(self.countCommandsInLoop.value) +1 

        return activeVars, index
            

    def START(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex):
        self.startIndex = index

        if len(cmd.args) > 0 and cmd.args[0] != "":
            self.countCommandsInLoop.setValue(cmd.args[0], activeVars)
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

    def onChange(self, targetType: str) -> str:
        return str(self.countLooped)

@register()
class FILE(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = []

        self.value: ZValue = ZValue("", "PT") # unused

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
            rawPath = ZValue("", "PT")
            rawPath.setValue(cmd.args[0], activeVars)
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
        if len(cmd.args) <= 0 and cmd.args[0] == "":
            raise ZError(14)
        
        text = ZValue("", "PT")
        text.setValue(cmd.args[0], activeVars)

        with self.path.open("w") as openFile:
            openFile.write(text.value)

    def cFLUSH(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        with self.path.open("w"):
            pass

    def gRENAME(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            newName = ZValue("", "PT")
            newName.setValue(cmd.args[0], activeVars)
            self.path.rename(newName.value)
        else:
            raise ZError(114)

    def gDEL(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.path.unlink()

    def onChange(self, targetType: str) -> str:
        ret = ""
        with self.path.open("r") as openFile:
            ret = openFile.readlines()
        
        return str(*ret)
    
@register()
class LIST(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["PT", "INT", "FLOAT"]

        self.pointer: ZValue = ZValue("1", "INT")

        self.allowedValueTypes: list[str] = ["INT", "PT", "FLOAT"]
        self.valueType: ZValueType = "FLOAT"

        self.posValues: List[ZValue] = []
        self.negValues: List[ZValue] = []


        # Set Value Type
        cmd.checkArgs(1)
        self.changeValueType(cmd, activeVars)

        if cmd.checkArgs(2, False): # Set value if 2 args
            args = cmd.args.copy()
            args.pop(0)

            for arg in args:
                self.setValue(arg, activeVars)
                self.pointer.value = str(int(self.pointer.value)+1)
            self.pointer.value = "1"

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


    def onChange(self, targetType: str) -> str:
        return self.getValue(int(self.pointer.value)).value

    def setPointer(self, position: str, activeVars: ActiveVars):
        pointer = ZValue("", "INT")
        pointer.setValue(position, activeVars)

        if int(pointer.value) == 0:
            raise ZError(109)

        self.pointer = pointer

    def setValue(self, valueRaw: str, activeVars: ActiveVars):
        if int(self.pointer.value) > 0:
            pointer = int(self.pointer.value) -1

            value = ZValue("", self.valueType)
            value.setValue(valueRaw, activeVars)

            while len(self.posValues) <= pointer:
                self.posValues.append(ZValue("", "INT"))

            self.posValues[pointer] = value

        elif int(self.pointer.value) < 0:
            pointer = abs(int(self.pointer.value)) -1
            value = ZValue("", self.valueType)
            value.setValue(valueRaw, activeVars)

            while len(self.negValues) <= pointer:
                self.negValues.append(ZValue("", "INT"))

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
        waitTime: ZValue = ZValue("0.0", "FLOAT")
        waitTime.setValue(cmd.args[0], activeVars)

        time.sleep(float(waitTime.value))

    def jump(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex] :
        indexToAdd: ZValue = ZValue("0", "INT")
        if len(cmd.args[0]):
            if cmd.args[0] == "":
                raise ZError(114)
            
            indexToAdd.setValue(cmd.args[0], activeVars)

            if indexToAdd.value.startswith("-"):
                return activeVars, ZIndex(index-int(indexToAdd.value.replace("-", ""))-1)
            else:
                return activeVars, ZIndex(index+(int(indexToAdd.value)))

        raise ZError(114)
    
    def jumpTo(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        indexToJump: ZValue = ZValue("0", "INT")
        if len(cmd.args[0]):
            if cmd.args[0] == "":
                raise ZError(114)
            
            indexToJump.setValue(cmd.args[0], activeVars)

            return activeVars, int(indexToJump.value)-2

        raise ZError(114)
 

    def LIB(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args[0]) > 0 and cmd.args[0] != "":
            userPath = ZValue("", "PT")
            userPath.setValue(cmd.args[0], activeVars)
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
            fileName = ZValue("", "PT")
            fileName.setValue(cmd.args[0], activeVars)

            zfile = ZFile(Path(fileName.value))

            zfile.zphPath.parent.mkdir(parents=True, exist_ok=True)

            with zfile.zpkgPath.open("wb") as f:
                pickle.dump(activeVars, f)
        else:
            with self.zfile.zpkgPath.open("wb") as f:
                pickle.dump(activeVars, f)

    def load(self, cmd: ZCommand, activeVars: ActiveVars) -> ActiveVars:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            fileName = ZValue("", "PT")
            fileName.setValue(cmd.args[0], activeVars)

            zfile = ZFile(Path(fileName.value))

            if not zfile.zphPath.is_file():
                raise ZError(116)
            
            with zfile.zpkgPath.open("rb") as f:
                newActiveVars = pickle.load(f)

        else:
            with self.zfile.zpkgPath.open("rb") as f:
                newActiveVars = pickle.load(f)


        return activeVars|newActiveVars

@register()
class AO(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "FLOAT"]

        self.value: ZValue = ZValue("0", "INT") # Current position of the Animation
        self.delay: ZValue = ZValue("0", "FLOAT")
        self.frames: list[ZValue] = []
        self.doClearScreen: ZValue = ZValue("~0", "BOOL")


        if cmd.args[0] != "":
            self.w(cmd, activeVars)
        if len(cmd.args) > 1 and cmd.args[1] != "":
            self.delay.setValue(cmd.args[1], activeVars)
        if len(cmd.args) > 2 and cmd.args[2] != "":
            self.doClearScreen.setValue(cmd.args[2], activeVars)
                
        

        self.registerFunc({self.w: "", self.setDelay: "", self.clearScreen: "", self.start: "", self.step: "", self.reset: "", self.setIndex: "", self.display: ""})

    def displayFrame(self, pos: int):
       print(self.frames[pos].value)

    def display(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.displayFrame(int(self.value.value))

    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if cmd.args[0] and cmd.args[0] != "":
            self.frames.append(ZValue("", "PT"))
            self.frames[-1].setValue(cmd.args[0], activeVars)


    def setDelay(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
       self.delay.setValue(cmd.args[0], activeVars) 

    def setIndex(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.value.setValue(cmd.args[0], activeVars)

    def clearScreen(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.doClearScreen.setValue(cmd.args[0], activeVars)

    def start(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        for index in range(int(self.value.value), len(self.frames)):
            self.displayFrame(index)
            time.sleep(float(self.delay.value))
            if self.doClearScreen.asPythonBOOL:
                print('\033[2J\033[H')
                pass # TODO: clear screen!
            
        self.value = ZValue("0", "INT")
        
    def step(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.displayFrame(int(self.value.value))
        self.value.increment("1", activeVars)
        
    def reset(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.value = ZValue("0", "INT")
            
if __name__ == "__main__":
    import subprocess
    subprocess.call(["python3", "src/main.py"])
