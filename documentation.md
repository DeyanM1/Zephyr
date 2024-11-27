
# Zephyr Documentation


---
# Table of Contents
1. [Syntax Overview](#syntax-overview)
2. [Types](#types)
3. [Basic info](#basic-info)
4. [Types Explained](#types-explained)
-- [Variables](#variables)
-- [Built-in Functions](#built-in-functions)
-- [Math Object](#math-object)
-- [Function](#function)
-- [Conditional Object](#conditional-object)
-- [Loop](#loop)
-- [Random Number Generator](#random-number-generator)
-- [Predefined Variables](#predefined-variables)
-- [Libraries](#libraries)
5. [Conclusion](#conclusion)



## Syntax Overview

**Basic Structure:**

```zephyr
<VariableName> <base> <function>:<Argument1>|<Argument2>|...;
<--------------------------command------------------------->
```


- **variableName**: The name of the variable
- **base**: The Base of the variable is used to define what is being done to the var:
**?**: Used for variable operations (e.g., modifying or retrieving values).
**#**: Used for declaring variables or changing their types.
- **function**: The function is the ht thing to be executed as the var (e.g. printing / defining a function, etc.)
- **arguments**: The arguments are used to pass more information to the function
- **command**: The entire thing combined is called command
---

## Types

- **Variable**: Simple variable Types: (INT, FLOAT, PT)
- **__**: Built-in Functions
- **MO**: Math Object
- **FUNC**: Function
- **CO**: Conditional Object
- **LOOP**: Loop
- **RNG**: Random Number Generator
- **PredefVar**: Predefined variable
- **LIB**: Library

---

## Basic Info

### Extensions
- **.zph**: The Zephyr code file                   (Zephyr code)
- **.zsrc**: The Zephyr source file, for debugging (Zephyr source)
- **.zpkg**: The Zephyr dumped variables file      (Zephyr package)

### Run a file

To run a file, first specify the folder in the main.py file, it has to be in the current working directory, if nested directories: add the next name with a slash in between.
!WITHOUT THE LAST SLASH!
```python
FILE_LIBRARY = "<FileLibrary>"
```
Now specify the file name in the main.py file, it has to be in the directory specified above
!Without the .zph extension!
```python
FILE_NAME = "<fileName>"
```
Optional: Specify the library folder name in the main.py file
default: lib
```python
LIB_FOLDER_NAME = "<libraryFolderName>"
```

After running the file, a new file has been created: <fileName>.zsrc 
its a Zephyr source file, it can be used to debug files more affective.
And its formatted like a .json file.
It can be run alone
TODO: Add run .zsrc file in main.py

-----
# Types Explained

## Variables

### Declaring Variables

- usage
```zephyr
<VariableName> # <Type>:<Value>(|<~1>/<~0>);
```

- **Type**: The data type of the variable.
- **Value**: The initial value of the variable.
- **~1/~0**: Optional flags for constants.

**Examples:**

- Declare an integer:
  ```zephyr
  counter # INT:10;
  ```
- Declare a constant text:
  ```zephyr
  message # PT:"Hello World"|~1;
  ```

### Changing Type

- usage:
```zephyr
<VariableName> # CT:<Type>;
```
- **Type**: The new variable type

**Example:**

- Change type to Printable Text:
  ```zephyr
  counter # CT:PT;
  ```

### Modifying Values

- usage:
```zephyr
<VariableName> ? w:<Value>;
<VariableName> ? w:<VariableName>;
```
- **Value**: Must be compatible with the variable's type.
- **VariableName**: By entering a VariableName, it copies its value

**Incrementing:**

- Increment integer or Float by 1 (1.0):
  ```zephyr
  counter ? w:++;
  ```
- Decrement integer or Float by 1 (1.0):
  ```zephyr
  counter ? w:--;
  ```
- Increment PT:
  ```zephyr
  printableText # PT:HelloWorld;
  printableText ? w:++;
  ```
  printableText after increment: HelloWorldHelloWorld




## Input and Output

**Print a value:**

- usage:
```zephyr
<VariableName> ? push:;
```

**Take user input:**

- usage:
```zephyr
<VariableName> ? INPUT:<optional input message>;
```

**Example:**

- Print the value of a variable:
  ```zephyr
  message ? push:;
  ```

---

## Built-in Functions

Zephyr comes with several built-in functions that can be used without prior definition.

**Example:**

```zephyr
__ ? JUMP:<Line>;
```
- **JUMP**: Jumps to a specific function, not a line.
- **DUMPING VARS** see below

---

## Math Object

Math objects allow for complex calculations.

**Declare a Math Object:**

- usage:
```zephyr
<VariableName> # MO:; 
<VariableName> # MO:(<equation>);
```

**Pass an Equation:**

- usage:
```zephyr
<VariableName> ? (<equation>):;
```
- **Equation Format**: `(a + b)` where `a` and `b` are variables.

**Example:**

- usage:
- Define and use a math object:
  ```zephyr
  result # MO:;
  result ? ('a' + 'b'):;
  ```

---

## Function

Functions in Zephyr allow you to encapsulate logic and reuse it.

**Declare a Function:**

- usage:
```zephyr
<VariableName> # FUNC:<returnType>|(~1/~0);
```

- **Return Types**: `RES` (Result)
- **~ 1/~0**: Indicates if the function's behavior changes based on external variable modifications.

**Pass an Equation to a Function:**

- usage:
```zephyr
<VariableName> ? (<equation>);
```

**Call a Function:**

- usage:
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


## Conditional Object

Conditional objects return boolean values (`~1` for true, `~0` for false) based on conditions.

**Declare a Conditional Object:**

```zephyr
<VariableName> # CO:;
<VariableName> # CO:(<condition>);
```

- **Condition Format**: `(a > b)`

**Example:**

- Create a condition:
  ```zephyr
  isGreater # ('a' > 'b'):;
  isGreater # CO:('a' > 'b');
  ```

## Loop

Loops in Zephyr allow you to repeat actions.

**Declare a Loop:**

- usage:
```zephyr
<VariableName> # LOOP:<Conditional Object Name>;
```

- **Conditional Object**: Controls the loop’s execution based on a boolean condition.

**End a Loop:**

- usage:
```zephyr
<VariableName> ? END:;
```

**Example:**

- Create a loop that runs while a conditionObject is true:
  ```zephyr
  repeatLoop # LOOP:<conditionalObject>;
  repeatLoop ? END:;
  ```

----

## Random Number Generator

- usage:
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

- usage:
```zephyr
<VariableName> ? CR:<range>;
```

-----

## Predefined Variables

Predefined variables allow you to define variables in a json script and use them in Zephyr.

**Load Predefined Variables:**

```zephyr
__ ? predefVars:<filename>;
```

**Predefined Variable File Structure:**

The file extension is .zpkg
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


!Without Extension!
**Dump Variables used in code**
```zephyr
__ ? dumpVars:<filename>;
```

**Example:**

```zephyr
__ ? predefVars:examplePredefVars;
__ ? dumpVars:usedVars;
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
code.zph
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
