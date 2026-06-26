from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, TypeAlias

from colorama import Back

ActiveVars: TypeAlias = dict[str, Any]
ZIndex: TypeAlias = int



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


class Base:
    def __init__(self) -> None:
        self.functionRegistry: dict[str, Callable[..., Any]] = {}

        
        
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