from __future__ import annotations


# from base import ZCommand, ActiveVars, Base, ZValue, ZError 


def importHandler(names: list[str]):
    import importlib.util
    from pathlib import Path
    import sys

    base_path = Path(__file__).resolve().parent / "base.py"

    moduleName = base_path.stem

    spec = importlib.util.spec_from_file_location(moduleName, base_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create spec for {base_path}")


    base = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = base
    spec.loader.exec_module(base)

    for name in names:
        globals()[name] = getattr(base, name)

importHandler(["ZCommand", "ActiveVars", "Base", "ZValue", "ZError"])




class ASCII(Base):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)

        self.registerFunc({self.ToAscii: "", self.ToNum: ""})


    def ToAscii(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(2)
        valueToConvert = ZValue("0", "INT")
        targetVarName = ZValue("", "PT")

        valueToConvert.setValue(cmd.args[0], activeVars)
        targetVarName.setValue(cmd.args[1], activeVars)


        char = chr(int(valueToConvert.value))
        targetVar = activeVars.get(targetVarName.value) 
        if not targetVar:
            raise ZError(113)
            
        targetVar.value.value = char  # pyright: ignore[reportOptionalMemberAccess]

        activeVars.update({targetVarName.value: targetVar})

        return activeVars
        
    def ToNum(self, cmd: ZCommand, activeVars: ActiveVars):
        charToConvert = ZValue("0", "PT")
        targetVarName = ZValue("", "PT")

        charToConvert.setValue(cmd.args[0], activeVars)
        targetVarName.setValue(cmd.args[1], activeVars)


        char = str(ord(charToConvert.value))
        targetVar = activeVars.get(targetVarName.value) 
        if not targetVar:
            raise ZError(113)
            
        targetVar.value.value = char  # pyright: ignore[reportOptionalMemberAccess]

        activeVars.update({targetVarName.value: targetVar})

        return activeVars



def load() -> dict[str, type]:
    return {"": ASCII}