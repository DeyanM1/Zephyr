from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, TypeAlias

from colorama import Back

ActiveVars: TypeAlias = dict[str, Any]
ZIndex: TypeAlias = int



def compileValue(rawValue: str, activeVars: ActiveVars) -> str:
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
            106: lambda: ("[106]  Invalid Boolean type. Allowed: ~0 | ~1 ", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            107: lambda: ("[107]  Value cannot be changed. Variable is constant! ", len(f"{cmd.name} {cmd.base} "), SyntaxError),
            108: lambda: ("[108]  Current Variable type doesnt support new variable type! ", len(f"{cmd.name} {cmd.base} {cmd.func} "), SyntaxError),
            109: lambda: (f"[109]  List ({cmd.name}) doesn't support position 0! ", len(f"{cmd.name}")+7, SyntaxError),
            110: lambda: ("[110]  Only INT, PT, FLOAT are in- and decrementable! ", 1, SyntaxError),
            111: lambda: ("[111]  Error in Condition. ", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            112: lambda: ("[112] Given variable isnt correct type!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            113: lambda: ("[113] Given variable isnt defined!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            114: lambda: ("[114] Error in arguments!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError),
            115: lambda: ("[115] Error at jump function! Index out of range!", len("f"), SyntaxError),
            116: lambda: ("[116] zpkg file cannot be found!", len(f"{cmd.name} {cmd.base} {cmd.func}  "), SyntaxError)
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

