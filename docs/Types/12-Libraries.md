# Libraries

Libraries in Zephyr allow for the creation of custom functions that extend the language’s capabilities.

**Declare a Library:**

```zephyr
<VariableName> # LIB:<library file name>;
```

**Use a Function from a Library:**

```zephyr
<VariableName> ? <Function>:<Params>;
```

### Creating a Library

**File Structure:**

- Libraries are stored in the `lib/` directory.

```plaintext
lib/
├── code.zpkg
└── exampleLibrary.py
main.py
functions.py
code.zsrc
code.zph
```

**Library Code Structure:**

- A search function is necessary to check if statements can be modified.

```python
def search(name, func, base, paramsList, codeLine):
    match func:
        case "?":
            match base:
                case "add10":
                    vars = add10(vars, vars[paramsList[0]])
    return vars

def add10(vars, var):
    a = int(var.value)
    b = a + 10
    var.value = str(b)
    vars.update({var.name: var})
    return vars
```

**Example:**

- Define a function in a custom library and use it in Zephyr:
  ```zephyr
  myLib # LIB:exampleLibrary;
  myVar ? add10:myVar;
  ```
