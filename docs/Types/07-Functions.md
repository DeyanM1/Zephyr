# Function

Supported types: `INT`, `PT`, `FLOAT`  
Value is calculated only when called.

Functions wrap a Math Object to allow reusable calculations. They only compute a result when explicitly called, enabling modular programming.

* Define:

*`ResultType`* is currently developed. It can be set to any value

*`disableVarialbeChange`* if set makes the function ignore if a variable changes and uses only the values saved at decleration
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