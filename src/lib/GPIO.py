from __future__ import annotations

from typing import Any, Callable

import FakeRPi.GPIO as GPIO  # type: ignore

from lib.base import ActiveVars, ZBool, ZCommand, ZError, ZValue


class gpio:
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        
        self.value = ZBool("~0")

        self.functionRegistry: dict[str, Callable[..., Any]] = {}

        if len(cmd.args) > 0 and cmd.args[0] != "":
            boardType: ZValue = ZValue()
            boardType.setValue(cmd.args[0], "PT", activeVars)
            
            match boardType.value:
                case "BCM":
                    GPIO.setmode(GPIO.BCM) 
                case "BOARD":
                    GPIO.setmode(GPIO.BOARD) 
                case _:
                    print("ERROR: wrong board Type. SUPPORTED: BCM/BOARD")
                    quit()
                

        self.registerFunc({self.SETUP: "", self.SET: "", self.READ: "", self.CLEAN: ""})


    def SETUP(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 1 and cmd.args[1] != "" and cmd.args[0] != "":
            pin: ZValue = ZValue()
            pin.setValue(cmd.args[0], "INT", activeVars)
            
            pinType: ZValue = ZValue()
            pinType.setValue(cmd.args[1], "PT", activeVars)

            match pinType.value:
                case "IN":
                    GPIO.setup(int(pin.value), GPIO.IN) 
                case "OUT":
                    GPIO.setup(int(pin.value), GPIO.OUT) 
                case _:
                    raise ZError(114)
        else:
            raise ZError(114)
    
    def SET(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            pin: ZValue = ZValue()
            pin.setValue(cmd.args[0], "INT", activeVars)
            
            pinValue: ZBool = ZBool()
            pinValue.setValue(cmd.args[1])

            match pinValue.getBool():
                case True:
                    GPIO.output(int(pin.value), GPIO.HIGH) 
                case False:
                    GPIO.output(int(pin.value), GPIO.LOW) 

    def READ(self, cmd: ZCommand, activeVars: ActiveVars):
        pin: ZValue = ZValue()
        pin.setValue(cmd.args[0], "INT", activeVars)


        rawValue = GPIO.input(int(pin.value))

        match rawValue:
            case 1:
                self.value.setValue("~1")
            case 0:
                self.value.setValue("~0")
            case _:
                pass

    def CLEAN(self, cmd: ZCommand, activeVars: ActiveVars):
        GPIO.cleanup()


    def onChange(self) -> str:
        return self.value.value

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
 

def load() -> dict[str, type]:
    return {"": gpio}