# Overview
**Basic Structure:**

```zephyr
<VariableName> <base> <function>:<Argument1>|<Argument2>|...;
<--------------------------command------------------------->
```

- **`VariableName`**: The name of the variable, user-defined.
- **`base`**: The base of the variable, used to define its operation:
  - **`?`**: For variable operations (e.g., modifying or retrieving values).
  - **`#`**: For declaring variables.
- **`function`**: The operation to execute on the variable (e.g., printing, defining a function).
- **`arguments`**: Additional information passed to the function.
- **`command`:** The entire statement.



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
2. Run `zcli.py` located in the `src` directory.
3. Pass the path to your `.zph` file as a parameter.

**Command:**

```
python src/cli.py <path_to_file.zph>
```

### Using the Interactive Shell

1. Run `zcli.py` without any command line arguments:

   ```
   python src/zcli.py
   ```
2. After the shell starts, enter your commands directly in the prompt.

#### Exiting the Shell

* If you type `exit`, the program terminates gracefully and deletes the `.temp.zph` file.
* If you press `Ctrl+C`, the program stops immediately and does not delete temporary files, including `.temp.zph`.

For consistent cleanup of temporary files, exit the shell using the `exit` command instead of interrupting it with `Ctrl+C`.

---

## Comments

Text after `§` on a line is ignored by the compiler.

**Usage:**

```
a # PT:'HelloWorld'; § This is a comment
§ This entire line is a comment
```

---

## Starting Info

* **`*`**: Represents a value that can be a replaced by a variable name (var names must be enclosed in `' '`).
* **`-`**: Represents an optional parameter in the command.
* all parameters in functions are absolute. you **can't change** the order!


## Declaring Variables

You declare a variable by specifying its name, type, and optional initial value:

```
<VariableName> # <Type>:<Value>|<Param1>|<Param2>|...;
```

* **VariableName** – Name of the variable.
* **Type** – Type of the Variable.
* **Value** – Optional initial value of the variable.
* **Param** – Optional parameters separated by `|`.

**Examples:**

```zephyr
counter # INT:10;          § Declare integer
message # PT:"Hello World"|~1;  § Declare constant text
```

---

## Changing Type

Use `? CT:` to change a variable’s type.

Future references of Supported types indicate which types the variable **can be changed into**.
If none is specified type cant be changed.

All variables can be redeclared just be creating a new Variable with the same name

```
<VariableName> ? CT:<NewType>;
```

**Example:**

```zephyr
counter # INT:5;
counter ? CT:PT; § counter is now a Printable Text
```