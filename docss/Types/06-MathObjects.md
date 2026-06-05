# Math Object

Supported types: `INT`, `PT`, `FLOAT`  
Value is calculated whenever the script is set or changed.

Math Objects evaluate an equation and store the result. They simplify calculations and can be reused in functions or other objects.

* Define:

```

mo # MO:<*-EquationScript>;

```

* Update script:

```

mo ? w:<*EquationScript>;

```

**EquationScripts are writen in this format:**

```

('a' + 'b' + 1)
('variable A' plus 'variable B' plus 1)

```
