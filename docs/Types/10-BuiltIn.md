# Built-In

Built-in commands provide core functionality for program flow control, timing, persistence, and library imports. The built-in variable is always named `__` and its state cannot be changed.

---



## Properties

- **`convertibleInto`** -> `None`
- **`convertValue`** -> None

## Methods

### Wait
Pauses program execution for a specified number of seconds.

```zephyr
__ ? wait:<*SecondsToWait>;
__ ? wait:2;
```

### Jump (Relative)
Moves execution to a relative position in the code (forward or backward).

```zephyr
__ ? jump:<*RelativePositionInCode>;
__ ? jump:5;
```

### Jump To (Absolute)
Moves execution to an absolute line number in the code.

```zephyr
__ ? jumpTo:<*AbsolutePositionInCode>;
__ ? jumpTo:10;
```

### Export
Saves variables to an export file. Defaults to `.zpkg` with the same name as the source file.

```zephyr
__ ? export:<*ExportPath>;  
__ ? export:"variables.zpkg";
```

### Load
Imports variables from a previously exported file.

```zephyr
__ ? load:<*ImportPath>;
__ ? load:"variables.zpkg";
```

### Library (LIB)
Imports and loads an external library file.

```zephyr
__ ? LIB:<*LibFilePath>;
__ ? LIB:"./lib/GPIO.py";
```


## Notes

- The `__` variable is reserved and built-in—it cannot be renamed or redeclared.
- Jump commands count executable lines. Blank lines and comments do not count.
- Export/Load operations use the `.zpkg` format.
- Libraries must be located at the specified file path relative to the current working directory.
- Library files typically have `.py` extensions as they are Python-based.
