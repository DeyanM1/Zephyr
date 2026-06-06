# Loop

A Loop object repeatedly executes a block of code while a Conditional Object evaluates to true. The loop's value automatically updates to reflect the number of completed iterations.

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
Marks the beginning of the loop block. The parameter specifies the number of individual commands to execute in each iteration. Blank lines and comment-only lines are not counted.

```zephyr
loop ? START:<*CommandCount>;
loop ? START:3;
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

#

## Notes

- Command count refers to individual Zephyr statements, not lines of code.
- Blank lines and lines containing only comments are not counted toward the command total.
- Each command must end with a semicolon.
- The loop continues as long as the Conditional Object evaluates to true (~1).
- The loop's value tracks the number of iterations completed.
- The variable value field shows the iteration count after execution.
