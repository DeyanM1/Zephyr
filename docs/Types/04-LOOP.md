# LOOP Statements

LOOP statements execute a block of code repeatedly while a condition is true.


## Creating a LOOP Statement

```zephyr
<VariableName> # LOOP:<*ConditionalObjectName>;
```

The Conditional Object must already exist before creating the LOOP.

## Structure of a LOOP

A LOOP has three parts:

### Part 1: Create the LOOP

```zephyr
myloop # LOOP:my_condition;
```

### Part 2: Define the LOOP block

```zephyr
myloop ? START:<*NumberOfCommands>;
  § Your commands go here
```

### Part 3: End the LOOP

```zephyr
myloop ? END:;
```

## How LOOPs Work

1. Check the condition
2. If true, execute all commands in the START block
3. Go back to step 1 (check condition again)
4. If false, skip to after END



## Summary

| Task | Example |
|------|---------|
| Create LOOP | `loop # LOOP:my_condition;` |
| Start block | `loop ? START:2;` (2 commands follow) |
| End block | `loop ? END:;` |
| Change condition | `loop ? w:new_condition;` |
| Display condition | `my_condition ? push:;` |

