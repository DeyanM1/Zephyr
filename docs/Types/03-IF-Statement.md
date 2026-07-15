# IF Statement

An IF statement executes a block of code only if a Conditional Object evaluates to true. It optionally supports an ELSE block to execute code when the condition is false.


---

## Syntax Overview

```zephyr
if # IF:<*ConditionalObjectName>;
if ? START:;
  § Code to execute if true
if ? ELSE:;
  § Code to execute if false
if ? END:;
```

## Properties

- **`convertibleInto`** -> `None`
- **`convertValue`** -> `None`

## Methods

### Define
Creates an IF statement with a Conditional Object reference.

```zephyr
if # IF:<*conditionalObjectName>;
if # IF:conditionName;
```

### START

Marks the beginning of the IF block.

```zephyr
if ? START:;
```

### ELSE
Marks the beginning of the ELSE block (optional). If the condition is false, these commands execute instead.

```zephyr
if ? ELSE:;
```

### END
Marks the end of the IF statement block.

```zephyr
if ? END:;
```

### Write (w)
Changes the Conditional Object that the IF statement checks.

```zephyr
if ? w:<*ConditionalObjectName>;
if ? w:newConditionName;
```
