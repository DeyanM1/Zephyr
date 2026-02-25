from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from colorama import Fore # type: ignore  # noqa: F401

import functions
from functions import (
    ActiveVars,
    ZBase,
    ZCommand,
    ZError,
    ZFile,
    ZIndex,
    getRequiredArgs,
)


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
    forbiddenChars = {"\n", "\r"}


    # Read file and remove comments, split per line into list
    currentCommand = ""
    for lineNum, line in enumerate(zfile.zphPath.read_text().splitlines(), start=1):
        skipLine: bool = False
        line = line.strip()
        for char in line:
            if char == "§":
                skipLine = True
                currentCommand = ""
                break
            if char == ";":
                compiledData.append((lineNum, currentCommand))
                currentCommand = ""
            elif char not in forbiddenChars:
                currentCommand += char
        if skipLine:
            continue

        if currentCommand:
            compiledData.append((lineNum, currentCommand))
            currentCommand = ""


    # Read compiledData, turn into ZCommands
    ZCommandData: list[ZCommand] = []
    cmd = ZCommand(-1, "", "", "", [""])
    try:
        # Parse each command into ZCommand objects
        ZCommandData: list[ZCommand] = []
        first, arguments, name, base, func = "", "", "", "", ""
        for line, command in compiledData:
            try:
                first, arguments = command.split(":", 1)
                name, base, func = first.lstrip().split(" ", 2)
            except ValueError:
                raise ZError(104)

            args = arguments.split("|")
            ZCommandData.append(ZCommand(line, name, base, func, args))
        #ZCommandData.append(ZCommand(ZCommandData[-1].lineNum+1, ZFILE, "EOF", "#", "EOF", []))
    except ZError as e:
        e.process(cmd, zfile)



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

def compiler(inputData: ZFile) -> None:
    ## Reform data. Force ZCommandData = list[ZCommand]
    ZCommandData: list[ZCommand] = []
    match inputData:
        case ZFile():
            data = json.loads(inputData.zsrcPath.read_text())

            for cmd_dict in data.values():
                cmd = ZCommand(
                    lineNum=cmd_dict["lineNum"],
                    name=cmd_dict["name"],
                    base=cmd_dict["base"],
                    func=cmd_dict["func"],
                    args=cmd_dict["args"],
                )
                ZCommandData.append(cmd)

            """case [*commands] if all(isinstance(cmd, ZCommand) for cmd in commands):
            ZCommandData = inputData
            #print(ZCommandData)"""

        case _:
            raise TypeError("Input must be a ZFile or a list of ZCommand instances")
       
        

    ## Loop through commands

    cmd = ZCommand(-1, "", "", "", [""])
    activeVars: ActiveVars = {}
    activeVars["__"] = functions.typeRegistry["__"](ZCommand(0, "__", ZBase.define, "", [""]), activeVars, inputData)

    index: ZIndex = 0
    try:
        while index < len(ZCommandData):
            cmd: ZCommand = ZCommandData[index]

            activeVars, index = execute(cmd, activeVars, index)
            
            index += 1
    except ZError as e:
        e.process(cmd, inputData)
    

    #print(f"\n{Fore.GREEN}Code finished successfully. \n{Fore.MAGENTA}{activeVars}{Fore.RESET}")

def execute(cmd: ZCommand, activeVars: ActiveVars, index: ZIndex) -> tuple[ActiveVars, ZIndex]:
    match cmd.base:
        case "#":
            if cmd.func not in functions.typeRegistry:
                raise ZError(103)
            
            typeRegVar = functions.typeRegistry[cmd.func]

            hasActiveVars = "activeVars" in getRequiredArgs(typeRegVar)
            hasIndex = "index" in getRequiredArgs(typeRegVar)
            
            if hasActiveVars and not hasIndex:
                var = typeRegVar(cmd, activeVars)
            elif hasActiveVars and hasIndex:
                var = typeRegVar(cmd, activeVars, index)
            else:
                var = typeRegVar(cmd)

            activeVars[cmd.name] = var

        
        
    
        case "?":
            if cmd.name not in activeVars:
                # Variable not found or declared
                raise ZError(102)
            
            var = activeVars.get(cmd.name)

            if not var or not hasattr(var, "functionRegistry"):
                raise ZError(108)
            
            if cmd.func not in var.functionRegistry:
                raise ZError(103)
                
            funcRegVar = var.functionRegistry[cmd.func]

            hasActiveVars = "activeVars" in getRequiredArgs(funcRegVar)
            hasIndex = "index" in getRequiredArgs(funcRegVar)

            newActiveVars = None
            newIndex = None



            if hasActiveVars and not hasIndex:
                newActiveVars = funcRegVar(cmd, activeVars)
            elif hasIndex and not hasActiveVars:
                newIndex = funcRegVar(cmd, index)
            elif hasActiveVars and hasIndex:
                newActiveVars, newIndex = funcRegVar(cmd, activeVars, index)
            else:
                funcRegVar(cmd)
            
            if newActiveVars is not None:
                activeVars = newActiveVars
            if newIndex is not None:
                index = newIndex
                


        case _:
            # Unknown Base
            raise ZError(101)
        
    return (activeVars, index)

if __name__ == "__main__":
    ZFILE: ZFile = ZFile(Path("src/code.zph"))

    lexer(ZFILE)
    compiler(ZFILE)



