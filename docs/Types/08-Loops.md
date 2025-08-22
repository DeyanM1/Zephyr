# Loops

Loops in Zephyr allow you to repeat actions.

**Declare a Loop:**

- usage:
```zephyr
<VariableName> # LOOP:<Conditional Object Name>;
```

- **Conditional Object**: Controls the loop’s execution based on a boolean condition.

**End a Loop:**

- usage:
```zephyr
<VariableName> ? END:;
```

**Example:**

- Create a loop that runs while a conditionObject is true:
  ```zephyr
  repeatLoop # LOOP:<conditionalObject>;
  repeatLoop ? END:;
  ```
