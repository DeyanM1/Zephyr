# LOOP

Supported types: `INT`, `PT`, `FLOAT`  
Value represents the number of iterations.

LOOP objects repeatedly execute a block of code while a Conditional Object evaluates to true. Their value updates to reflect the number of completed iterations.

**`commandsInLoop`** refers to the count of individual commands in the loop block.
Blank lines or lines with just a comment are not counted.


* Define:

```

loop # LOOP:<*ConditionalObjectName>;

loop ? START:<*commandsInLOOP>;
    ~ this gets repeated
loop ? END:;

```

* Change condition:

```

loop ? w:<*ConditionalObjectName>;

```
