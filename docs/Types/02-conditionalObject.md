# Conditional Object

Supported types: `INT`, `PT`, `FLOAT`

Conditional Objects evaluate a condition and store its result as boolean values: 

- **`b1` for `true`** 
- **`b0` for `false`** 

They are used to drive decision-making in IF statements or loops. 

* Define:

```

co # CO:<*- ConditionScript>;

```

* Replace the Condition:

```

co ? w:<*ConditionScript>;

```

**ConditionScripts are writen in this format:**

```

('a' > 'b')
('variable A' is greater than 'variable B')

```