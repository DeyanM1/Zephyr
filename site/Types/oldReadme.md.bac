# Zephyr Documentation

---

# Beginner Info

## Syntax Overview

### Basic Structure

Zephyr commands follow a strict structure:

```
<VariableName> <base> <function>:<Argument1>|<Argument2>|...;
<---------------------------command------------------------->
```

* **VariableName**: User-defined name of the variable.
* **base**: Determines the operation type:

  * `#` – Declare a variable or change its type.
  * `?` – Operate on an existing variable (e.g., modify or retrieve values).
* **function**: The specific operation to execute.
* **arguments**: Additional information passed to the function.
* **command**: Complete statement executed by Zephyr.

---

### Comments

Text after `~` on a line is ignored by the compiler.

**Usage:**

```
a # PT:'HelloWorld'; ~ This is a comment
~ This entire line is a comment
```

---

## File Extensions

* **.zph** – Zephyr script file.
* **.zsrc** – Zephyr source file for debugging.
* **.zpkg** – Dumped variables file.


![](https://github.com/user-attachments/assets/58b3cce4-7ca9-4432-8cd0-45dfd3cda824#gh-dark-mode-only)
![](https://github.com/user-attachments/assets/6c7fc8b9-c8f1-450f-bda8-6863f83aa567#gh-light-mode-only)
![flowChart2](https://github.com/user-attachments/assets/332dac53-778b-4986-9fe6-67c22719c03e)


---

## Running a Script

1. Locate your `.zph` script.
2. Run `cli.py` located in the `src` directory.
3. Pass the path to your `.zph` file as a parameter.

**Command:**

```
python src/cli.py <path_to_file.zph>
```

---

# Overview

* **`*`**: Represents a value that can be a variable name or input (must be enclosed in `' '` where specified).
* **`-`**: Represents an optional parameter in the command.


## Declaring Variables

Declare a variable by specifying its name, type, and initial value:

```
<VariableName> # <Type>:<Value>|<Param1>|<Param2>|...;
```

* **VariableName** – Name of the variable.
* **Type** – Data type (`PT`, `INT`, `FLOAT`).
* **Value** – Initial value of the variable.
* **Param** – Optional parameters separated by `|`.

**Examples:**

```zephyr
counter # INT:10;          ~ Declare integer
message # PT:"Hello World"|~1;  ~ Declare constant text
```

---

## Changing Type

Use `# CT:` to change a variable’s type. This resets its value.

Supported types indicate which types the variable **can be changed into**.

```
<VariableName> # CT:<Type>;
```

**Example:**

```zephyr
counter # INT:5;
counter # CT:PT; ~ counter is now a Printable Text
```


---

# Types

## Simple Variable

Supported types: `INT`, `PT`, `FLOAT`

* Define:

```
var # <Vartype>:<*Value>;
```

* Update value:

```
var ? w:<*NewValue>;
```

* Increment (INT/FLOAT):

```
var ? w:++|<*incrementBy>;   ~ Defaults to 1 if not set
```

* Decrement (INT/FLOAT):

```
var ? w:-|<*decrementBy>;    ~ Defaults to 1 if not set
```

* Print PT value:

```
var ? push:;
```

* Take input:

```
var ? INPUT:<*Message>;      ~ Overrides previous value
```

---

## Conditional Object

Supported types: `INT`, `PT`, `FLOAT`

* Define:

```
co # CO:<*ConditionScript>;
```

* Update:

```
co ? w:<*ConditionScript>;
```

**Condition format example:**

```
('a' > 'b')
```

---

## IF-Statement

Once defined, the variable name/state cannot be changed.

* Define:

```
if # IF:<*ConditionalObjectName>;
```

* Change condition:

```
if ? w:<*ConditionalObjectName>;
```

* Start block:

```
if ? START:<*commandsInIF>;
```

* Else block:

```
if ? ELSE:<*commandsInELSE>;
```

* End IF block:

```
if ? END:;
```

---

## LOOP

Supported types: `INT`, `PT`, `FLOAT`
Value represents the number of iterations.

* Define:

```
loop # LOOP:<*ConditionalObjectName>;
```

* Change condition:

```
loop ? w:<*ConditionalObjectName>;
```

* Start loop block:

```
loop ? START:<*commandsInLOOP>;
```

* End loop block:

```
loop ? END:;
```

---

## Math Object

Supported types: `INT`, `PT`, `FLOAT`
Value is calculated whenever the script is set or changed.

* Define:

```
mo # MO:<*EquationScript>;
```

* Update:

```
mo ? w:<*EquationScript>;
```

---

## Function

Supported types: `INT`, `PT`, `FLOAT`
Value is calculated only when called.

* Define:

```
func # FUNC:<ResultType>|<*disableVariableChange>|<*MathObjectName>;
```

* Change Math Object:

```
func ? w:<*MathObjectName>;
```

* Call function:

```
func ? call:;
```

---

## Random Number Generator

Supported types: `INT`, `PT`, `FLOAT`

* Define:

```
rng # RNG:<*RangeMin>|<*RangeMax>|<*NumberType>;
```

* Update:

```
rng ? w:<*RangeMin>|<*RangeMax>|<*NumberType>;
```

---

## Built-in (`__`)

Variable state cannot be changed. Always named `__`.

* Wait:

```
__ ? wait:<*SecondsToWait>;
```

* Jump relative:

```
__ ? jump:<*RelativePositionInCode>;
```

* Jump absolute:

```
__ ? jumpTo:<*AbsolutePositionInCode>;
```

* Export variables:

```
__ ? export:<*ExportPath>;  ~ Defaults to `.zpkg` matching `.zph` filename
```

* Import variables:

```
__ ? load:<*ImportPath>;
```

* Import library:

```
__ ? LIB:<*LibFilePath>;
```

---

## File Management

Variable state cannot be changed. Value is the absolute path.

* Open file:

```
file # FILE:<*Path>;  ~ Defaults to 'unnamed_file.txt'
```

* Change file path:

```
file ? w:<*Path>;
```

* Set file content:

```
file ? cSET:<*Content>;
```

* Clear file content:

```
file ? cFLUSH:;
```

* Rename file:

```
file ? gRENAME:<*NewName>;
```

* Delete file:

```
file ? gDEL:;
```

---

## GPIO

Value represents the status of the last read pin.

* Import GPIO library:

```
__ ? LIB:./lib/GPIO.py;
```

* Define GPIO setup:

```
gpio # GPIO:<*PinoutType>;   ~ PinoutType: BCM or Board
```

* Configure pin:

```
gpio ? SETUP:<*PinNum>|<*PinType>;   ~ PinType: IN or OUT
```

* Set pin value:

```
gpio ? SET:<*PinNum>|<*PinValue>;   ~ PinValue: 1 (HIGH) or 0 (LOW)
```

* Read pin value:

```
gpio ? READ:<*PinNum>;   ~ Requires pin set to IN
```

* Clean all pins:

```
gpio ? CLEAN:;
```