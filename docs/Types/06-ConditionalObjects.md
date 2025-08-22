# Conditional Objects

Conditional objects return boolean values (`~1` for true, `~0` for false) based on conditions.

**Declare a Conditional Object:**

```zephyr
<VariableName> # CO:;
<VariableName> # CO:(<condition>);
```

- **Condition Format**: `(a > b)`

**Example:**

- Create a condition:
  ```zephyr
  isGreater # CO:('a' > 'b');
  ```
