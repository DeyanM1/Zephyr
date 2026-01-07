from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from colorama import Fore

import functions
from functions import (
    ActiveVars,
    ZBase,
    ZCommand,
    ZError,
    ZFile,
    getRequiredArgs,
)

ZCommandData: list[ZCommand] = []


def lexer(zfile: ZFile) -> list[ZCommand]:
    """
    Parses a .zph file associated with the given ZFile object and extracts commands.

    This function reads the .zph file, processes its content to extract commands, and converts them into
    a list of ZCommand objects. The extracted commands are also serialized into a JSON file at the
    location specified by the ZFile's zsrcPath.

    Args:
        zfile (ZFile): The ZFile object containing paths to the .zph file and other related files.

    Returns:
        list[ZCommand]: A list of ZCommand objects representing the parsed commands from the .zph file.
    """


    compiledData: list[tuple[int, str]] = []
    forbiddenChars = {"\n", "\r"}  # use set for faster lookup

    # Read the file and process commands line by line
    currentCommand = ""
    for lineNum, line in enumerate(zfile.zphPath.read_text().splitlines(), start=1):
        for char in line:
            if char == ";":
                compiledData.append((lineNum, currentCommand))
                currentCommand = ""
            elif char not in forbiddenChars:
                currentCommand += char




    
    # Parse each command into ZCommand objects
    ZCommandData: list[ZCommand] = []
    first, arguments, name, base, func = "", "", "", "", ""
    for line, command in compiledData:
        try:
            first, arguments = command.split(":", 1)
            name, base, func = first.split(" ", 2)
        except ValueError:
            cmd = ZCommand(line, ZFILE, "", "", "", [])
            ZError(104).raiseException(cmd)

        args = arguments.split("|")
        ZCommandData.append(ZCommand(line, ZFILE, name, base, func, args))
    #ZCommandData.append(ZCommand(ZCommandData[-1].lineNum+1, ZFILE, "EOF", "#", "EOF", []))



    # Convert ZCommand objects to JSON-friendly dictionary
    combined_json = {str(cmd.lineNum): asdict(cmd) for cmd in ZCommandData}
    for entry in combined_json.values():
        entry.pop("jsonized", None)
        zfile_dict = entry.get("zfile")
        if zfile_dict:
            if zfile_dict.get("basePath") is not None:
                zfile_dict["basePath"] = str(zfile_dict["basePath"])
            for key in ["zphPath", "zsrcPath", "zpkgPath"]:
                zfile_dict.pop(key, None)



    zfile.zsrcPath.parent.mkdir(parents=True, exist_ok=True)
    zfile.zsrcPath.write_text(json.dumps(combined_json, indent=4))

    return ZCommandData



def compile(inputData: ZFile | list[Any]):
    ## Reform data. Force ZCommandData = list[ZCommand]
    ZCommandData: list[ZCommand]
    match inputData:
        case ZFile():
            data = json.loads(inputData.zsrcPath.read_text())
            
            ZCommandData: list[ZCommand] = []
            for cmd_dict in data.values():
                cmd = ZCommand(
                    lineNum=cmd_dict["lineNum"],
                    zfile=inputData,
                    name=cmd_dict["name"],
                    base=cmd_dict["base"],
                    func=cmd_dict["func"],
                    args=cmd_dict["args"],
                )
                ZCommandData.append(cmd)

        case [*commands] if all(isinstance(cmd, ZCommand) for cmd in commands):
            ZCommandData = inputData
            #print(ZCommandData)

        case _:
            raise TypeError("Input must be a ZFile or a list of ZCommand instances")
       
        

    ## Loop through commands

    

    activeVars: ActiveVars = {"__": functions.typeRegistry["__"](ZCommand(0, ZFILE, "__", ZBase.define, "", [""]))}
    index: int = 0
    while index != len(ZCommandData):

        cmd: ZCommand = ZCommandData[index]





        match cmd.base:
            case "#":
                match cmd.func:

                    case "CT":
                        activeVars = activeVars[cmd.name].functionRegistry[cmd.func](cmd, activeVars)
                    
                    case _:
                        try:
                            var = functions.typeRegistry[cmd.func](cmd)
                            activeVars.update({cmd.name: var})
                        except KeyError:
                            ZError(103).raiseException(cmd)
                        
            
            
        
            case "?":
                if activeVars and cmd.name in activeVars or cmd.name == "__":
                    var = activeVars.get(cmd.name)
                    if var and hasattr(var, "functionRegistry"):
                        if cmd.func not in var.functionRegistry:
                            ZError(103).raiseException(cmd)


                        if "activeVars" in getRequiredArgs(var.functionRegistry[cmd.func]):
                            activeVars = var.functionRegistry[cmd.func](cmd, activeVars)
                        else:
                            var.functionRegistry[cmd.func](cmd)

                else:
                    # Variable not found or declared
                    ZError(102).raiseException(cmd)


            case _:
                # Unknown Base
                ZError(101).raiseException(cmd)
        
        index += 1

    
    
    print(f"\n{Fore.GREEN}Code finished... \n{Fore.MAGENTA}{activeVars}{Fore.RESET}")



if __name__ == "__main__":

    ZFILE: ZFile = ZFile("src/code")

    lexer(ZFILE)
    compile(ZFILE)



