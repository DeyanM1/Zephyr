# Simple Variable

Supported types: `INT`, `PT`, `FLOAT`

Simple Variables store single pieces of data that can be changed, incremented, decremented, printed, or replaced with user input. They are the basic building blocks for storing values in Zephyr.

There are 3 types of simple Variables: 

- **`PT`**: Printable Text (strings of characters) 
- **`INT`**: Integer (whole numbers) 
- **`FLOAT`**: Floating-point number (decimal values) 

---

* Define:

```

var # <Vartype>:<*- Value>;

```

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