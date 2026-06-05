# Simple Variables

Simple variables are the most basic building blocks in Zephyr. They store single pieces of data that can be modified, displayed, or used in calculations.

## Variable Types

Zephyr supports four types of simple variables:

| Type | Purpose | Example | Can Be Changed |
|------|---------|---------|-----------------|
| `PT` | **Printable Text** - strings of characters | `"Hello World"` | Yes |
| `INT` | **Integer** - whole numbers | `42`, `-10` | Yes |
| `FLOAT` | **Floating-point** - decimal numbers | `3.14`, `-2.5` | Yes |
| `BOOL` | **Boolean** - true or false values | `~1` (true) or `~0` (false) | Yes |

## Creating a Simple Variable

To create a simple variable, use the `#` base with the type and optional initial value:

```zephyr
<VariableName> # <Type>:<Value>|<Param1>|<Param2>|...;
```

### Examples

```zephyr
age # INT:25;              § Create an integer
name # PT:"Alice";         § Create text
pi # FLOAT:3.14;           § Create a decimal number
is_active # BOOL:~1;       § Create a boolean (true)
```

## Working with TEXT (PT)

### Creating Text Variables

```zephyr
greeting # PT:"Hello";
message # PT:"Welcome to Zephyr";
```

### Displaying Text

Use `? push:` to display text:

```zephyr
greeting # PT:"Hello";
greeting ? push:;          § Output: Hello
```

only Variables of the Type PT can be pushed

### Changing Text Value

Use `? w:` to write/change the value:

```zephyr
message # PT:"Hello";
message ? w:"Goodbye";     § Now message contains "Goodbye"
message ? push:;           § Output: Goodbye
```

### Adding Text (Incrementing)

Use `? w:++` to append text to the end:

```zephyr
message # PT:"Hello";
message ? w:++|"!";        § Appends "!" to the end
message ? push:;           § Output: Hello!
```

### Clearing Text (Decrementing)

Use `? w:--` to delete all the text:

```zephyr
message # PT:"Hello";
message ? w:--;            § Clears the message
message ? push:;           § Output: (empty)
```

### Inserting Text at a Position

Insert text at a specific position (position 1 is the first character):

```zephyr
message # PT:"Hello";
message ? insertAt:"Mr. "|1;    § Insert "Mr. " at the beginning
message ? push:;                 § Output: Mr. Hello
```

### Getting User Input

Use `? INPUT:` to let the user type text:

```zephyr
message # PT:"";
message ? INPUT:"What's your name? ";
message ? push:;           § Displays what the user typed
```

## Working with INTEGERS (INT)

### Creating Integer Variables

```zephyr
count # INT:10;            § Create an integer
score # INT:0;             § Create with initial value 0
negative # INT:-5;         § Create negative number
```

### Changing Integer Value

```zephyr
count # INT:10;
count ? w:20;              § Change value to 20
```

### Incrementing (Adding)

Increment by 1 (default):

```zephyr
count # INT:5;
count ? w:++;              § Add 1 to count
```

Increment by a specific amount:

```zephyr
count # INT:5;
count ? w:++|3;            § Add 3 to count
```

### Decrementing (Subtracting)

Decrement by 1 (default):

```zephyr
count # INT:10;
count ? w:--;               § Subtract 1 from count
```

Decrement by a specific amount:

```zephyr
count # INT:10;
count ? w:--|3;            § Subtract 3 from count
```

### Getting User Input

```zephyr
age # INT:0;
age ? INPUT:"Enter your age: ";
```

## Working with FLOAT (Decimal Numbers)

### Creating Float Variables

```zephyr
pi # FLOAT:3.14;
temperature # FLOAT:-5.5;
```

### Displaying Floats

```zephyr
pi # FLOAT:3.14159;
```

### Changing Float Value

```zephyr
temperature # FLOAT:20.0;
temperature ? w:25.5;      § Change temperature
```

### Incrementing Floats

```zephyr
temperature # FLOAT:20.0;
temperature ? w:++|0.5;    § Add 0.5 to temperature
```

### Decrementing Floats

```zephyr
temperature # FLOAT:20.0;
temperature ? w:--|0.5;    § Subtract 0.5 from temperature
```

### Getting User Input

```zephyr
weight # FLOAT:0.0;
weight ? INPUT:"Enter your weight in kg: ";
```

## Working with BOOLEAN (True/False)

### Understanding Booleans

Booleans represent true/false or yes/no:
- `~1` means **true** (yes, on, active)
- `~0` means **false** (no, off, inactive)

### Creating Boolean Variables

```zephyr
is_active # BOOL:~1;       § Create true
is_finished # BOOL:~0;     § Create false
```

### Displaying Boolean Values

```zephyr
is_active # BOOL:~1;
```

### Toggling a Boolean (Flipping True/False)

Use `? w:++` or `? w:--` to toggle between true and false:

```zephyr
is_active # BOOL:~1;
is_active ? w:++;          § Toggle: ~1 becomes ~0

is_active ? w:++;          § Toggle: ~0 becomes ~1
```

### Converting Boolean to Integer

You can convert a boolean to INT:

```zephyr
is_active # BOOL:~1;
is_active ? CT:INT;        § Convert to integer
```

## Changing Variable Types

You can convert a simple variable to a different type using `? CT:` (Change Type):

```zephyr
value # INT:5;
value ? CT:PT;             § Convert from INT to PT
```

### Conversion Rules

When converting, here's what happens:

| From | To | Result |
|------|-----|--------|
| `INT` or `FLOAT` | `PT` | Converted to text (e.g., 5 becomes "5") |
| `PT` | `INT` or `FLOAT` | Only works if text is a valid number |
| `BOOL:~1` | `INT` or `FLOAT` | Becomes 1 or 1.0 |
| `BOOL:~0` | `INT` or `FLOAT` | Becomes 0 or 0.0 |
| Any type | `BOOL` | Only works if the value is 1, 0, ~1, or ~0 |

### Example Conversions

```zephyr
§ INT to PT
num # INT:42;
num ? CT:PT;
num ? push:;               § Output: 42

§ PT to INT
text # PT:"100";
text ? CT:INT;

§ BOOL to INT
flag # BOOL:~1;
flag ? CT:INT;
```

## Making a Variable Constant (NOT YET IMPLEMENTED!)

You can make a simple variable constant (unchangeable) by adding the `~1` parameter:

```zephyr
pi # PT:"3.14159"|~1;      § This variable cannot be changed
```

If you try to change a constant variable, you'll get an error:

```zephyr
pi # PT:"3.14159"|~1;
pi ? w:"3.14";             § ERROR! Write Protection - can't change constant
```

## Practical Examples

### Example 1: Simple Calculator

```zephyr
§ Create two numbers
num1 # INT:10;
num2 # INT:5;


§ Do basic math (we'll learn about Math Objects later)
§ For now, just manipulate the values
num1 ? w:++|5;             § Add 5 to num1

num1 ? CT:PT;              § Change type to PT
num1 ? push:;              § Print num to console
```

### Example 2: User Input

```zephyr
name # PT:"";
name ? INPUT:"What is your name? ";

greeting # PT:"Hello, ";
greeting ? w:++|'name';    § Append the name to greeting
greeting ? push:;          § Output: Hello, [whatever they typed]
```

### Example 3: Toggle Status

```zephyr
is_ready # BOOL:~0;        § Start as not ready

is_ready ? w:++;           § Toggle to ready

is_ready ? w:++;           § Toggle back to not ready
```

## Summary

| Operation | Example | Result |
|-----------|---------|--------|
| Create variable | `count # INT:5;` | Creates variable with value 5 |
| Change value | `count ? w:10;` | Sets value to 10 |
| Display value | `message ? push:;` | Prints PT to console |
| Increment by 1 | `count ? w:++;` | Adds 1 |
| Increment by N | `count ? w:++|3;` | Adds 3 |
| Decrement by 1 | `count ? w:--;` | Subtracts 1 |
| Decrement by N | `count ? w:--|3;` | Subtracts 3 |
| Get user input | `count ? INPUT:"Enter: ";` | Waits for user to type |
| Insert text (PT) | `text ? insertAt:"X"|1;` | Inserts "X" at position 1 |
| Change type | `count ? CT:PT;` | Converts to different type |
