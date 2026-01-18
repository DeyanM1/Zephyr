from __future__ import annotations

import inspect
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeAlias

from colorama import Back

typeRegistry: dict[str, type] = {}


ActiveVars: TypeAlias = dict[str, "Variable"]
ZIndex: TypeAlias = int


class ZError(Exception):
    def __init__(self, code: int) -> None:
        self.code = code
    
    def process(self, cmd: ZCommand) -> None:
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
            110: lambda: ("[110]  Only INT, PT, FLOAT are in- and decrementable! ", 1, SyntaxError),
            111: lambda: ("[111]  Error in Condition. ", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            112: lambda: ("[112] Given variable isnt correct type!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            113: lambda: ("[113] Given variable isnt defined!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            114: lambda: ("[114] Missing arguments!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
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
        compiledValue = compileValue(newValue, activeVars)
        try:
            if not self.supportedTypes(compiledValue)[targetType]:
                raise ZError(105)
        except KeyError:
            pass
            
        self.value = compiledValue

    def getValueIfVarType(self, targetType: str) -> str|bool:
        # Return value if current Value is supported by target Type
        if self.supportedTypes(self.value)[targetType]:
            return self.value
        else:
            return False

    def increment(self, incrementValue: str, currentType: str, activeVars: ActiveVars) -> None:
        if not self.supportedTypes(incrementValue)[currentType]:
            raise ZError(105)
        
        # Long and complicated statement. Dont know what it does#
        if currentType == "PT":
            if incrementValue == "":
                self.incrementValue = "1"
            
            self.setValue(self.value + (self.value)*int(incrementValue), currentType, activeVars)



        else:
            newValue = float(self.value) + float(incrementValue)
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
        if not var:
            raise ZError(113)
        
        returnValue = var.value.value
    
    return returnValue



class Variable:
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.name = cmd.name
        self.varType = cmd.func

        self.value: Any


        self.const: ZBool = ZBool()
        self.supportedVars: list[str] = [] # Supported Variables to change to


        self.functionRegistry: dict[str, Callable[..., Any]] = {}
        self.registerFunc({self.CT: ""})


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


        newVarCmd: ZCommand = ZCommand(cmd.lineNum, cmd.zfile, cmd.name, ZBase.define, targetVarType, [oldVar.onChange()])
        newVar = typeRegistry[targetVarType](newVarCmd, activeVars)

        activeVars.update({newVar.name: newVar})

        return activeVars
    


    
    #def __repr__(self):
    #    return f"This is {self.name}. Its a {self.varType}"

@register()
class INT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["FLOAT", "PT"]

        self.value: ZValue = ZValue()
        self.value.setValue(cmd.args[0], self.varType, activeVars)
        
        self.registerFunc({self.w: ""})
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if self.const.compiledValue:
            raise ZError(107)


        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)

            case _:
                self.value.setValue(cmd.args[1], self.varType, activeVars)

@register()
class FLOAT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "PT"]

        self.value: ZValue = ZValue()
        self.value.setValue(cmd.args[0], self.varType, activeVars)
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if self.const.compiledValue:
            raise ZError(107)


        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)

            case _:
                self.value.setValue(cmd.args[1], self.varType, activeVars)

@register()
class PT(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = ["INT", "FLOAT"]

        self.value: ZValue = ZValue()
        self.value.setValue(cmd.args[0], self.varType, activeVars)

        self.registerFunc({self.push: "", self.w: "", self.INPUT: ""})
    
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if self.const.compiledValue:
            raise ZError(107)


        match cmd.args[0]:
            case "++":
                self.value.increment(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)
            case "--":
                self.value.decrement(cmd.args[1] if 1 < len(cmd.args) else "1", self.varType, activeVars)

            case _:
                self.value.setValue(cmd.args[1], self.varType, activeVars)
    
    def INPUT(self, cmd: ZCommand, activeVars: ActiveVars):
        newValue = input(cmd.args[0])
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


        if len(cmd.args) > 0:
            if cmd.args[0] != "":
                self.w(cmd, activeVars)



        self.registerFunc({self.w: ""})

        
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        self.rawCondition.setValue(cmd.args[0], "PT", activeVars)
        self.compile(activeVars)

    
    def compile(self, activeVars: ActiveVars) -> None:
        allowedChars: str = "()=!><+-*/"
        inVar = False
        varName = ""
        
        for char in self.rawCondition.value:
            if char == "'":
                if not inVar:
                    inVar = True
                    
                else:
                    self.compiledCondition += compileValue(varName, activeVars)
                    inVar = False
                    varName = ""
                    
            
            if inVar:
                varName += char
                continue
            
            if char in allowedChars:
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
        
        if len(cmd.args) > 1:
            self.conditionalObjectName.setValue(cmd.args[0], "PT", activeVars)
            self.countCommandsInIf.setValue(cmd.args[1], "INT", activeVars)

            conditionalObject = activeVars.get(self.conditionalObjectName.value)

            if isinstance(conditionalObject, CO):
                self.conditionalObjectValue = conditionalObject.value # type: ignore
            else:
                raise ZError(112)
        else:
            raise ZError(114)
            
        self.registerFunc({self.START: "", self.ELSE: "", self.END: ""})

  
    
    def START(self, cmd: ZCommand, index: ZIndex) -> ZIndex:
        newIndex: ZIndex = 0
        if self.conditionalObjectValue.getBool():
            newIndex = index
        elif not self.conditionalObjectValue.getBool():
            newIndex = index + int(self.countCommandsInIf.value)
        
        return newIndex

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
        allowedChars: str = "+-*/%=()"
        inVar = False
        varName = ""

        for char in self.rawEquation.value:
            if char == "'":
                if not inVar:
                    inVar = True
                    
                else:
                    self.compiledEquation += compileValue(varName, activeVars)
                    inVar = False
                    varName = ""
                    
            
            if inVar:
                varName += char
                continue
            
            if char in allowedChars:
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

        if len(cmd.args) > 0 and cmd.args[0]:
            self.returnType = cmd.args[0]
        if len(cmd.args) > 1:
            if cmd.args[1]:
                self.disableVariableChange.setValue(cmd.args[1])
        
    
                
        self.registerFunc({self.w: "", self.call: "call"})
                
    def w(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        mathObject: MO = activeVars.get(cmd.args[0])
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
        allowedChars: str = "+-*/%=()"
        inVar = False
        varName = ""

        for char in self.rawEquation:
            if char == "'":
                if not inVar:
                    inVar = True
                    
                else:
                    self.compiledEquation += compileValue(varName, activeVars)
                    inVar = False
                    varName = ""
                    
            
            if inVar:
                varName += char
                continue
            
            if char in allowedChars:
                self.compiledEquation += char

        self.calculate(activeVars)
    
    def calculate(self, activeVars: ActiveVars) -> None:
        result: float = 0

        try:
            result = eval(self.compiledEquation)
        except Exception: 
            raise ZError(111)
        
        self.value.setValue(str(result), "FLOAT", activeVars)


@register(name="__")
class BUILD_IN(Variable):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.registerFunc({self.wait: ""})

    
    def wait(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        waitTime: ZValue = ZValue()
        waitTime.setValue(cmd.args[0], "FLOAT", activeVars)

        time.sleep(float(waitTime.value))





if __name__ == "__main__":
    import subprocess
    subprocess.call(["python3", "src/main.py"])