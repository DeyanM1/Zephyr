# Zephyr Documentation

## Introduction

Zephyr is a variable-based programming language designed for simplicity and efficiency. In Zephyr, all variables are lowercase, and the syntax is minimalistic, allowing you to define and manipulate variables, perform calculations, and structure your programs using loops, functions, and conditional logic.

---

## Syntax Overview

**Basic Structure:**
```
<VariableName> <Command>:<Argument1>|<Argument2>|...;
```
markdown
Copy code

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
```
__ ? JUMP:<Line>;
```
- **JUMP**: Jumps to a specific function, not a line.

---

## Variables

### Declaring Variables
```
<VariableName> # <Type>:<Value>(|<~1>/<~0>);
```
- **Type**: The data type of the variable.
- **Value**: The initial value of the variable.
- **~1/~0**: Optional flags for constants or special properties.

**Examples:**

- Declare an integer:
counter # INT:10;


- Declare a constant text:
```
message # PT:"Hello World" | ~1;
```

### Changing Type
```
<VariableName> # CT:<Type>;
```

**Example:**

- Change type to Printable Text:
```
counter # CT:PT;
```

### Modifying Values
```
<VariableName> ? w:<Value>;
```


- **Value**: Must be compatible with the variable's type.

**Examples:**

- Increment integer by 1:
```
counter ? w:++;
```

- Decrement integer by 1:
```
counter ? w:--;
```
---

## Input and Output

**Print a value:**
```
<VariableName> ? push:;
```

**Take user input:**
```
<VariableName> ? INPUT:<optional input message>;
```


**Example:**

- Print the value of a variable:
```
message ? push:;
```

---

## Random Number Generator
```
<VariableName> # RNG:<Random number type>|<range>;
```

- **Range**: Format `min->max`, inclusive.

**Example:**

- Generate a random number between 0 and 30:
```
randomValue # RNG|0->30;
```

### Changing Range

```
<VariableName> ? CR:<range>;
```

---

## Math Objects

Math objects allow for complex calculations.

**Declare a Math Object:**
```
<VariableName> # MO:;
```

**Pass an Equation:**
```
<VariableName> ? (<equation>):;
```

- **Equation Format**: `(a + b)` where `a` and `b` are variables or literals.

**Example:**

- Define and use a math object:
```
result # MO:; result ? ('a' + 'b'):;
```

---

## Functions

Functions in Zephyr allow you to encapsulate logic and reuse it.

**Declare a Function:**
```
<VariableName> # FUNC:<returnType>|(~1/~0);
```

- **Return Types**: `RES` (Result)**





You said:
make everything a big .me filec dont split it into junks
ChatGPT said:
ChatGPT
Here is the Zephyr documentation formatted as a single .me file:

markdown
Copy code
# Zephyr Documentation

## Introduction
Zephyr is a variable-based programming language designed for simplicity and efficiency. In Zephyr, all variables are lowercase, and the syntax is minimalistic, allowing you to define and manipulate variables, perform calculations, and structure your programs using loops, functions, and conditional logic.

## Syntax Overview
**Basic Structure:**

<VariableName> <Command>:<Argument1>|<Argument2>|...;

markdown
Copy code

- **Variables**: All variables must be lowercase.
- **Commands**: The command indicates the action to be performed on the variable.
- **Arguments**: The arguments provide the necessary data or parameters for the command.

## Types
- **PT**: Printable Text
- **INT**: Integer
- **MO**: Math Object
- **FUNC**: Function
- **LOOP**: Loops
- **CO**: Conditional Object
- **LIB**: Library

## Commands
- **?**: Used for variable operations (e.g., modifying or retrieving values).
- **#**: Used for declaring variables or changing their types.
- **~**: Used to ignore the entire line (comment).

## Tutorials
### Built-in Functions
Zephyr comes with several built-in functions that can be used without prior definition.

**Example:**

__ ? JUMP:<Line>;

markdown
Copy code

- **JUMP**: Jumps to a specific function, not a line.

## Variables
### Declaring Variables
<VariableName> # <Type>:<Value>(|<~1>/<~0>);

markdown
Copy code
- **Type**: The data type of the variable.
- **Value**: The initial value of the variable.
- **~1/~0**: Optional flags for constants or special properties.

**Examples:**

- Declare an integer:
counter # INT:10;

vbnet
Copy code
- Declare a constant text:
message # PT:"Hello World" | ~1;

shell
Copy code

### Changing Type
<VariableName> # CT:<Type>;

markdown
Copy code

**Example:**

- Change type to Printable Text:
counter # CT
;

shell
Copy code

### Modifying Values
<VariableName> ? w:<Value>;

markdown
Copy code
- **Value**: Must be compatible with the variable's type.

**Examples:**

- Increment integer by 1:
counter ? w:++;

vbnet
Copy code
- Decrement integer by 1:
counter
