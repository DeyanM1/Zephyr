# Syntax Overview


## The Basic Structure of Every Command

In Zephyr, every statement follows the same pattern:

```zephyr
<VariableName> <base> <function>:<Argument1>|<Argument2>|...;
<---------------------------command------------------------->
```

Here's what each part means:

- **`VariableName`**: The name of the variable, user-defined.
- **`base`**: The base of the variable, used to define its operation:
  - **`?`**: For variable operations (e.g., modifying or retrieving values).
  - **`#`**: For declaring variables.
- **`function`**: The operation to execute on the variable (e.g., printing, defining a function).
- **`arguments`**: Additional information passed to the function Seperated by `|`.
- **`command`:** The entire statement.



## Example:

```zephyr
counter # INT:10;
```

| Part | Meaning |
|------|---------|
| `counter` | This is the name of our variable |
| `#` | We're creating/declaring this variable |
| `INT` | The type is Integer (whole numbers) |
| `:10` | The initial value is 10 |
| `;` | End of statement |

## File Extensions

When you save Zephyr programs, use these file types:

![](https://github.com/user-attachments/assets/58b3cce4-7ca9-4432-8cd0-45dfd3cda824#gh-dark-mode-only)
![](https://github.com/user-attachments/assets/6c7fc8b9-c8f1-450f-bda8-6863f83aa567#gh-light-mode-only)
![flowChart2](https://github.com/user-attachments/assets/332dac53-778b-4986-9fe6-67c22719c03e)
#### Compiler Functionality Diagram

## Running Scripts

### Running a Script File

If you have a file called `program.zph`:

```bash
python src/zcli.py program.zph
```

### Interactive Shell Mode

To try commands interactively without a file:

```bash
python src/zcli.py
```

Type your commands at the prompt. Each command runs immediately. Type `exit` to quit.

**Important**: If you press `Ctrl+C` instead of `exit`, temporary files won't be cleaned up, this is useful for keeping .zsrc files.

## Comments: Documenting Your Code

Comments help explain what your code does. In Zephyr, use `§` (section symbol) to mark comments:

```zephyr
counter # INT:10;  § This is a comment on the same line
§ This entire line is a comment and will be ignored
```


## Key Syntax Rules

### Parameters Are Absolute Order

When a function expects parameters, **you must provide them in the exact order specified**. 

### Optional Parameters

Some functions have optional parameters. These are shown with a `-` in documentation:

```
function:<*- OptionalParam>
```

If you don't provide optional parameters, Zephyr uses default values.

### Variables in Arguments

You can use variables as arguments by enclosing them in single quotes:

```zephyr
num1 # INT:5;
num2 # INT:10;
sum # INT:0;
sum ? w:('num1' + 'num2');  § Using variables num1 and num2
```

The `'num1'` and `'num2'` are replaced with their actual values.

### Wildcards in Documentation

In the documentation, you'll see symbols representing different things:

| Symbol | Meaning |
|--------|---------|
| `*` | A value (can be a value compatible with the variable type or variable name in quotes) |
| `-` | An optional value |
| `' '` | Enclose variable names in single quotes when using them as values |

### Convertible information

Every type has a set of other types it can be converted into.
In the documentation Allowed Conversions are declared using the convertibleInto property, followed by the list of target types:

ConvertValue is the value that is going to be passed onto the new Variable type

- **`convertibleInto`** -> `PT`, `INT`
- **`convertValue`** -> Value of the Var

**Note**: Even if the variable is compatible with the new type, the conversion can fail because the value of the type is not compatible with the new type.

## Declaring Variables

To create a new variable, use the `#` base:

```zephyr
<VariableName> # <Type>:<Value>|<Param1>|<Param2>|...;
```

**Example:**

```zephyr
age # INT:25;
name # PT:"Alice";
active # BOOL:~1;
```

## Changing a Variable's Type

You can convert a variable from one type to another using `? CT:` (Change Type):

```zephyr
count # INT:5;
count ? CT:PT;  § Convert from INT to PT (now it's text "5")
```

Not all type conversions are possible. Check the documentation for each type to see which conversions are allowed.

**Note**: You can also just redeclare a variable with a new type using `#`:

```zephyr
value # INT:10;
value # PT:"Hello";  § Redeclare as a different type
```

## Working with Variables

Once you create a variable, you use `?` to perform actions on it:

```zephyr
message # PT:"Hello";
message ? push:;              § Display the message
message ? w:"Goodbye";        § Change the value
```
