# Math Object

A Math Object evaluates a mathematical equation and stores the result. Math Objects simplify calculations and can be reused in functions or other operations. The value is calculated whenever the equation script is set or changed.

---


## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`
- **`convertValue`** -> Result of calculation

## Methods

### Define
Creates a new Math Object with an optional initial equation.

```zephyr
mathObject # MO:<*-EquationScript>;
calculation # MO:('x' + 'y' * 2);
```

- **`EquationScript`** — (Optional) Mathematical expression to evaluate


### Write (w)
Updates the equation script and recalculates the result.

```zephyr
mo ? w:<*EquationScript>;
calculation ? w:('a' - 'b' / 2);
```

## Equation Script Format

Equation scripts perform arithmetic on numbers and variables. Enclose the entire equation in parentheses:

```zephyr
('value1' + 'value2')
('num1' - 'num2')
('x' * 'y')
('total' / 'count')
```

Supported operators:
- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)



## Notes

- Math Objects calculate results only when the equation is defined or updated.
- Variables in equations must be enclosed in single quotes.
- The result type depends on the operand types and the operation performed.
- Math Objects are typically used as input to Function objects.
