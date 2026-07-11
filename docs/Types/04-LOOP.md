# Loop

A Loop object repeatedly executes a block of code while a Conditional Object evaluates to true. 

---

## Syntax Overview

```zephyr
loop # LOOP:<*ConditionalObjectName>;
loop ? START:<*CommandCount>;
  § Code to execute repeatedly
loop ? END:;
```

## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`
- **`convertValue`** -> Count of times Looped

## Methods

### Define

Creates a LOOP object with a Conditional Object that controls execution.

```zephyr
loop # LOOP:<*ConditionalObjectName>;
loop # LOOP:conditionName;
```

### START

Marks the beginning of the loop block.

```zephyr
loop ? START:;
```

### END

Marks the end of the loop block.

```zephyr
loop ? END:;
```

### Write (w)
Changes the Conditional Object that controls whether the loop continues.

```zephyr
loop ? w:<*ConditionalObjectName>;
loop ? w:newConditionName;
```

## Notes

- The loop continues as long as the Conditional Object evaluates to true (~1).
- The loop's value tracks the number of iterations completed.
- The variable value field shows the iteration count after execution.
