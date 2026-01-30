# Simple Variable

Supported types: `INT`, `PT`, `FLOAT`

Simple Variables store single pieces of data that can be changed, incremented, decremented, printed, or replaced with user input. They are the basic building blocks for storing values in Zephyr.

* Define:

```

var # <Vartype>:<*Value>;

```

* Update value:

```

var ? w:<*NewValue>;

```

* Increment (INT/FLOAT):

```

var ? w:++|<*incrementBy>;   ~ Defaults to 1 if not set

```

* Decrement (INT/FLOAT):

```

var ? w:-|<*decrementBy>;    ~ Defaults to 1 if not set

```

* Print PT value:

```

var ? push:;

```

* Take input:

```

var ? INPUT:<*Message>;      ~ Overrides previous value

```