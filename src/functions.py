from __future__ import annotations

import inspect
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeAlias

from colorama import Back

typeRegistry: dict[str, type] = {}


ActiveVars: TypeAlias = dict[str, "Variable"]


  

@dataclass
class ZError:
    errorCode: int

    def raiseException(self, cmd: ZCommand) -> None:
        """
        Raises an exception based on the provided error code and command context.

        Args:
            cmd (ZCommand): The command object containing details about the command that caused the error.
            errorCode (int): The error code corresponding to the specific error to raise.

        Raises:
            ValueError: If the provided error code is not recognized.
            SyntaxError: For specific error codes, with detailed context about the error.
        """
        path: Path = cmd.zfile.zphPath
        context: str = path.read_text().splitlines()[cmd.lineNum - 1]

        # errorCode: (message, offset_function)
        errors: dict[int, Callable[..., tuple[str, int, type[BaseException]]]] = {
            101: lambda: (f"[101]  Unknown Base, use  '{ZBase.use}' or '{ZBase.define}'", len(cmd.name) + 2, SyntaxError),
            102: lambda: ("[102]  Undefined Variable ", 1, SyntaxError),
            103: lambda: ("[103]  Unknown Function. Maybe your type is wrong?", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            104: lambda: ("[104]  Wrong command structure. Missing ':' or ';'? ", 1, SyntaxError),
            105: lambda: ("[105]  Variable Type doesn't match given Value ", 1, SyntaxError),
            106: lambda: ("[106]  Invalid Boolean type. Allowed: ~0 | ~1 ", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            107: lambda: ("[107]  Value cannot be changed. Variable is constant! ", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            108: lambda: ("[108]  Current Variable type doenst support new variable type! ", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            109: lambda: (f"[109]  List ({cmd.name}) doesn't support position 0! ", len(f"{cmd.name}")+7, SyntaxError),
            110: lambda: ("[110]  Only INT, PT, FLOAT are in- and decrementable! ", 1, SyntaxError)
        }

        if self.errorCode not in errors:
            raise ValueError(f"Unknown error code: {self.errorCode}")

        message, offset, errorType = errors[self.errorCode]()

        raise errorType(
            f"{Back.RED}{message}{Back.RESET}",
            (str(path), cmd.lineNum, offset, context)
        )
 


@dataclass
class ZFile:
    """
    A class representing a Zephyr file with paths for different file types.

    Attributes:
        rawName (str): The base name of the file without extensions.
        basePath (Path | None): The base directory where the file resides. Defaults to the current working directory.
        zphPath (Path): The path to the .zph file.
        zsrcPath (Path): The path to the .zsrc file.
        zpkgPath (Path): The path to the .zpkg file.
    """
    
    rawName: str = ""
    basePath: Optional[Path] = None

    zphPath: Path = Path()
    zsrcPath: Path = Path()
    zpkgPath: Path = Path()

    def __post_init__(self):
        self.basePath = self.basePath or Path.cwd()
        self.zphPath = self.basePath / f"{self.rawName}.zph"
        self.zsrcPath = self.basePath / f"{self.rawName}.zsrc"
        self.zpkgPath = self.basePath / f"{self.rawName}.zpkg"

    @classmethod
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

        return obj

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
    zfile: ZFile
    name: str
    base: str
    func: str
    args: list[str]

@dataclass
class ZBool:
    rawValue: str = field(default_factory=lambda:"~0")

    lookUpTable: dict[str, bool] = field(default_factory=lambda:{
        "~0": False,
        "~1": True
    })


    @property
    def compiledValue(self) -> bool|ZError:
        return self.lookUpTable[self.rawValue]

    def setValue(self, value: str) -> None|ZError:
        if value not in self.lookUpTable:
            return ZError(106)
        self.rawValue = value

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

    def setValue(self, newValue: str, targetType: str) -> None|ZError:
        try:
            if not self.supportedTypes(newValue)[targetType]:
                return ZError(105)
        except KeyError:
            pass
            
        self.value = newValue

    def getValueIfVarType(self, targetType: str):
        # Return value if current Value is supported by target Type
        if self.supportedTypes(self.value)[targetType]:
            return self.value
        else:
            return False

    def increment(self, incrementValue: str, currentType: str) -> None|ZError:
        error = None
        if not self.supportedTypes(incrementValue)[currentType]:
            return ZError(105)
        
        # Long and complicated statement. Dont know what it does#
        if currentType == "PT":
            if incrementValue == "":
                self.incrementValue = "1"
            
            error = self.setValue(self.value + (self.value)*int(incrementValue), currentType)



        else:
            newValue = float(self.value) + float(incrementValue)
            if currentType == "INT":
                error = self.setValue(str(newValue).split(".")[0], currentType)
            elif currentType == "FLOAT":
                error = self.setValue(str(newValue), currentType)
            else:
                return ZError(110)
        
        return error if error else None

    def decrement(self, decrementValue: str, currentType: str) -> None|ZError:
        error = None
        if not self.supportedTypes(decrementValue)[currentType]:
            return ZError(105)

        if currentType == "PT":
            error = self.setValue("", currentType)

        else:
            newValue = float(self.value) - float(decrementValue)
            if currentType == "INT":
                error = self.setValue(str(newValue).split(".")[0], currentType)
            elif currentType == "FLOAT":
                error = self.setValue(str(newValue), currentType)
            else:
                error = ZError(110)
        


        return error if error else None


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


def matchValueToVar(name: str, activeVars: ActiveVars) -> ZValue:
    
    if name.startswith("'"):
        varName = name.replace("'", "")
        var: Variable = activeVars[varName]

        return var.value

    return ZValue(name)

def compileValue(rawValue: str, activeVars: ActiveVars) -> str:
    # This function ignores the type of the variable!
    # This function returns the raw Value
    returnValue: str = rawValue

    if rawValue.startswith("'"):
        varName = rawValue.replace("'", "")

        var = activeVars.get(varName)
        if var is not None:
            returnValue = var.value.value
    
    return returnValue



class Variable:
    def __init__(self, cmd: ZCommand) -> None:
        self.name = cmd.name
        self.varType = cmd.func

        self.value: ZValue = ZValue()
        error = self.value.setValue(cmd.args[0], self.varType)
        if error: error.raiseException(cmd)  # noqa: E701


        self.const: ZBool = ZBool()
        self.supportedVars: list[str] = [] # Supported Variables to change to


        self.functionRegistry: dict[str, Callable[..., Any]] = {}

        self.registerFunc(self.w)
        self.registerFunc(self.CT)


    def registerFunc(self, func: Callable[..., Any], name: Optional[str] = "") -> Callable[..., Any]:
        """
        Register a function for a type. Its added to the functionRegistry

        Args:
            func (Callable[..., Any]): The function to generate the docstring for.
            name (Optional[str]): The name to use in the docstring. If not provided, the function's name will be used.

        """
        if name:
            self.functionRegistry[name] = func
        else:
            self.functionRegistry[func.__name__] = func
        return func
    
    def onChange(self) -> ZValue:
        """
        Returns the value that is being used for typechanging
        """
        return self.value
        


    def CT(self, cmd: ZCommand, activeVars: ActiveVars) -> ActiveVars:
        targetVarType: str = cmd.args[0]

        if targetVarType not in self.supportedVars:
            ZError(108).raiseException(cmd)

        targetVarType: str = cmd.args[0]

        oldVar: Variable = activeVars[cmd.name]


        newVarCmd: ZCommand = ZCommand(cmd.lineNum, cmd.zfile, cmd.name, ZBase.define, targetVarType, [oldVar.onChange().value])
        newVar = typeRegistry[targetVarType](newVarCmd)

        activeVars.update({newVar.name: newVar})

        return activeVars
    

    def w(self, cmd: ZCommand):
        if self.const.compiledValue:
            ZError(107).raiseException(cmd)


        match cmd.args[0]:
            case "++":
                error = self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType)
            case "--":
                error = self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType)

            case _:
                error = self.value.setValue(cmd.args[1], self.varType)
        if error: error.raiseException(cmd)  # noqa: E701
    
    #def __repr__(self):
    #    return f"This is {self.name}. Its a {self.varType}"

@register()
class INT(Variable):
    def __init__(self, cmd: ZCommand) -> None:
        super().__init__(cmd)
        self.supportedVars = ["FLOAT", "PT"]

@register()
class FLOAT(Variable):
    def __init__(self, cmd: ZCommand) -> None:
        super().__init__(cmd)
        self.supportedVars = ["INT", "PT"]

@register()
class PT(Variable):
    def __init__(self, cmd: ZCommand) -> None:
        super().__init__(cmd)
        self.supportedVars = ["INT", "FLOAT"]

        self.registerFunc(self.push)
    
    
    def push(self, cmd: ZCommand) -> None:
        print(self.value.value)
   
@register()
class CO(Variable):
    def __init__(self, cmd: ZCommand) -> None:
        super().__init__(cmd)

        self.supportedVars = ["INT", "FLOAT", "PT"]

        self.value: ZBool = ZBool("~0")
        self.equation: str = ""
        self.compiledEquation: str = ""


@register(name="__")
class BUILD_IN(Variable):
    def __init__(self, cmd: ZCommand):
        super().__init__(cmd)

        self.registerFunc(self.wait)

    
    def wait(self, cmd: ZCommand, activeVars: ActiveVars) -> ActiveVars:
        value = matchValueToVar(cmd.args[0], activeVars)

        if value.getValueIfVarType("INT") or value.getValueIfVarType("FLOAT"):
            time.sleep(float(value.getValueIfVarType("FLOAT")))

        return activeVars




if __name__ == "__main__":
    import subprocess
    subprocess.call(["python3", "src/main.py"])