# Zephyr Documentation


---
# Table of Contents
1. [Syntax Overview](#syntax-overview)
2. [Types](#types)
3. [Basic info](#basic-info)
4. [Types Explained](#types-explained)  
4.1 [Variables](#variables)  
4.2 [Built-in Functions](#built-in-functions)   
4.3 [List](#lists)  
4.4 [AList](#alists)  
4.5 [Math Object](#math-object)    
4.6 [Function](#function)    
4.7 [Conditional Object](#conditional-object)  
4.8 [Loop](#loop)  
4.9 [Random Number Generator](#random-number-generator)  
4.10 [Predefined Variables](#predefined-variables)  
4.11 [Libraries](#libraries)  
5. [Conclusion](#conclusion)  



## Syntax Overview

**Basic Structure:**

```zephyr
<VariableName> <base> <function>:<Argument1>|<Argument2>|...;
<--------------------------command------------------------->
```


- **VariableName**: The name of the variable, it is user defined
- **base**: The Base of the variable is used to define what is being done to the variable it is language construct:
**?**: Used for variable operations (e.g., modifying or retrieving values).
**#**: Used for declaring variables or changing their types.
- **function**: The function is the thing to be executed as the variable (e.g. printing / defining a function, etc.), its a language construct too
- **arguments**: The arguments are used to pass more information to the function
- **command**: The entire thing combined is called command
---

## Types

- **Variable**: Simple variable Types: (INT, FLOAT, PT)  
- **__**: Built-in Functions
- **LIST**: Lists
- **ALIST**: Allocated Lists
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

  ![](https://github.com/user-attachments/assets/58b3cce4-7ca9-4432-8cd0-45dfd3cda824#gh-dark-mode-only)
  ![](https://github.com/user-attachments/assets/6c7fc8b9-c8f1-450f-bda8-6863f83aa567#gh-light-mode-only)
  ![flowChart2](https://github.com/user-attachments/assets/332dac53-778b-4986-9fe6-67c22719c03e)

### Run a file

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

TODO: Add run .zsrc file in main.py

-----
# Types Explained

## Variables

### Declaring Variables

- usage:
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

Variables **cant** have numbers in them!!

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
- **DUMPING VARIABLES** see below

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
myList # LIST:<ElementsType>|optionalData;
myList ? SET:[POS]|Data;

myList ? SET:'myPosVar'|'myPosValue';

myNum # INT:0;
myNum ? w:'myList<POS>';


```
optionalData Syntax: ..|5,1,5,2
                     ..|test1,test2,test3

---

## ALIST
A Allocated List is a list that does'nt fill spaces between values. It saves memory.
The positioning an Commands are like a normal List.





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


## IF statement

If statements are used to add logic to your program. 

**Declare a IF statement**
```zephyr
statement # IF:<conditionalObjectName>|<commandsInIF>;

statement ? ELSE:;

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

## Conclusion

Zephyr is a flexible and powerful language that simplifies variable-based programming. By following the syntax and leveraging built-in functions, loops, conditionals, and libraries, you can build robust programs with ease.
