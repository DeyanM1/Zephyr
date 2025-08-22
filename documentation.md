# Zephyr Documentation

---
## Table of Contents
- [Zephyr Documentation](#zephyr-documentation)
  - [Table of Contents](#table-of-contents)
- [Begginer Info](#begginer-info)
  - [Syntax Overview](#syntax-overview)
  - [Types](#types)
  - [Basic Info](#basic-info)
    - [Extensions](#extensions)
    - [Run a File](#run-a-file)
- [Error Handling](#error-handling)
  - [Different Error Types](#different-error-types)
- [Types Explained](#types-explained)
  - [Variables](#variables)
    - [Declaring Variables](#declaring-variables)
    - [Changing Type](#changing-type)
    - [Modifying Values](#modifying-values)
    - [Input and Output](#input-and-output)
    - [Variable passthrough](#variable-passthrough)
  - [Built-in Functions](#built-in-functions)
  - [Lists](#lists)
  - [ALIST](#alist)
  - [Math Object](#math-object)
  - [Function](#function)
  - [Function RES](#function-res)
  - [Function VC](#function-vc)
  - [Conditional Object](#conditional-object)
  - [IF Statement](#if-statement)
  - [Loop](#loop)
  - [Random Number Generator](#random-number-generator)
    - [Changing Range](#changing-range)
  - [Predefined Variables](#predefined-variables)
  - [Files](#files)
- [Libraries](#libraries)
    - [Creating a Library](#creating-a-library)
  - [GPIO-Library](#gpio-library)
  - [Conclusion](#conclusion)


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

---

## Types

- **Variable**: Simple variable types (INT, FLOAT, PT).
- **__**: Built-in functions.
- **LIST**: Lists.
- **ALIST**: Allocated lists.
- **MO**: Math object.
- **FUNC**: Function.
- **CO**: Conditional object.
- **LOOP**: Loop.
- **RNG**: Random number generator.
- **PredefVar**: Predefined variable.
- **LIB**: Library.

---

## Basic Info

### Extensions
- **.zph**: Zephyr code file.
- **.zsrc**: Zephyr source file for debugging.
- **.zpkg**: Zephyr dumped variables file.

![](https://github.com/user-attachments/assets/58b3cce4-7ca9-4432-8cd0-45dfd3cda824#gh-dark-mode-only)
![](https://github.com/user-attachments/assets/6c7fc8b9-c8f1-450f-bda8-6863f83aa567#gh-light-mode-only)
![flowChart2](https://github.com/user-attachments/assets/332dac53-778b-4986-9fe6-67c22719c03e)

### Run a File

1. Define the folder containing your Zephyr files in main.py. Ensure the folder is in the current working directory, if nested directories: add the next name with a slash in between.
!WITHOUT THE LAST SLASH!
```python
FILE_LIBRARY = "<FileLibrary>"
```
2. Specify the file name (without the .zph extension) in main.py:
```python
FILE_NAME = "<fileName>"
```
3. Optional: If you are using a custom library folder, define it:
default: lib
```python
LIB_FOLDER_NAME = "<libraryFolderName>"
```
4. Run the file. This will generate a .zsrc file (e.g., exampleFile.zsrc) for debugging. The file is formatted like JSON and can be executed directly.

**TODO:** Add functionality to run `.zsrc` files in `main.py`.

---

# Error Handling

## Different Error Types

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
[110]: ERROR: {type} != {descriptionChild} -> unsupported type!
{description} | {name} {base} {function}
```

---

# Types Explained

## Variables

### Declaring Variables

- usage:
```zephyr
<VariableName> # <Type>:<Value>(|<~1>/<~0>);
```

- **`Type`**: The data type of the variable.
- **`Value`**: The initial value of the variable.

- **`~1/~0`**: Optional flags for constants.

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
- **`Type`**: The new variable type

**Example:**

- Change type to Printable Text:
  ```zephyr
  counter # CT:PT;
  ```

### Modifying Values

- usage:
```zephyr
<VariableName> ? w:<Value>;
<VariableName> ? w:'<VariableName>';
```
- **`Value`**: Must be compatible with the variable's type.
- **`VariableName`**: By entering a VariableName in `' '`, it copies its value

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

### Input and Output

**Print a value:**
Only PT is pushable
- usage:
```zephyr
<VariableName> ? push:;
```

**Take user input:**

- usage:
```zephyr
<VariableName> ? INPUT:<optionalInputMessage>;
```
`optionalInputMessage` can't use `: ;` !

**Example:**

- Print the value of a variable:
  ```zephyr
  message ? push:;
  ```

### Variable passthrough
Many Variable functions or arguments support pass from other variables.

```zephyr
a # PT:;
b # PT:abc;
c # LIST:PT|a,b,c;

~ pass from other variables
a ? w:'b';
a ? w:'c<2>'

```
- pass
to use variables they must be in `' '`.
If the Var is a List you can add `< >` after the variable to enter the position. For more about List: [Lists](#lists)

---

## Built-in Functions

Zephyr comes with several built-in functions that can be used without prior definition.

**Example:**

```zephyr
__ ? JUMP:<Line>;
__ ? WAIT:<Seconds>;
```
- **`JUMP`**: Jumps to a specific function, not a line.
- **`WAIT`**: Wait for a specific amount of second. | INT Variable name support if in `' '`
- **`DUMPING VARIABLES`**: see below

---

## Lists

Lists are variables that hold multiple values of the same type. It will fill spaces between values with null values.
Lists don't support type changes

POS = 1 to +Inf
NEG-POS = -1 to -Inf

OptionalData from 1 to +Inf

Supported types: Variables
**Declare a list:**

- usage:
```zephyr
~ define
myList # LIST:<ElementsType>|optionalData;
myList ? SET:<pos>|<data>;
myList ? SET:'myPosVar'|'myPosValue';

~ read to supported types from a LIST
myNum # INT:0;
myNum ? w:'myList<pos>';
```
- define
**`optionalData Syntax`**: `..|5,1,5,2`  /  `..|test1,test2,test3`
**`pos`**: can be from 1 to +Inf or from -1 to -Inf. | INT, LIST Variable name support if in `' '`
**`data`**: can be any value which the type supports| PT, LIST Variable name support if in `' '`
- read
**`pos`** must be in `< >`
variable name must be in `' '`

---
## ALIST
A Allocated List is a list that does'nt fill spaces between values. It saves memory.
The positioning Commands are like a normal List.

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
*****VC -> Under Construction*****

**Declare a Function:**

- usage:
```zephyr
<VariableName> # FUNC:<returnType>|(~1/~0);
```

- **Return Types**: `RES` (Result); `VC` (Variable changable);
- **~ 1/~0**: Indicates if the function's behavior changes based on external variable modifications.
- **~ 1** Disables variable change!
## Function RES
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

## Function VC
- usage:
```zephyr
<VariableName> ? (<equation>);
```

Variables are notes as v1, v2, ...
**changeInternVariables**
- usage:
```zephyr
  <VariableName> ? VC:<v1>|<v2>|...;
```

**Example**
```zephyr
a # INT:1;
b # INT:2;

a2 # INT:2;
b2 # INT:3;

function # FUNC:VC;
function ? ('v1'+'v2')

function ? VC:a|b;
function ? call:;  -> Result == 3

function ? VC:a2|b2;
function ? call:;   -> Result == 5
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
  isGreater # CO:('a' > 'b');
  ```

## IF Statement

If statements are used to add logic to your program.

**Declare a IF statement**
```zephyr
statement # IF:<conditionalObjectName>|<commandsInIF>;

statement ? ELSE:<commandsInIF>;

statement ? END:;
```

commandsInIF is the count of commands in IF statement

**Example:**
```
conditionalObject # CO:('a' > 'b')

statement # IF:conditionalObject|1;

~ A is greater than b

statement ? ELSE:1;
~ B is greater than A

statement ? END:;
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

## Files

Files are used to open Files from the computer to read and write to it.

**open a file**
```zephyr
<VariableName> # FILE:<fileName>|~1/~0;
```

always creates a File if not existent
`~1` -> delete content of file and open for edit & write
`~0` (default) -> open for edit & write

**Basic actions**
```zephyr
~ Clear a File
<VariableName> ? clear:<lineNumber>;

~ Delete File
<VariableName> ? delete:~0/~1;

~ Rename a File
<VariableName> ? rename:<newName>|~1/~0;

~ close and repoen a File after editing
<VariableName> ? close:;
<VariableName> ? reopen:;
```
- clear:
`<lineNumber>` -> optional line Number to clear | Variable name supported in `' '`
- delete:
`~1` -> delete only if empty
`~0` (default) -> force delete
- rename:
`~1` -> delete content
`~0` (default) -> keep content

**Write**
```zephyr
~ write to a specific Line
<VariableName> ? w:<pos>|<value>;

~ append to the file
<VariableName> ? a:<value>;

~ insert to the file
<VariableName> ? i:<pos>|<value>;

~ replace a file
<VariableName> ? rep:<listName>|<startingIndex>;
```
- write
`pos` can be every number from 1 | INT Variable names supported in `' '`
`value` can be every char combination except `; ' :` | PT Variable names supported in `' '`
- append
appends always to one after the last line
`value` can be every char combination except `; ' :` | PT Variable names supported in `' '`
- insert
insert a value in a line shifting all values after the pos to the right
`pos` can be every number from 1 | INT Variable names supported in `' '`
`value` can be every char combination except `; ' :` | PT Variable names supported in `' '`
- replace
replaces an entire File with a List
`listName` -> Name of the list variable in `' '`
`startingIndex` -> optional starting index to start replacing with a shift | INT Variable name support

**Read**


---

# Libraries

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
├── code.zpkg
└── exampleLibrary.py
main.py
functions.py
code.zsrc
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


## GPIO-Library

- usage:
```zephyr
GPIO # LIB:GPIO; ~ import GPIO library
GPIO # INIT:<BoardMode>; ~ BCM or BOARD

GPIO ? SETUP:<PIN>|<Mode>; ~ IN or OUT

GPIO ? SET:<PIN>|<value>; ~ LOW or HIGH
```
- write to Pins:
```zephyr
GPIO # LIB:GPIO;
GPIO # INIT:BCM;

GPIO ? SETUP:4|OUT;
GPIO ? SET:4|HIGH;
```

- read from Pins:
```zephyr
output # INT:0;
GPIO # LIB:GPIO;
GPIO # INIT:BCM;

GPIO ? SETUP:4|IN;
GPIO ? READ:4|output
```

## Conclusion

Zephyr is a flexible and powerful language that simplifies variable-based programming. By following the syntax and leveraging built-in functions, loops, conditionals, and libraries, you can build robust programs with ease.
