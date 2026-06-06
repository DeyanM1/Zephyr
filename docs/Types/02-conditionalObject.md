# Conditional Object

A Conditional Object evaluates a condition and stores the result as a boolean value. Conditional Objects are used to drive decision-making in IF statements and loops.

---



## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`, `BOOL`
- **`convertValue`** -> Result of the condition

### Boolean Values

Conditional Objects store results as boolean values:
- **`~1`** = `true`
- **`~0`** = `false`

## Methods

### Define
Creates a new Conditional Object with an initial condition.

```zephyr
conditionalObject # CO:<*- ConditionScript>;
conditionalObject # CO:('a' > 'b');
```

### Write (w)
Replaces the condition script with a new one and re-evaluates it.

```zephyr
conditionalObject ? w:<*ConditionScript>;
conditionalObject ? w:('x' < 'y');
```

## Condition Script Format

Condition scripts compare two values or variables using operators. Enclose the entire condition in parentheses:

```zephyr
('variable1' > 'variable2')
('num1' == 'num2')
('count' < 10)
```

Supported operators:
- `>` (greater than)
- `<` (less than)
- `==` (equal to)
- `!=` (not equal to)


## Notes

- Conditional Objects are typically used as arguments to IF statements and LOOP objects.
- The result is always stored as either `~1` (true) or `~0` (false).
- Variables used in conditions must be enclosed in single quotes.
