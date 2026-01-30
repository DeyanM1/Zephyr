# Overview

## Basic Structure

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

--

## Comments

Text after `~` on a line is ignored by the compiler.

**Usage:**

```
a # PT:'HelloWorld'; ~ This is a comment
~ This entire line is a comment
```

---

## Starting Info

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