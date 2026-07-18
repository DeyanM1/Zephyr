from __future__ import annotations
import sys
from pathlib import Path


# from base import ZError, ZCommand, ActiveVars, ZValue, Base    # <- for debugging. Use importHandler for final Project!


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

importHandler(["Base", "ZError", "ZCommand", "ActiveVars", "ZValue"])


class SYSTEM(Base):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
                

        self.registerFunc({self.quit: "", self.getCWD: ""})


    def quit(self, cmd: ZCommand, activeVars: ActiveVars):
        errorCode = ZValue("0", "INT")

        cmd.checkArgs(1)
        errorCode.setValue(cmd.args[0], activeVars)


        sys.exit(int(errorCode.value))

    def getCWD(self, cmd:ZCommand, activeVars: ActiveVars) -> ActiveVars:
        varName = ZValue("", "PT")

        cmd.checkArgs(1, True)
        varName.setValue(cmd.args[0], activeVars)
        
        path = Path.cwd()
        path = path.absolute()

        var = activeVars.get(varName.value)
        
        if not var:
            raise ZError(113)

        var.value.setValue(str(path), activeVars)

        activeVars.update({var.name: var})
        

        return activeVars

    
 

def load() -> dict[str, type]:
    return {"": SYSTEM}
