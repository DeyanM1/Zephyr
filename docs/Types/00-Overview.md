# Overview

## Declaring Variables
You declare a variable by giving it a name, a type, and an initial value.

- usage:
```zephyr
<VariableName> # <Type>:<Value>|<Param1>|<Param2>|...;
```

- **`<VariableName>`** -> Name of the variable.
- **`Type`** -> Data type of the variable (PT, INT, FLOAT).
- **`<Value>`** -> Data type of the variable (PT, INT, FLOAT).
- **`Value`**: The initial value of the variable.
- **`Param`**: Optional parameters; Multiple parameters can be added, separated by |.


**Examples:**

- Declare an integer:
  ```zephyr
  counter # INT:10;
  ```
- Declare a constant text:
  ```zephyr
  message # PT:"Hello World"|~1;
  ```

## Changing Type
You can change the type of an existing variable with **`# CT:`** operation.
This resets the variable’s value.

- usage:
```zephyr
<VariableName> # CT:<Type>;
```
- **`<VariableName>`** -> Name of the variable.
- **`Type`**: The new variable type; Only compatible types can be changed to

**Example:**

- Change type to Printable Text:
```zephyr
counter # INT:5;
counter # CT:PT;   ~ counter is now a Printable Text variable
```
