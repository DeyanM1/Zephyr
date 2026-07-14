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
from typing import Any, Callable, List, TypeAlias, Literal, Union

from colorama import Back

typeRegistry: dict[str, type] = {}


ActiveVars: TypeAlias = dict[str, "Variable"]
ZIndex: TypeAlias = int

MO_ALLOWEDCHARS: str = "+-*/%=()1234567890."
CO_ALLOWEDCHARS: str = "()=!><1234567890."


class ZError(Exception):
    def __init__(self, code: int) -> None:
        self.code = code
    
    def process(self, cmd: ZCommand, zfile: ZFile, exit: bool = True, returnDict: bool = False) -> None|dict:
        # errorCode: (message, offset_function)
        errors: dict[int, Callable[..., tuple[str, str, int, type[BaseException]]]] = {
            101: lambda: (f"Unknown Base, use '{ZBase.use}' or '{ZBase.define}'", "UnknownBase", len(cmd.name) + 2, SyntaxError),
            102: lambda: ("Undefined Variable", "UndefinedVariable", 1, SyntaxError),
            103: lambda: ("Unknown Function.", "UnknownFunction", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            104: lambda: ("Wrong command structure. Missing ':' or ';'?", "InvalidStructure", 1, SyntaxError),
            105: lambda: ("Variable Type doesn't match given Value", "ValueError", 1, SyntaxError),
            106: lambda: ("Invalid Boolean type. Allowed: ~0 / ~1", "ValueError", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            107: lambda: ("Value cannot be changed. Variable is constant!", "WriteProtection", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            108: lambda: ("Current Variable type doesnt support new variable type!", "TypeError", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            109: lambda: ("List doesn't support position 0!", "ListIndexError", len(f"{cmd.name}")+7, SyntaxError),
            110: lambda: ("Only INT, PT, FLOAT are in- and decrementable!", "WriteError", 1, SyntaxError),
            111: lambda: ("Error in Condition/Equation.", "ConditionError",  len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
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
            123: lambda: ("PT insertion Error! Index out of bounds!", "IndexOutoFBounds", 0, SyntaxError),
            124: lambda: ("Module Not Found inside global / local dir", "ModuleNotFound", 0, SyntaxError),
            125: lambda: ("Unknown List collection type! Use: POS / NEG", "UnknownListCollectionType", 0, SyntaxError),
            126: lambda: ("Uncompleted Index Scobe: Missing > in variable index.", "UncompletedIndexScobe", 0, SyntaxError),
            127: lambda: ("MO name not yet provided. use: ? w.", "MONotFound", 0, SyntaxError),
        }

        if returnDict:
            return errors

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
    args: List[str]


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
        if value.endswith(".0"):
            core = value[:-2]
            return core.isdigit() or (core.startswith("-") and core[1:].isdigit()) or value == ""
        return value.isdigit() or (value.startswith("-") and value[1:].isdigit())

    def isBool(self, value: str) -> bool:
        if value in ("1", "0", "1.0", "0.0", "", "~0", "~1"):
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
    def asZBOOL(self) -> bool | ZBOOLValues:
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
                    if newValue == "":
                        self.value = "0.0"
                    else:
                        self.value = str(float(newValue))
                except ValueError:
                    raise ZError(105)

            case "INT":
                try:
                    if newValue == "":
                        self.value = "0"
                    else:
                        self.value = str(int(str(newValue).split(".")[0]))
                except ValueError:
                    raise ZError(105)

            case "BOOL":
                match newValue:
                    case "0"|"0.0"|"~0"|False|"":
                        self.value = "~0"
                    case "1"|"1.0"|"~1"|True:
                        self.value = "~1"
                    case _:
                        self.value = "~0"

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
                try:
                    varName, indexRaw = varName.split("<", 1)
                except ValueError:
                    raise ZError(126)

                indexRaw = "".join(indexRaw.rsplit(">", 1))

                index = ZValue("0", "INT")
                index.setValue(indexRaw, activeVars)

                isList = True


            if isList:
                listVar: LIST = activeVars.get(varName)
                
                if not listVar:
                    raise ZError(113)
                    
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

            case "INT":
                incrementValue = ZValue("0", "INT")
                incrementValue.setValue(incrementValueRaw, activeVars)
                
                self.setValue(str(int(self.value)+int(incrementValue.value)), activeVars)
            
            case "FLOAT":
                incrementValue = ZValue("0", "FLOAT")
                incrementValue.setValue(incrementValueRaw, activeVars)
                
                self.setValue(str(float(self.value)+float(incrementValue.value)), activeVars)


    def decrement(self, decrementValueRaw: str, activeVars: ActiveVars) -> None:
        match self.valueType:   
            case "PT":
                self.value = ""
            case "BOOL":
                match self.value:
                    case "~0":
                        self.value = "~1"
                    case "~1":
                        self.value = "~0"
                
            case "INT":
                incrementValue = ZValue("0", "INT")
                incrementValue.setValue(decrementValueRaw, activeVars)
                
                self.setValue(str(int(self.value)-int(incrementValue.value)), activeVars)
            
            case "FLOAT":
                incrementValue = ZValue("0", "FLOAT")
                incrementValue.setValue(decrementValueRaw, activeVars)
                
                self.setValue(str(float(self.value)-float(incrementValue.value)), activeVars)



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

        self.value: ZValue


        self.supportedVars: List[str] = [] # Supported Variables to change to

        self.functionRegistry: dict[str, Callable[..., Any]] = {}
        self.registerFunc({self.CT: "", self.debug: ""})


    def registerFunc(self, funcList: dict[Callable[..., Any], str]) -> None:
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
        cmd.checkArgs(1, True)
        
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

### ------- Simple Variable -------

@register()
class INT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["FLOAT", "PT"]

        self.value: ZValue = ZValue("0", "INT")
        self.constant: ZValue = ZValue("~0", "BOOL")

        self.firstTimeInit(cmd, activeVars)
        
        self.registerFunc({self.w: "", self.INPUT: "", self.C: "", self.LGTH: ""})

    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)
        
        if cmd.checkArgs(2, False):
            self.setConstant(cmd.args[1], activeVars)

    def setConstant(self, newStateRaw: str, activeVars: ActiveVars):
        self.constant.setValue(newStateRaw, activeVars)

    ### --- Callable Functions

    def LGTH(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)
        targetVarName = ZValue("", "PT")
        targetVarName.setValue(cmd.args[0], activeVars)

        length = str(len(self.value.value))
        var = activeVars.get(targetVarName.value)
        if not var:
            raise ZError(113)

        if var.varType not in ["INT", "PT", "FLOAT", "BOOL"]:
            raise ZError(112)
            
        var.value.setValue(length, activeVars)
        activeVars.update({var.name: var})

        return activeVars

    def C(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        self.setConstant(cmd.args[0], activeVars)
        
    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if self.constant.asPythonBOOL:
            raise ZError(107)

        cmd.checkArgs(1, True)

        match cmd.args[0]:
            case "++":
                if cmd.checkArgs(2, False):
                    self.value.increment(cmd.args[1], activeVars)
                else:
                    self.value.increment("1", activeVars)
                    
            case "--":
                if cmd.checkArgs(2, False):
                    self.value.decrement(cmd.args[1], activeVars)
                else:
                    self.value.decrement("1", activeVars)

            case _:
                self.value.setValue(cmd.args[0], activeVars)

@register()
class FLOAT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "PT"]

        self.value: ZValue = ZValue("0.0", "FLOAT")
        self.constant: ZValue = ZValue("~0", "BOOL")
        self.maxFloatingPointNumbers: ZValue = ZValue("1", "INT") # Currently unused

        self.firstTimeInit(cmd, activeVars)

        self.registerFunc({self.w: "", self.INPUT: "", self.C: "", self.LGTH: ""})

    
    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):      
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)
        
        if cmd.checkArgs(2, False):
            self.setConstant(cmd.args[1], activeVars)

    def setConstant(self, newStateRaw: str, activeVars: ActiveVars):
        self.constant.setValue(newStateRaw, activeVars)


    # --- Callable Functions
     
    def LGTH(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)
        targetVarName = ZValue("", "PT")
        targetVarName.setValue(cmd.args[0], activeVars)

        length = str(len(self.value.value))
        var = activeVars.get(targetVarName.value)
        if not var:
            raise ZError(113)

        if var.varType not  in ["INT", "PT", "FLOAT", "BOOL"]:
            raise ZError(112)
            
        var.value.setValue(length, activeVars)
        activeVars.update({var.name: var})

        return activeVars 

    def C(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        self.setConstant(cmd.args[0], activeVars)
          
    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if self.constant.asPythonBOOL:
            raise ZError(107)

        cmd.checkArgs(1, True)


        match cmd.args[0]:
            case "++":
                if cmd.checkArgs(2, False):
                    self.value.increment(cmd.args[1], activeVars)
                else:
                    self.value.increment("1", activeVars)
                    
            case "--":
                if cmd.checkArgs(2, False):
                    self.value.decrement(cmd.args[1], activeVars)
                else:
                    self.value.decrement("1", activeVars)

            case _:
                self.value.setValue(cmd.args[0] if cmd.args[0] != "" else "0", activeVars)

@register()
class PT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "FLOAT", "LIST"]

        self.value: ZValue = ZValue("", "PT")
        self.constant: ZValue = ZValue("~0", "BOOL")
        
        self.firstTimeInit(cmd, activeVars)

        self.registerFunc({self.push: "", self.w: "", self.INPUT: "", self.insertAt: "", self.C: "", self.LGTH: ""})

        
    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)
        
        if cmd.checkArgs(2, False):
            self.setConstant(cmd.args[1], activeVars)

    def setConstant(self, newStateRaw: str, activeVars: ActiveVars):
        self.constant.setValue(newStateRaw, activeVars)

    def onChange(self, targetType: str) -> str|List[str]:    # pyright: ignore[reportIncompatibleMethodOverride]
        if targetType == "LIST":
            params = ["PT"]
            for char in self.value.value:
                params.append(f"{char}")

            return params
        return self.value.value
    

    # --- Callable Functions

    def LGTH(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)
        targetVarName = ZValue("", "PT")
        targetVarName.setValue(cmd.args[0], activeVars)

        length = str(len(self.value.value))
        var = activeVars.get(targetVarName.value)
        if not var:
            raise ZError(113)

        if var.varType not  in ["INT", "PT", "FLOAT", "BOOL"]:
            raise ZError(112)
            
        var.value.setValue(length, activeVars)
        activeVars.update({var.name: var})

        return activeVars 

    def C(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        self.setConstant(cmd.args[0], activeVars)
       
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if self.constant.asPythonBOOL:
            raise ZError(107)

        
        cmd.checkArgs(1, True)


        match cmd.args[0]:
            case "++":
                if cmd.checkArgs(2, False):
                    self.value.increment(cmd.args[1], activeVars)
                else:
                    self.value.increment("1", activeVars)
                    
            case "--":
                self.value.decrement("0", activeVars)

            case _:
                self.value.setValue(cmd.args[0], activeVars)

    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)

    def insertAt(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(2, True)
        
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

    def push(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if cmd.checkArgs(1, False):
            newLine = ZValue("~1", "BOOL")
            newLine.setValue(cmd.args[0], activeVars)

            if newLine.asPythonBOOL:
                print(self.value.value)
            else:
                sys.stdout.write(self.value.value)
        else:           
            print(self.value.value)

@register()
class BOOL(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["FLOAT", "PT", "INT"]

        self.value: ZValue = ZValue("~0", "BOOL")
        self.constant: ZValue = ZValue("~0", "BOOL")
        
        self.firstTimeInit(cmd, activeVars)
        
        self.registerFunc({self.w: "", self.INPUT: "", self.C: ""})

    
    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)
        
        if cmd.checkArgs(2, False):
            self.setConstant(cmd.args[1], activeVars)

    def setConstant(self, newStateRaw: str, activeVars: ActiveVars):
        self.constant.setValue(newStateRaw, activeVars)
 
    def onChange(self, targetType: str) -> str:
        match targetType:
            case "PT":
                return self.value.value
            case _:
                return str(self.value.asNumBOOL)


    # --- Callable Functions

    def C(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        self.setConstant(cmd.args[0], activeVars)
          
    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        message = ZValue("", "PT")
        message.setValue(cmd.args[0], activeVars)
        newValue = input(message.value)
        self.value.setValue(newValue, activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if self.constant.asPythonBOOL:
            raise ZError(107)

        
        cmd.checkArgs(1, True)


        match cmd.args[0]:
            case "++":
                self.value.increment("1", activeVars)
                    
            case "--":
                self.value.decrement("1", activeVars)

            case _:
                self.value.setValue(cmd.args[0], activeVars)


### ------- Other -------

@register()
class CO(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT", "BOOL"]

        self.value: ZValue = ZValue("~0", "BOOL")
        self.rawCondition: ZValue = ZValue("", "PT")
        self.compiledCondition: str = ""


        self.firstTimeInit(cmd, activeVars)


        self.registerFunc({self.w: ""})

    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)

    def compile(self, activeVars: ActiveVars) -> None:
        self.compiledCondition = ""

        
        if self.rawCondition.value.startswith("(") and self.rawCondition.value.endswith(")"):
            self.rawCondition.value = self.rawCondition.value.removeprefix("(").removesuffix(")")


        varBuffer = ""
        qCounter = 0 # Quote Counter
        cCounter = 0 # < / > Counter
        inVar = False

        for char in self.rawCondition.value:
            if char == "'":
                if not inVar:
                    self.compiledCondition += "~"
                    
                if cCounter == qCounter:
                    qCounter += 1
                    varBuffer += "'"
                    inVar = True

                elif cCounter != qCounter:
                    qCounter -= 1
                    varBuffer += "'"
            
            elif char == "<" and inVar:
                cCounter += 1
                varBuffer += "<"
                    
            elif char == ">" and inVar:
                cCounter -= 1
                varBuffer += ">"
                    
            else:
                if inVar:
                    varBuffer += char

                elif char in CO_ALLOWEDCHARS:
                    self.compiledCondition += char

            if qCounter == 0 and cCounter == 0 and inVar:
                value = ZValue("", "PT")
                value.setValue(varBuffer, activeVars)

                if not value.isFloat(value.value):
                    value.value = f'"{value.value}"'
                
                self.compiledCondition = self.compiledCondition.replace("~", value.value, 1)

                varBuffer = ""
                inVar = False

        
        self.evaluate()

    def evaluate(self) -> None:
        result: bool = False
        
        try:
            result = bool(eval(self.compiledCondition))
        except Exception: 
            raise ZError(111)
        
        self.value.formatValueToMatchType(result)

    def onChange(self, targetType: str) -> str:
        return self.value.value


    # --- Callable Functions
        
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1, True)
        
        self.rawCondition.setValue(cmd.args[0], activeVars)
        self.compile(activeVars)

@register()
class IF(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = []

        self.value: ZValue = ZValue("", "PT") # UNUSED HERE


        self.conditionalObject: Variable

        self.endIndex: ZIndex = 0
        self.elseIndex: ZIndex = 0
        
        self.firstTimeInit(cmd, activeVars) 
        
            
        self.registerFunc({self.START: "", self.ELSE: "", self.END: "", self.w: ""})


    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)

    # --- Callable Functions

    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)

        coName = ZValue("", "PT")
        
        coName.setValue(cmd.args[0], activeVars)
        conditionalObject = activeVars.get(coName.value)

        if not conditionalObject: 
            raise ZError(113)

        if conditionalObject.varType == "CO":
            raise ZError(112)
              
        self.conditionalObject = conditionalObject
            
  
    def START(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        cmd.checkArgs(1)
        self.endIndex = int(cmd.args[0])

        if cmd.checkArgs(2, False):
            self.elseIndex = int(cmd.args[1])
        
        newIndex: ZIndex = 0
        if self.conditionalObject.value.asPythonBOOL:
            newIndex = index
            
        else:
            if self.elseIndex != 0:
                newIndex = self.elseIndex
            else:
                newIndex = self.endIndex
        
        return activeVars, newIndex

    def ELSE(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        newIndex: ZIndex = 0
        if not self.conditionalObject.value.asPythonBOOL:
            newIndex = index
        else:
            newIndex = self.endIndex
            
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

        self.firstTimeInit(cmd, activeVars)
        
        self.registerFunc({self.w: ""})


    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)
            
    
    def compile(self, activeVars: ActiveVars) -> None:
        self.compiledEquation = ""

        
        if self.rawEquation.value.startswith("(") and self.rawEquation.value.endswith(")"):
            self.rawEquation.value = self.rawEquation.value.removeprefix("(").removesuffix(")")

        
        varBuffer = ""
        qCounter = 0 # Quote Counter
        cCounter = 0 # < / > Counter
        inVar = False

        for char in self.rawEquation.value:
            if char == "'":
                if not inVar:
                    self.compiledEquation += "~"
                    
                if cCounter == qCounter:
                    qCounter += 1
                    varBuffer += "'"
                    inVar = True

                elif cCounter != qCounter:
                    qCounter -= 1
                    varBuffer += "'"
            
            elif char == "<" and inVar:
                cCounter += 1
                varBuffer += "<"
                    
            elif char == ">" and inVar:
                cCounter -= 1
                varBuffer+= ">"
                    
            else:
                if inVar:
                    varBuffer += char

                elif char in MO_ALLOWEDCHARS:
                    self.compiledEquation += char

            if qCounter == 0 and cCounter == 0 and inVar:
                buf = ''.join(varBuffer)
                
                value = ZValue("", "PT")
                value.setValue(buf, activeVars)
                
                self.compiledEquation = self.compiledEquation.replace("~", value.value, 1)

                varBuffer = [""]
                inVar = False

        
        self.calculate(activeVars)


    def calculate(self, activeVars: ActiveVars) -> None:
        result: float = 0

        try:
            result = eval(self.compiledEquation)
        except Exception: 
            raise ZError(111)
        
        self.value.setValue(str(result), activeVars)

    
    # --- Callable Functions

    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1, True)
        
        self.rawEquation.setValue(cmd.args[0], activeVars)
        self.compile(activeVars)
      
@register()
class FUNC(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "PT", "FLOAT"]


        self.returnType: ZValue = ZValue("", "PT")
        self.disableVariableChange: ZValue = ZValue("~0", "BOOL")

        self.value: ZValue = ZValue("0.0", "FLOAT")
        self.mo: MO # Is initialized Later

        self.firstTimeInit(cmd, activeVars)
                
        self.registerFunc({self.w: "", self.call: ""})

    
    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        self.returnType.setValue(cmd.args[0], activeVars)

        if cmd.checkArgs(2, False): 
            self.disableVariableChange.setValue(cmd.args[1], activeVars)
        
        if cmd.checkArgs(3, False):
            mathObject: MO = activeVars.get(cmd.args[2])
            if not mathObject:
                raise ZError(113)
            if isinstance(mathObject, MO):
                self.mo = mathObject
            else:
                raise ZError(112)

            self.autoCall(activeVars)

    def autoCall(self, activeVars: ActiveVars) -> None:
        """This function is called after the equation is set and calculates the equation if diasbleVariableChange is True
            The normal call function is the one called using    fun ? call:;
        """
        if self.disableVariableChange.asPythonBOOL:
            self.mo.compile(activeVars)
            self.value = self.mo.value

    # --- Callable Functions
                
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1, True)
        
        moName = ZValue("", "PT")
        moName.setValue(cmd.args[0], activeVars)
        mathObject = activeVars.get(moName.value)
        
        if not mathObject:
            raise ZError(113)
        if mathObject.varType != "MO":
            raise ZError(112)
                       
        self.mo = mathObject

        self.autoCall(activeVars)

    def call(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if not self.disableVariableChange.asPythonBOOL:
            try:
                self.mo.compile(activeVars)
            except AttributeError:
                raise ZError(127)
            self.value = self.mo.value
        
@register()
class RNG(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT", "BOOL"]

        self.randomNumberType: ZValueType = "FLOAT"
        self.allowedTypes: List[str] = ["INT", "FLOAT"]

        self.value: ZValue = ZValue("0", self.randomNumberType) # type:ignore
        self.rangeMin: ZValue = ZValue("0", self.randomNumberType)  # type:ignore
        self.rangeMax: ZValue = ZValue("0", self.randomNumberType)  # type:ignore

        self.firstTimeInit(cmd, activeVars)

        self.registerFunc({self.w: ""})
    
    
    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(3, True)
        
        self.w(cmd, activeVars)
    
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

    # --- Callable Functions  

    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        # Check if all arguments are available
        cmd.checkArgs(3)
        
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

@register()
class LOOP(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> None:
        super().__init__(cmd, activeVars)

        self.supportedVars = ["INT", "FLOAT", "PT"]

        self.startIndex: ZIndex = index
        self.endIndex: ZIndex = 0
        
        self.active: bool = False
        self.countLooped: int = 1

        self.conditionalObject: CO # Defined later

        self.firstTimeInit(cmd, activeVars)
        
        self.registerFunc({self.w: "", self.START: "", self.END: "", self.STOP: ""})

    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)

    def checkCondition(self, activeVars: ActiveVars):
        self.conditionalObject.compile(activeVars)
        if self.conditionalObject.value.asPythonBOOL:
            self.active = True
        else:
            self.active = False
   
    def onChange(self, targetType: str) -> str:
        return str(self.countLooped)

    
    # --- Callable Functions  

    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)
        
        coName = ZValue("", "PT")
        coName.setValue(cmd.args[0], activeVars)

        var: CO = activeVars.get(coName.value)

        if not var:
            raise ZError(113)
            
        if not isinstance(var, CO):
            raise ZError(112)

        self.conditionalObject = var
        
        self.checkCondition(activeVars)
        
    def STOP(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex):
        index = self.endIndex

        return activeVars, index
            
    def START(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex):
        self.startIndex = index
        
        cmd.checkArgs(1)
        self.endIndex = int(cmd.args[0])


        self.checkCondition(activeVars)
        if not self.active:
            return activeVars, self.endIndex
        
        
        return activeVars, index

    def END(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex):
        self.checkCondition(activeVars)

        if self.active:
            self.countLooped += 1
            return activeVars, self.startIndex
        else:
            return activeVars, index

@register()
class FILE(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = []

        self.path: Path = Path()


        self.firstTimeInit(cmd, activeVars)
        

        self.registerFunc({self.w: ""})
        self.registerFunc({self.cSET: "", self.cFLUSH: "", self.cREAD: ""})
        self.registerFunc({self.gRENAME: "", self.gDEL: ""})

        
    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)
            
    def onChange(self, targetType: str) -> str:
        ret = ""
        with self.path.open("r") as openFile:
            ret = openFile.readlines()
        
        return "".join(ret)
        
                
    # --- Callable Functions  

    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        """
        Only sets the filePath
        
        """

        if not cmd.checkArgs(1, False):
            self.path = Path.cwd() / "unnamed_file.txt"

        else:
            rawPath = ZValue("", "PT")
            rawPath.setValue(cmd.args[0], activeVars)
            path = Path(rawPath.value)

            if not path.is_absolute():
                path = (Path.cwd() / path).resolve()
            
            self.path = path


        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

        self.value.value = self.path.as_posix()

    def cREAD(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)

        cleanLines = ZValue("~0", "BOOL")
        if cmd.checkArgs(2, False):
            cleanLines.setValue(cmd.args[1], activeVars)

        targetVarName = ZValue("", "PT")
        targetVarName.setValue(cmd.args[0], activeVars)

        targetVar: Union[None, LIST, PT] = activeVars.get(targetVarName.value)
        if not targetVar:
            raise ZError(113)
        
        with self.path.open("r") as f:
            content = f.readlines()

        if cleanLines.asPythonBOOL:
            tempLines = []
            for line in content:
                tempLines.append(line.lstrip().rstrip().removesuffix("\n"))
            content = tempLines.copy()

        
            
        match targetVar.varType:
            case "LIST":
                listContent = []
                for line in content:
                    listContent.append(ZValue(line, "PT"))
                    
                targetVar.posValues = listContent

            case "PT":
                targetVar.value.value = "".join(content)

            case _:
                raise ZError(112)


        activeVars.update({targetVar.name: targetVar})
        return activeVars
                
        

    def cSET(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1)
        
        text = ZValue("", "PT")
        text.setValue(cmd.args[0], activeVars)

        with self.path.open("w") as openFile:
            openFile.write(text.value)

    def cFLUSH(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        with self.path.open("w"):
            pass

    def gRENAME(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1, True)
        
        newName = ZValue("", "PT")
        newName.setValue(cmd.args[0], activeVars)
        self.path = self.path.rename(newName.value)

    def gDEL(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.path.unlink()
  
@register()
class LIST(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["PT", "INT", "FLOAT"]

        self.pointer: ZValue = ZValue("1", "INT")

        self.allowedValueTypes: List[str] = ["INT", "PT", "FLOAT"]
        self.valueType: ZValueType = "FLOAT"

        self.posValues: List[ZValue] = []
        self.negValues: List[ZValue] = []


        self.firstTimeInit(cmd, activeVars)

        self.registerFunc({self.w: "", self.SET: "SET", self.changeValueType: "CVT", self.LGTH: "", self.copy: ""})


    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
       cmd.checkArgs(1, True) 
       self.changeValueType(cmd, activeVars)
                
       if cmd.checkArgs(2, False): # Set value if 2 args
            args = cmd.args.copy()
            args.pop(0)

            for arg in args:
                self.setValue(arg, activeVars)
                self.pointer.value = str(int(self.pointer.value)+1)
            self.pointer.value = "1"
                           
    def onChange(self, targetType: str) -> str:
        return self.getValue(int(self.pointer.value)).value

    def setPointer(self, position: str, activeVars: ActiveVars):
        pointer = ZValue("1", "INT")
        pointer.setValue(position, activeVars)

        if int(pointer.value) > 0:
            while len(self.posValues) < int(pointer.value):
                self.posValues.append(ZValue("", self.valueType))

        if int(pointer.value) == 0:
            raise ZError(109)

        self.pointer = pointer


    def setValue(self, valueRaw: str, activeVars: ActiveVars):
        if int(self.pointer.value) > 0:
            pointer = int(self.pointer.value) -1

            value = ZValue("", self.valueType)
            value.setValue(valueRaw, activeVars)

            while len(self.posValues) <= pointer:
                self.posValues.append(ZValue("", self.valueType))

            self.posValues[pointer] = value

        elif int(self.pointer.value) < 0:
            pointer = abs(int(self.pointer.value)) -1
            value = ZValue("", self.valueType)
            value.setValue(valueRaw, activeVars)

            while len(self.negValues) <= pointer:
                self.negValues.append(ZValue("", self.valueType))

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


    # --- Callable Functions  

    def copy(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)

        targetListName = ZValue("", "PT")
        targetListName.setValue(cmd.args[0], activeVars)
        
        targetList = activeVars.get(targetListName.value)
        if not targetList:
            raise ZError(113)
            
        if not targetList.varType == "LIST":
            raise ZError(112)


        targetList.posValues = self.posValues   # pyright: ignore[reportAttributeAccessIssue]
        targetList.negValues = self.negValues   # pyright: ignore[reportAttributeAccessIssue]

        activeVars.update({targetList.name: targetList})

        return activeVars
        

        
     
    def LGTH(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(2, True)

        listToChoose = ZValue("", "PT") # POS | NEG
        listToChoose.setValue(cmd.args[0], activeVars)

        if listToChoose.value not in ["POS", "NEG"]:
            raise ZError(125)
        
        targetVarName = ZValue("", "PT")
        targetVarName.setValue(cmd.args[1], activeVars)

        length = ""
        match listToChoose.value:
            case "POS":
                length = str(len(self.posValues))
            case "NEG":
                length = str(len(self.negValues))

                
        var = activeVars.get(targetVarName.value)
        if not var:
            raise ZError(113)

        if var.varType not  in ["INT", "PT", "FLOAT", "BOOL"]:
            raise ZError(112)
            
        var.value.setValue(length, activeVars)
        activeVars.update({var.name: var})

        return activeVars 

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

    def debug(self, cmd: ZCommand, activeVars: ActiveVars):
        print(self.posValues, "\n", self.negValues)
        print("POS: ", self.pointer)

@register(name="__")
class BUILD_IN(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars, zfile: ZFile) -> None:
        super().__init__(cmd, activeVars)
        self.value = ZValue("", "PT")

        self.zfile: ZFile = zfile

        self.registerFunc({self.wait: "", self.jump: "", self.jumpTo: "", self.export: "", self.load: "", self.LIB: ""})

    
    # --- Callable Functions  
    
    def wait(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1, True)
        
        waitTime: ZValue = ZValue("0.0", "FLOAT")
        waitTime.setValue(cmd.args[0], activeVars)

        time.sleep(float(waitTime.value))

    def jump(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex] :
        cmd.checkArgs(1, True)
        
        indexToAdd: ZValue = ZValue("0", "INT")

        indexToAdd.setValue(cmd.args[0], activeVars)

        if indexToAdd.value.startswith("-"):
            return activeVars, ZIndex(index-int(indexToAdd.value.replace("-", ""))-1)
        else:
            return activeVars, ZIndex(index+(int(indexToAdd.value)))
            
    
    def jumpTo(self, cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
        cmd.checkArgs(1)
        
        indexToJump: ZValue = ZValue("0", "INT")       
            
        indexToJump.setValue(cmd.args[0], activeVars)

        return activeVars, int(indexToJump.value)-2


    def LIB(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)
        
        userPath = ZValue("", "PT")
        userPath.setValue(cmd.args[0], activeVars)
        userPath = Path(userPath.value)
        
        path: Path | None = None
        module_name = ""
 
        # Path is absolute
        if userPath.is_absolute():
            if userPath.suffix != ".py":
                raise ZError(117)
            path = userPath
            module_name = userPath.stem
        
        # path is relative -> uses relative on cwd
        elif userPath.parts and len(userPath.parts) > 1 or "/" in str(userPath) or "\\" in str(userPath):
            currentFileDir = self.zfile.zphPath.parent
            resolved = (currentFileDir / userPath).resolve()
            if not resolved.exists():
                raise ZError(116)
            if resolved.suffix != ".py":
                raise ZError(117)
            path = resolved
            module_name = resolved.stem
        
        # just name -> absolute then local ./lib 
        else:
            name = userPath
        
            # global
            globalDir = getZephyrPath()
            if globalDir is not None:
                candidate = (globalDir / name).with_suffix(".py").resolve()
                if candidate.exists():
                    path = candidate
                    module_name = candidate.stem
        
            # local ./lib
            if path is None:
                currentFileDir = self.zfile.zphPath.parent
                candidate = (currentFileDir / "lib" / name).with_suffix(".py").resolve()
                if candidate.exists():
                    path = candidate
                    module_name = candidate.stem
        
            if path is None:
                raise ZError(116)
        
        # import the file
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Failed to create spec for {path}")
        
        self.module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = self.module
        
        try:
            spec.loader.exec_module(self.module)
        except FileNotFoundError:
            raise ZError(124)
        
        newTypes: dict[str, type] = self.module.load()
        for name, cls in newTypes.items():
            register(name)(cls)

    def export(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
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
        if cmd.checkArgs(1, False):
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
        self.frames: List[ZValue] = []
        self.doClearScreen: ZValue = ZValue("~0", "BOOL")


        self.firstTimeInit(cmd, activeVars)
                
        self.registerFunc({self.w: "", self.wLIST: "", self.setDelay: "", self.clearScreen: "", self.start: "", self.step: "", self.reset: "", self.setIndex: "", self.display: ""})
        


    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        if cmd.checkArgs(1, False):
            self.w(cmd, activeVars)
            
        if cmd.checkArgs(2, False):
            self.delay.setValue(cmd.args[1], activeVars)
            
        if cmd.checkArgs(3, False):
            self.doClearScreen.setValue(cmd.args[2], activeVars)
                
    def displayFrame(self, pos: int):
       print(self.frames[pos].value)


    # --- Callable Functions  

    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1, True)
        
        self.frames.append(ZValue("", "PT"))
        self.frames[-1].setValue(cmd.args[0], activeVars)

    def wLIST(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1, True)

        listVarName = cmd.args[0]
        listVar = activeVars.get(listVarName)
        if not listVar:
            raise ZError(113)

        if listVar.varType != "LIST":
            raise ZError(113)

        elementsListZValue: List[ZValue] = listVar.posValues  # pyright: ignore[reportAttributeAccessIssue]
        elementsList = []
        for zvalue in elementsListZValue:
            elementsList.append(zvalue.value)

        elements = "".join(elementsList)

        self.frames.append(ZValue(elements, "PT"))
            
    def display(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.displayFrame(int(self.value.value))

    def setDelay(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1)
        self.delay.setValue(cmd.args[0], activeVars) 

    def setIndex(self, cmd: ZCommand, activeVars: ActiveVars) -> None:       
        cmd.checkArgs(1)
        self.value.setValue(cmd.args[0], activeVars)

    def clearScreen(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(1)
        self.doClearScreen.setValue(cmd.args[0], activeVars)

    def start(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        for index in range(int(self.value.value), len(self.frames)):
            self.displayFrame(index)
            time.sleep(float(self.delay.value))
            if self.doClearScreen.asPythonBOOL:
                print('\033[2J\033[H')
            
        self.value = ZValue("0", "INT")
        
    def step(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.displayFrame(int(self.value.value))
        self.value.increment("1", activeVars)
        
    def reset(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.value = ZValue("0", "INT")
