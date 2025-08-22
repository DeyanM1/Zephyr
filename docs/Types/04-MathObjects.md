# Math Objects

Math objects allow for complex calculations.

**Declare a Math Object:**

- usage:
```zephyr
<VariableName> # MO:;
<VariableName> # MO:(<equation>);
```

**Pass an Equation:**

- usage:
```zephyr
<VariableName> ? (<equation>):;
```
- **Equation Format**: `(a + b)` where `a` and `b` are variables.

**Example:**

- usage:
- Define and use a math object:
  ```zephyr
  result # MO:;
  result ? ('a' + 'b'):;
  ```
