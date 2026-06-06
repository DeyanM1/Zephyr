# IF Statement

An IF statement executes a block of code only if a Conditional Object evaluates to true. It optionally supports an ELSE block to execute code when the condition is false.

---

## Syntax Overview

```zephyr
if # IF:<*ConditionalObjectName>;
if ? START:<*CommandCount>;
  § Code to execute if true
if ? ELSE:<*CommandCount>;
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
Marks the beginning of the IF block. The parameter is the number of individual commands to execute. Blank lines and comment-only lines are not counted.

```zephyr
if ? START:<*commandsInIF>;
if ? START:2;
```

### ELSE
Marks the beginning of the ELSE block (optional). Specifies the number of commands in the ELSE block. If the condition is false, these commands execute instead.

```zephyr
if ? ELSE:<*commandsInELSE>;
if ? ELSE:1;
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



## Notes

- Command count refers to individual Zephyr statements, not lines of code.
- Blank lines and lines containing only comments are not counted toward the command total.
- Each command must end with a semicolon.
- The IF statement must have exactly matching command counts, or execution may fail.
