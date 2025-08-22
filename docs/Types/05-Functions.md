# Functions

Functions in Zephyr allow you to encapsulate an equation and reuse it.


**Declare a Function:**

- usage:
```zephyr
<VariableName> # FUNC:<returnType>|(~1/~0);
```

- **Return Types**: `RES` (Result); `VC` (Variable changable);
- **~ 1/~0**: Indicates if the function's behavior changes based on external variable modifications.
- **~ 1** Disables variable change!
## Function RES
**Pass an Equation to a Function:**

- usage:
```zephyr
<VariableName> ? (<equation>);
```

**Call a Function:**

- usage:
```zephyr
<VariableName> ? call:;
```

**Example:**

- Create a function that adds two numbers:
  ```zephyr
  addNumbers # FUNC:RES;
  addNumbers ? ('a' + 'b');
  addNumbers ? call:;
  ```

## Function VC **(Coming Soon)**
- usage:
```zephyr
<VariableName> ? (<equation>);
```

Variables are notes as v1, v2, ...
**changeInternVariables**
- usage:
```zephyr
  <VariableName> ? VC:<v1>|<v2>|...;
```

**Example**
```zephyr
a # INT:1;
b # INT:2;

a2 # INT:2;
b2 # INT:3;

function # FUNC:VC;
function ? ('v1'+'v2')

function ? VC:a|b;
function ? call:;  -> Result == 3

function ? VC:a2|b2;
function ? call:;   -> Result == 5
```
