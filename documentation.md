
# Zephyr Documentation

## Introduction

Zephyr is a variable-based programming language designed for simplicity and efficiency. In Zephyr, all variables are lowercase, and the syntax is minimalistic, allowing you to define and manipulate variables, perform calculations, and structure your programs using loops, functions, and conditional logic.

---

## Syntax Overview

**Basic Structure:**

```zephyr
<VariableName> <Command>:<Argument1>|<Argument2>|...;
```

- **Variables**: All variables must be lowercase.
- **Commands**: The command indicates the action to be performed on the variable.
- **Arguments**: The arguments provide the necessary data or parameters for the command.

---

## Types

- **PT**: Printable Text
- **INT**: Integer
- **MO**: Math Object
- **FUNC**: Function
- **LOOP**: Loops
- **CO**: Conditional Object
- **LIB**: Library

---

## Commands

- **?**: Used for variable operations (e.g., modifying or retrieving values).
- **#**: Used for declaring variables or changing their types.
- **~**: Used to ignore the entire line (comment).

---

## Tutorials

### Built-in Functions

Zephyr comes with several built-in functions that can be used without prior definition.

**Example:**

```zephyr
__ ? JUMP:<Line>;
```

- **JUMP**: Jumps to a specific function, not a line.

---

## Variables

### Declaring Variables

```zephyr
<VariableName> # <Type>:<Value>(|<~1>/<~0>);
```

- **Type**: The data type of the variable.
- **Value**: The initial value of the variable.
- **~1/~0**: Optional flags for constants or special properties.

**Examples:**

- Declare an integer:
  ```zephyr
  counter # INT:10;
  ```
- Declare a constant text:
  ```zephyr
  message # PT:"Hello World" | ~1;
  ```

### Changing Type

```zephyr
<VariableName> # CT:<Type>;
```

**Example:**

- Change type to Printable Text:
  ```zephyr
  counter # CT:PT;
  ```

### Modifying Values

```zephyr
<VariableName> ? w:<Value>;
```

- **Value**: Must be compatible with the variable's type.

**Examples:**

- Increment integer by 1:
  ```zephyr
  counter ? w:++;
  ```
- Decrement integer by 1:
  ```zephyr
  counter ? w:--;
  ```

---

## Input and Output

**Print a value:**

```zephyr
<VariableName> ? push:;
```

**Take user input:**

```zephyr
<VariableName> ? INPUT:<optional input message>;
```

**Example:**

- Print the value of a variable:
  ```zephyr
  message ? push:;
  ```

---

## Random Number Generator

```zephyr
<VariableName> # RNG:<Random number type>|<range>;
```

- **Range**: Format `min->max`, inclusive.

**Example:**

- Generate a random number between 0 and 30:
  ```zephyr
  randomValue # RNG:INT|0->30;
  ```

### Changing Range

```zephyr
<VariableName> ? CR:<range>;
```

---

## Math Objects

Math objects allow for complex calculations.

**Declare a Math Object:**

```zephyr
<VariableName> # MO:; 
```

**Pass an Equation:**

```zephyr
<VariableName> ? (<equation>):;
```

- **Equation Format**: `(a + b)` where `a` and `b` are variables or literals.

**Example:**

- Define and use a math object:
  ```zephyr
  result # MO:;
  result ? ('a' + 'b'):;
  ```

---

## Functions

Functions in Zephyr allow you to encapsulate logic and reuse it.

**Declare a Function:**

```zephyr
<VariableName> # FUNC:<returnType>|(~1/~0);
```

- **Return Types**: `RES` (Result)
- **~1/~0**: Indicates if the function's behavior changes based on external variable modifications.

**Pass an Equation to a Function:**

```zephyr
<VariableName> ? (<equation>);
```

**Call a Function:**

```zephyr
<VariableName> ? call:;
```

**Example:**

- Create a function that adds two numbers:
  ```zephyr
  addNumbers # FUNC:RES;
  addNumbers ? ('a' + 'b');
  addNumbers ? call:;
  ```

---

## Loops

Loops in Zephyr allow you to repeat actions.

**Declare a Loop:**

```zephyr
<VariableName> # LOOP:<Conditional Object Name>;
```

- **Conditional Object**: Controls the loop’s execution based on a boolean condition.

**End a Loop:**

```zephyr
<VariableName> ? END:;
```

**Example:**

- Create a loop that runs while a condition is true:
  ```zephyr
  repeatLoop # LOOP:condition;
  repeatLoop ? END:;
  ```

---

## Conditional Objects

Conditional objects return boolean values (`~1` for true, `~0` for false) based on conditions.

**Declare a Conditional Object:**

```zephyr
<VariableName> # CO:(<condition>);
```

- **Condition Format**: `(a > b)`

**Example:**

- Create a condition:
  ```zephyr
  isGreater # CO:('a' > 'b');
  ```

---

## Predefined Variables

Predefined variables allow you to define variables in a Python script and use them in Zephyr.

**Load Predefined Variables:**

```zephyr
__ ? PredefVars:<filename>;
```

**Predefined Variable File Structure:**

```json
{
    "<Variable Name>": {
        "type": "<Variable Type>",
        "value": "<Variable Value>",
        "const": false
    }
}
```
- Place predefined variable files in the `lib/` directory.

**Dump Variables used in code**
```zephyr
__ ? DumpVars:<filename>;
```

**Example:**

```zephyr
__ ? PredefVars:examplePredefVars;
__ ? DumpVars:usedVars;
```

---

## Libraries

Libraries in Zephyr allow for the creation of custom functions that extend the language’s capabilities.

**Declare a Library:**

```zephyr
<VariableName> # LIB:<library file name>;
```

**Use a Function from a Library:**

```zephyr
<VariableName> ? <Function>:<Params>;
```

### Creating a Library

**File Structure:**

- Libraries are stored in the `lib/` directory.

```plaintext
lib/
└── exampleLibrary.py
main.py
functions.py
code.lys
```

**Library Code Structure:**

- A search function is necessary to check if statements can be modified.

```python
def search(name, func, base, paramsList, codeLine):
    match func:
        case "?":
            match base:
                case "add10":
                    vars = add10(vars, vars[paramsList[0]])
    return vars

def add10(vars, var):
    a = int(var.value)
    b = a + 10
    var.value = str(b)
    vars.update({var.name: var})
    return vars
```

**Example:**

- Define a function in a custom library and use it in Zephyr:
  ```zephyr
  myLib # LIB:exampleLibrary;
  myVar ? add10:myVar;
  ```

---

## Conclusion

Zephyr is a flexible and powerful language that simplifies variable-based programming. By following the syntax and leveraging built-in functions, loops, conditionals, and libraries, you can build robust programs with ease.
