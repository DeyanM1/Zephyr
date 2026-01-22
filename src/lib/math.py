from __future__ import annotations

import math
from typing import Any, Callable

from lib.base import ZCommand, ActiveVars

class MoreMath:
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        
        self.functionRegistry: dict[str, Callable[..., Any]] = {}

        self.registerFunc({self.fact: ""})

    def fact(self, cmd: ZCommand, activeVars: ActiveVars):
        var1 = activeVars.get(cmd.args[0])

        var1.value.setValue(str(math.factorial(int(var1.value.value))), "INT", activeVars) # type: ignore

        activeVars.update({var1.name: var1}) # type: ignore
        return activeVars

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
 

def load() -> list[type]:
    return [MoreMath]