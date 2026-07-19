# Simple Variables

Simple variables are the most basic building blocks in Zephyr. They store single pieces of data that can be modified, displayed, or used in calculations.

## Variable Types

Zephyr supports four types of simple variables:

| Type | Purpose | Example |
|------|---------|---------|
| `PT` | **Printable Text** - strings of characters | `Hello World` |
| `INT` | **Integer** - whole numbers | `42`, `-10` |
| `FLOAT` | **Floating-point** - decimal numbers | `3.14`, `-2.5` |
| `BOOL` | **Boolean** - true or false values | `~1` (true) or `~0` (false) |


## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`, `BOOL`, `LIST`
- **`convertValue`** -> Value of variable

**Note**: Every simplevar can be converted between the 4 simplevar types
**Note**: Only PT can be turned into `LIST`, Chars of the PT are turned into values of LIST (Split by char)


## Creating a Simple Variable

To create a simple variable, use the `#` base with the type, optional initial value and optional constant flag:

```zephyr
<VariableName> # <Type>:<*- Value>|<*- const>;
```

### Examples

```zephyr
age # INT:25|~0;           § Create an integer
name # PT:"Alice";         § Create text
pi # FLOAT:3.14;           § Create a decimal number
is_active # BOOL:~1;       § Create a boolean (true)
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
| Any type | `PT` | Converts the values to text |
| `PT` | `INT` or `FLOAT` | Only works if text is a valid number |
| `BOOL:~1` | `INT` or `FLOAT` | Becomes 1 or 1.0 |
| `BOOL:~0` | `INT` or `FLOAT` | Becomes 0 or 0.0 |
| Any type | `BOOL` | Only works if the value is 1, 0, ~1, or ~0 |


## Constant

You can make a simple variable constant (unchangeable) by adding the `~1` parameter:

```zephyr
<name> # <Type>:<*- initialValue>|<*- const>

pi # PT:3.14159|~1;      § This variable cannot be changed
```

If you try to change a constant variable, you'll get an error:

```zephyr
pi # PT:3.14159|~1;
pi ? w:3.14;             § ERROR! Write Protection - can't change constant
```


Or using the `? C`:

```zephyr
<name> ? C:<~ const>;

age # INT:25|~1;
age ? w:26;               § Throws a write protection error
age ? C:~0;               § write protection is now turned off
age ? w:26;               § Value is now changed.
```

- **const** is a boolean value that sets if the var is const or not.


## Length of a variable

use LNGH to get the amount of characters or digits in a variable

this function is available on: INT, PT, FLOAT

usage:

```zephyr
<name> ? LGTH:<* targetVarName>;

a # PT:Length;
lengthOfA # INT:;

a ? LGTH:lengthOfA;

lengthOfA ? push:;    § outputs 6
```

- **targetVarName** is the name of the variable the length is pasted into


## Working with TEXT (PT)

### Creating Text Variables

```zephyr
<name> # PT:<*- initialValue>|<*- const>;

greeting # PT:Hello;
message # PT:Welcome to Zephyr;
```

### Displaying Text

Use `? push:` to display text:

```zephyr
<name> ? push:<*- newLine>;

greeting # PT:Hello;
greeting ? push:;          § Output: Hello
```

- **newLine** if set to False it doesnt print a newline after the print (~1 / ~0). Default is True
- only Variables of the Type PT can be pushed

### Changing Text Value

Use `? w:` to write/change the value:

```zephyr
<name> ? w:<newValue>;

message # PT:Hello;
message ? w:Goodbye;     § Now message contains "Goodbye"
message ? push:;         § Output: Goodbye
```

### Adding Text (Incrementing)

Use `? w:++` to append text to the end:

```zephyr
<name> ? w:++|<* ValuetoAppend>;

message # PT:Hello;
message ? w:++|<* text>;
message ? w:++|!;          § Appends ! to the end
message ? push:;           § Output: Hello!
```

### Clearing Text (Decrementing)

Use `? w:--` to delete all the text:

```zephyr
<name> ? w:--;

message # PT:Hello;
message ? w:--;            § Clears the message
message ? push:;           § Output: (empty)
```

### Inserting Text at a Position

Insert text at a specific position (position 1 is the first character):

```zephyr
<name> ? insertAt:<* value>|<* position>;

message # PT:Hello;
message ? insertAt:Mr. |1;    § Insert "Mr. " at the beginning
message ? push:;                 § Output: Mr. Hello
```

### Inserting Text at PlaceHolder

Inserting text at a placeholder in the original Text

```zephyr
<name> ? insertAt:<* placeholder>|<* text>;

message # PT:Hello $a!;
message ? insertAt:$a|World;  § Insert World at the $a
message ? push:;              § Output: Hello World!
```

### Getting User Input

Use `? INPUT:` to let the user type text:

```zephyr
<name> ? INPUT:<*- message>;

message # PT:;
message ? INPUT:What's your name? ;
message ? push:;           § Displays what the user typed
```

### Check type compatibility of value ( ? check)

Use `? check:;` to check if the current value is compatible with a variable type

```zephyr
value ? check:<* type>|<* targetVarName>;

value # PT:Hello;
isInt # BOOL:~0;
value ? check:INT|isInt;    § isInt is still ~0
```

- **`type`**: the to check for. allowed: `INT`, `FLOAT`, `BOOL`
- **`targetVarName`**: the name of the boolean var the result is pasted into.



## Working with INTEGERS (INT)

### Creating Integer Variables

```zephyr
<name> # INT:<*- initialValue>|<*- const>;

count # INT:10;            § Create an integer
score # INT:0;             § Create with initial value 0
negative # INT:-5;         § Create negative number
```

### Changing Integer Value

```zephyr
<name> ? w:<* newValue>;

count # INT:10;
count ? w:20;              § Change value to 20
```

### Incrementing (Adding)


```zephyr
<name> ? w:++|<*- incrementValue>;

count # INT:5;
count ? w:++;              § Add 1 to count
count ? w:++|4;            § Add 4 to count
```

- **incrementValue** defaults to 1.

### Decrementing (Subtracting)


```zephyr
<name> ? w:++|<*- decrementValue>;

count # INT:10;
count ? w:--;              § decrement count by 1
count ? w:--|4;            § decrement count by 4
```

- **decrementValue** defaults to 1.

### Getting User Input

```zephyr
<name> ? INPUT:<*- message>;

age # INT:0;
age ? INPUT:Enter your age: ;
```

- **message**: Message printet in the line of the input.
- **Note**: If the Input doesnt match the type it throws a ZError!



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
temperature ? w:++|<* amount>;
temperature ? w:++|0.5;    § Add 0.5 to temperature
```

### Decrementing Floats

```zephyr
temperature # FLOAT:20.0;
temperature ? w:--|<* amount>;
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

- `~1` means **true**
- `~0` means **false**

### Creating Boolean Variables

```zephyr
<name> # Type:<*- initialState>;

is_active # BOOL:~1;       § Create true
is_finished # BOOL:~0;     § Create false
```

### Toggling a Boolean

Use `? w:++` or `? w:--` to toggle between true and false:

```zephyr
<name> ? w:<++/-->;

is_active # BOOL:~1;
is_active ? w:++;          § Toggle: ~1 becomes ~0

is_active ? w:++;          § Toggle: ~0 becomes ~1
```

### Converting Boolean to Integer/Float

You can convert a boolean to INT/FLOAT:

```zephyr
<name> ? CT:<newType>;

is_active # BOOL:~1;
is_active ? CT:INT;        § Convert to integer
```

- **newType**: The newType has to either be `INT` or `FLOAT`
