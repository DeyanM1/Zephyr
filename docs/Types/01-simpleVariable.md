# Simple Variable

Supported types: `INT`, `PT`, `FLOAT`, `BOOL`

Simple Variables store single pieces of data that can be changed, incremented, decremented, printed, or replaced with user input. They are the basic building blocks for storing values in Zephyr.

There are 3 types of simple Variables: 

- **`PT`**: Printable Text (strings of characters) 
- **`INT`**: Integer (whole numbers) 
- **`FLOAT`**: Floating-point number (decimal values) 
- **`BOOL`**: Boolean value: ~1/~0 | True/False

---

* Define:

```

var # <Vartype>:<*- Value>;

```

* Changing Type:
You can change a type of any variable using CT. Be awere of the supported types of the Variable Type. The return value is the type that is being passed to the new variable on change. if not presents its the value of the old variable

```

var ? CT:<Vartype>;     § <VarType> is the new type of the variable

```

Changing the type of a bool to INT, FLOAT converts it to 1/0 or 1.0/0.0
changing a variable to bool only works if the other variabls return value is either 1/0 or 1.0/0.0  or ~1/~0

* Update value:

```

var ? w:<*NewValue>;

```

* Increment value of INT/FLOAT:

```

var ? w:++|<*- incrementBy>;   § Defaults to 1 if not set

```

* Decrement value of INT/FLOAT:

```

var ? w:-|<*- decrementBy>;    § Defaults to 1 if not set

```

* Increment / decrement value of PT:

```

var ? w:++|<*- incrementBy>;   § Defaults to 1 if not set -> The new incrementBy value is appended to var
var ? w:--;                    § decrementing a PT deletes its content. parameters are not supported.

```
* Increment / decrement value of BOOL:

```

var ? w:++|<*- incrementBy>;   §  incrementing or decrementing a BOOL Swaps the boolean value | ~1->~0; ~0->~1

```

* PTs can be pushed to the console:

```

var ? push:;

```

* Take input from the user:

```

var ? INPUT:<*- Message>;      § Overrides previous value

```

* Insert Value at position (PT)

```

var ? insertAt:<*valueToInsert>|<*position>; § position 1 is the first position

```
