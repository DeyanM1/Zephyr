# Function

Supported types: `INT`, `PT`, `FLOAT`  
Value is calculated only when called.

Functions wrap a Math Object to allow reusable calculations. They only compute a result when explicitly called, enabling modular programming.

* Define:

```

func # FUNC:<ResultType>|<*disableVariableChange>|<*MathObjectName>;

```

* Change Math Object:

```

func ? w:<*MathObjectName>;

```

* Call function:

```

func ? call:;

```