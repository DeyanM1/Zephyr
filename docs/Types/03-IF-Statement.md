# IF Statements

IF statements allow your program to make decisions. They execute code only if a condition is true, and optionally run different code if the condition is false.


## Creating an IF Statement

```zephyr
<VariableName> # IF:<*ConditionalObjectName>;
```

The Conditional Object must already exist before you create the IF statement.

## Structure of an IF Statement

A complete IF statement has three parts:

### Part 1: Create the IF

```zephyr
statement # IF:my_condition;
```

### Part 2: Define the IF block

```zephyr
statement ? START:<*NumberOfCommands>;
  § Your commands go here
```

The number tells Zephyr how many individual commands are in the IF block.

**Important**: Blank lines and comment-only lines don't count as commands!

### Part 3: End the IF

```zephyr
statement ? END:;
```

### Adding an ELSE block (Optional)

Between START and END, you can add an ELSE block:

```zephyr
statement ? ELSE:<*NumberOfCommands>;
  § Commands here run if condition is false
```

## Simple IF Statement (Without ELSE)

This runs code only when the condition is true:

```zephyr
score # INT:90;
is_high # CO:('score' >= 80);

check # IF:is_high;
check ? START:1;
  score ? CT:PT
  score ? push:;           § This only runs if score >= 80
check ? END:;
```

**Output**: `90` (because 90 >= 80 is true)

If the score was 50, nothing would print.

## IF with ELSE

ELSE runs code when the condition is false:


```zephyr
age # INT:15;
is_adult # CO:('age' >= 18);
message # PT:"";

check # IF:is_adult;
check ? START:1;
  message ? w:"You are an adult";
check ? ELSE:1;
  message ? w:"You are not yet an adult";
check ? END:;

message ? push:;
```


**Output**: `You are not yet an adult` (because 15 < 18)

## Changing the Condition

You can change what condition an IF statement uses before the start:

```zephyr
condition1 # CO:(5 > 3);
condition2 # CO:(5 < 3);

my_if # IF:condition1;

§ Now change to condition2
my_if ? w:condition2;

my_if ? START:1;
my_if ? END:;
```




## Summary

| Task | Example |
|------|---------|
| Create IF | `check # IF:my_condition;` |
| IF block | `check ? START:2;` (2 commands follow) |
| ELSE block | `check ? ELSE:1;` (1 command follows) |
| End IF | `check ? END:;` |
| Change condition | `check ? w:new_condition;` |
| Display condition | `my_condition ? push:;` |
