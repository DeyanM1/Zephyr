# Conditional Object

Supported types: `INT`, `PT`, `FLOAT`

Conditional Objects evaluate a condition and store its result. They are used to drive decision-making in IF statements or loops.

* Define:

```

co # CO:<*ConditionScript>;

```

* Update:

```

co ? w:<*ConditionScript>;

```

**Condition format example:**

```

('a' > 'b')

```