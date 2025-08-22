# Simple Variables

Simple variables in Zephyr hold basic values.
There are three types:

- **`PT`**: Printable Text (strings of characters)
- **`INT`**: Integer (whole numbers)
- **`FLOAT`**: Floating-point number (decimal values)

### PT (Printable Text)
Represents a sequence of characters.

- usage:
```zephyr
myText # PT:HelloWorld!~|0;
```
- Parameters:
  - **`|~0`** → Marks the variable as non-constant (default).
  - **`|~1`** → Marks the variable as constant (value cannot change).


### INT (Integer)

Represents whole numbers without decimals.
- usage:
```zephyr
myText # INT:123;
```
- **Valid Values**: Positive or negative whole numbers (e.g., 0, 42, -99).

### FLOAT (Floating-point Number)
Represents decimal values.
- usage:
```zephyr
myText # FLOAT:3.1415;
```
- **Valid Values**: Positive or negative numbers with decimals (e.g., 0.0, -1.25, 99.999).

## Modifying Values
To modify variables, use the **`? w:`** operation.


usage:
```zephyr
<VariableName> ? w:<Value>;
<VariableName> ? w:'<AnotherVariableName>';
```
Parameters:
- **`<VariableName>`** → Name of the variable you want to modify.
- **`VariableName`** → Must match the variable’s type.
- **`'AnotherVariableName'`** → By entering any variable name inside ' ', its current value is copied.

Example:
```zephyr
a # INT:10;
b # INT:0;

b ? w:'a';   ~ b now holds the value of a → 10
```

**Incrementing:**

- Increment integer or float by 1 (or 1.0)::
  ```zephyr
  counter ? w:++;
  ```
- Decrement integer or Float by 1 (or 1.0):
  ```zephyr
  counter ? w:--;
  ```
- Increment PT:
  ```zephyr
  printableText # PT:HelloWorld;
  printableText ? w:++;
  ```
  printableText after increment: HelloWorldHelloWorld
