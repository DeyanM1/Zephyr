# Begginer Info
## Syntax Overview

**Basic Structure:**

```zephyr
<VariableName> <base> <function>:<Argument1>|<Argument2>|...;
<--------------------------command------------------------->
```

- **`VariableName`**: The name of the variable, user-defined.
- **`base`**: The base of the variable, used to define its operation:
  - **`?`**: For variable operations (e.g., modifying or retrieving values).
  - **`#`**: For declaring variables or changing their types.
- **`function`**: The operation to execute on the variable (e.g., printing, defining a function).
- **`arguments`**: Additional information passed to the function.
- **`command`:** The entire statement.

### Comments
adding a **`~`** in a line all text after the character will be ignored.

- usage:
```zephyr
a # PT:HelloWorld; ~ This is a comment
~ This is also a comment
```

### File Extensions
- **.zph**: Zephyr code file.
- **.zsrc**: Zephyr source file for debugging.
- **.zpkg**: Zephyr dumped variables file.

![](https://github.com/user-attachments/assets/58b3cce4-7ca9-4432-8cd0-45dfd3cda824#gh-dark-mode-only)
![](https://github.com/user-attachments/assets/6c7fc8b9-c8f1-450f-bda8-6863f83aa567#gh-light-mode-only)
![flowChart2](https://github.com/user-attachments/assets/332dac53-778b-4986-9fe6-67c22719c03e)

## Run a File

1. Download the installer.bat from the releases tab or the dist library.
2. run the installer as administrator
3. run the command:
```bat
zephyr compile -r <filename>
```
run **`--help`** for more information

## Error Handling

### Error Codes:

1. **[101]** -> Type doesn't have this function.
2. **[102]** -> Unknown variable.
3. **[103]** -> Keyboard interrupt
4. **[110]** -> Current type doesn't support new value or new type.
5. **[201]** -> Only PT type is pushable.
6. **[202]** -> Invalid positional value.
7. **[203]** -> Invalid return function.
8. **[204]** -> Invalid condition or RNG range.
9. **[205]** -> Unable to import library.

**Example Error Message:**
```
[110]: ERROR: {type} != {description} -> unsupported type!
{description} | {name} {base} {function}
```
