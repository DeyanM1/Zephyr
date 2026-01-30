# LOOP

Supported types: `INT`, `PT`, `FLOAT`  
Value represents the number of iterations.

LOOP objects repeatedly execute a block of code while a Conditional Object evaluates to true. Their value updates to reflect the number of completed iterations.

* Define:

```

loop # LOOP:<*ConditionalObjectName>;

```

* Change condition:

```

loop ? w:<*ConditionalObjectName>;

```

* Start loop block:

```

loop ? START:<*commandsInLOOP>;

```

* End loop block:

```

loop ? END:;

```