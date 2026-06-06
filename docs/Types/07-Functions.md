# Function

A Function wraps a Math Object to enable reusable calculations. Unlike Math Objects that calculate immediately, Functions only compute their result when explicitly called. 

---


## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`
- **`convertValue`** -> Result of latest calculation

## Methods

### Define
Creates a new Function with a Math Object.

```zephyr
function # FUNC:<ResultType>|<*-DisableVariableChange>|<*-MathObjectName>;
calculate # FUNC:RES|0|myMathObject;
```

- **`ResultType`** — The type of the function result currently only RES
- **`DisableVariableChange`** — (Optional) If set, the function uses variable values from declaration time only
- **`MathObjectName`** — (Optional) Name of the Math Object to wrap

### Write (w)
Changes which Math Object the Function uses.

```zephyr
func ? w:<*MathObjectName>;
calculate ? w:newMathObject;
```

### Call
Executes the Function and computes its result based on the current Math Object.

```zephyr
calculate ? call:;
```


## Notes

- Functions only calculate results when `call:` is executed.
- By default, Functions always use current variable values. Set the second parameter to disable this and use values from declaration time.
- Functions are useful for organizing complex calculations and reusing computation logic.
