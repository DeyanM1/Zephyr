# Zephyr Documentation

Welcome to the Zephyr documentation. This guide uses specific notation to help you understand the syntax requirements for each command:

* **`*`**: Represents a value that can be a variable name (must be enclosed in `' '`).
* **`-`**: Represents an optional parameter in the current command.

# Beginner Info

## Syntax Overview

### Basic Structure

Zephyr follows a strict command structure to ensure clarity in operations:

`<VariableName> <base> <function>:<Argument1>|<Argument2>|...;`
`<---------------------------command------------------------->`

* **VariableName**: The name of the variable, user-defined.
* **base**: The base of the variable, used to define its operation:
* `#`: For declaring variables or changing their types.
* `?`: For variable operations (e.g., modifying or retrieving values).


* **function**: The operation to execute on the variable (e.g., printing, defining a function).
* **arguments**: Additional information passed to the function.
* **command**: The entire statement.

### Comments

Adding a `~` in a line will cause all text after the character to be ignored by the compiler.

**Usage:**
`a # PT:'HelloWorld'; ~ This is a comment`
`~ This is also a comment`

---

## File Extensions

* **.zph**: Zephyr code file.
* **.zsrc**: Zephyr source file for debugging.
* **.zpkg**: Zephyr dumped variables file.


![](https://github.com/user-attachments/assets/58b3cce4-7ca9-4432-8cd0-45dfd3cda824#gh-dark-mode-only)
![](https://github.com/user-attachments/assets/6c7fc8b9-c8f1-450f-bda8-6863f83aa567#gh-light-mode-only)
![flowChart2](https://github.com/user-attachments/assets/332dac53-778b-4986-9fe6-67c22719c03e)

---

## Run a script
To execute a Zephyr script, you must run the `cli.py` file located inside the `src` directory.

Locate your `.zph` script.

Execute `cli.py` via your terminal.

Pass the path to your `.zph` file as a parameter (this can be an absolute path or a relative path from your current working directory).

Command Format: `python src/cli.py <path_to_file.zph>`



---
## Simple Variable

**Types supported:** `INT`, `PT`, `FLOAT`

`var # <Vartype>:<*- Value>;`
Defines a simple variable.

`var ? w:<*NewValue>;`
Changes the current value.

`var ? w:++|<*- incrementBy>;`
Increments `INT` or `FLOAT` values. If `incrementBy` is not set, it defaults to 1.

`var ? w:-|<*- decrementBy>;`
Decrements `INT` or `FLOAT` values. If `decrementBy` is not set, it defaults to 1.

`var ? push:;`
Prints the current value of a `PT` variable to the console.

`var ? INPUT:<*- Message>;`
Takes user input and overrides the previous value. The `optionalMessage` is printed before input is taken.

---

## Conditional Object

**Types supported:** `INT`, `PT`, `FLOAT`
**Behavior:** The value is the evaluation of the condition.

`co # CO:<*- ConditionScript>;`
Defines a Conditional Object.

`co ? w:<*conditionScript>;`
Changes the existing condition script.

**Condition Format:** `('a' > 'b')`

---

## IF-Statement

**Behavior:** The variable name/state cannot be changed once defined.

`if # IF:<*- ConditionalObjectName>;`
Defines an IF statement based on a specific Conditional Object.

`if ? w:<*ConditionalObjectName>;`
Changes the Conditional Object being checked.

`if ? START:<*commandsInIF>;`
Defines the start of the commands to execute if the condition is met.

`if ? ELSE:<*commandsInELSE>;`
Defines the commands to execute if the condition is not met.

`if ? END:;`
Finalizes the IF block.

---

## LOOP

**Types supported:** `INT`, `PT`, `FLOAT`
**Behavior:** Value represents the total count of times looped.

`loop # LOOP:<*- conditionalObjectName>;`
Defines a loop based on a Conditional Object.

`loop ? w:<*ConditionalObjectName>;`
Changes the Conditional Object that controls the loop.

`loop ? START:<*commandsInLOOP>;`
Begins the block of commands to be repeated.

`loop ? END:;`
Ends the loop block.

---

## Math Object

**Types supported:** `INT`, `PT`, `FLOAT`
**Behavior:** Value is the result of the equation. Result is calculated whenever the script is set or changed.

`mo # MO:<*- equationScript>;`
Defines a Math Object with an equation script.

`mo ? w:<* equationScript>;`
Updates the equation script and recalculates the result.

---

## Function

**Types supported:** `INT`, `PT`, `FLOAT`
**Behavior:** Value is the result of the equation. Result is calculated only when called.

`func # FUNC:<resultType>|<*- disableVariableChange>|<*- mathObjectName>;`
Defines a Function.

`func ? w:<* mathObjectName>;`
Changes the Math Object associated with the function.

`func ? call:;`
Executes the function.

---

## Random Number Generator

**Types supported:** `INT`, `PT`, `FLOAT`
**Behavior:** Value is a generated random number.

`rng # RNG:<*- rangeMin>|<*- rangeMax>|<*- numberType>;`
Defines a Random Number Generator.

`rng ? w:<* rangeMin>|<* rangeMax>|<* numberType>;`
Changes the RNG parameters.

---

## __ (BuiltIn)

**Behavior:** Variable state cannot be changed. This object does not need to be defined; the name is always `__`.

`__ ? wait:<* secondsToWait>;`
Pauses execution for a specified duration.

`__ ? jump:<* relativePositionInCode>;`
Moves execution to a position relative to the current line.

`__ ? jumpTo:<* absolutePositionInCode>;`
Moves execution to a specific line number.

`__ ? export:<*- exportPath>;`
Exports all currently used variables. If `exportPath` is unset, the output file uses the `.zph` filename with a `.zpkg` extension.

`__ ? load:<*- importPath>;`
Imports variables saved in a `.zpkg` file.

`__ ? LIB:<* libFilePath>;`
Imports a library from a Python (`.py`) file.

---

## File management

**Behavior:** Variable state cannot be changed. The value is the absolute path of the opened file.

`file # FILE:<*- path>;`
Opens a file. If no path is provided, it defaults to `unnamed_file.txt` in the current working directory.

`file ? w:<* path>;`
Changes the target file path.

`file ? cSET:<* content>;`
Replaces all existing content in the file with the new content provided.

`file ? cFLUSH:;`
Clears all content from the file.

`file ? gRENAME:<* newName>;`
Renames the current file.

`file ? gDEL:;`
Deletes the current file.

---

## GPIO

**Behavior:** Value represents the status of the last read pin.

`lib # LIB:GPIO;`
Required step to import the GPIO library before use.

`gpio # GPIO:<* pinoutType>;`
Defines the GPIO setup. `pinoutType` must be `BCM` or `Board`.

`gpio ? SETUP:<* pinNum>|<* pinType>;`
Configures a pin. `pinType` is either `IN` or `OUT`.

`gpio ? SET:<* pinNum>|<* pinValue>;`
Sets a pin value (1 for HIGH, 0 for LOW).

`gpio ? READ:<* pinNum>;`
Reads the value of a pin (requires the pin to be set to `IN`).

`gpio ? CLEAN:;`
Cleans all pins. Recommended for use after operations are finished.
