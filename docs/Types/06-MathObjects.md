# Math Objects

Math Objects (MO) evaluate mathematical equations and store the result. They're useful for calculations that you might want to reuse or update.

## Understanding Math Objects

A Math Object is like a stored formula. When you create it, it calculates the result. When variables in the formula change, the result stays the same unless you explicitly update it.

```zephyr
a # INT:10;
b # INT:5;
total # MO:('a' + 'b');  § Calculates 10 + 5 = 15
```

## Creating a Math Object

```zephyr
<VariableName> # MO:<*EquationScript>;
```

The equation script is wrapped in parentheses.

## Equation Format

Write equations using variables in single quotes and operators:

### Using Shorthand (Recommended)

```zephyr
result # MO:('a' + 'b' * 2);
```

### Using Word Form

```zephyr
result # MO:('variable A' plus 'variable B' times 2);
```

## Supported Operators

Math Objects support basic arithmetic operators:

| Symbol | Word | Example | Result |
|--------|------|---------|--------|
| `+` | `plus` | `('a' + 'b')` | Addition |
| `-` | `minus` | `('a' - 'b')` | Subtraction |
| `*` | `times` | `('a' * 'b')` | Multiplication |
| `/` | `divided by` | `('a' / 'b')` | Division |
| `%` | `modulo` | `('a' % 'b')` | Remainder |
| `^` | `power` | `('a' ^ 'b')` | Exponentiation |

## Creating Math Objects

### Simple Addition

```zephyr
x # INT:10;
y # INT:5;
sum # MO:('x' + 'y');

result # INT:0;
result ? w:'sum';
result ? push:;  § Output: 15
```

### Multiple Operations

```zephyr
a # INT:10;
b # INT:5;
c # INT:2;

calculation # MO:('a' + 'b' * 'c');
§ Note: Follows order of operations (multiplication first)

result # INT:0;
result ? w:'calculation';
result ? push:;  § Output: 20 (not 30, because 5*2=10, then 10+10=20)
```

### Using Direct Values

```zephyr
multiplier # INT:5;
factor # MO:('multiplier' * 10);

result # INT:0;
result ? w:'factor';
result ? push:;  § Output: 50
```

## Practical Math Object Examples

### Example 1: Temperature Conversion

```zephyr
celsius # INT:25;
fahrenheit # MO:('celsius' * 9 / 5 + 32);

result # INT:0;
result ? w:'fahrenheit';
result ? push:;  § Output: 77 (25°C = 77°F)
```

### Example 2: Discount Calculator

```zephyr
price # FLOAT:100.0;
discount_percent # INT:10;
discount_amount # MO:('price' * 'discount_percent' / 100);

final_price # FLOAT:0;
final_price ? w:('price' - 'discount_amount');
final_price ? push:;  § Output: 90.0
```

### Example 3: Pythagorean Theorem

```zephyr
side_a # INT:3;
side_b # INT:4;
hypotenuse # MO:('side_a' ^ 2 + 'side_b' ^ 2);  § a² + b²

result # INT:0;
result ? w:'hypotenuse';
result ? push:;  § Output: 25
```

## Updating a Math Object

Use `? w:` to change the equation:

```zephyr
a # INT:10;
equation # MO:('a' + 5);

result # INT:0;
result ? w:'equation';
result ? push:;  § Output: 15

§ Change the equation
equation ? w:('a' * 2);

result ? w:'equation';
result ? push:;  § Output: 20
```

## Math Objects with Lists

You can use list values in Math Objects:

```zephyr
numbers # LIST:INT|10|20|30;

index1 # INT:1;
index2 # INT:3;

sum_of_ends # MO:('numbers<'index1'>' + 'numbers<'index2'>');

result # INT:0;
result ? w:'sum_of_ends';
result ? push:;  § Output: 40 (10 + 30)
```

## Division and Remainders

### Division

```zephyr
dividend # INT:20;
divisor # INT:3;
quotient # MO:('dividend' / 'divisor');

result # INT:0;
result ? w:'quotient';
result ? push:;  § Output: 6 (integer division)
```

### Modulo (Remainder)

```zephyr
dividend # INT:20;
divisor # INT:3;
remainder # MO:('dividend' % 'divisor');

result # INT:0;
result ? w:'remainder';
result ? push:;  § Output: 2 (20 / 3 leaves remainder 2)
```

## Using Math Objects in Conditionals

You can use Math Objects in conditions:

```zephyr
a # INT:10;
b # INT:5;
sum # MO:('a' + 'b');

is_big # CO:('sum' > 10);
is_big ? push:;  § Output: 1 (true, because 15 > 10)
```

## Order of Operations

Math Objects follow standard mathematical order of operations:
1. Parentheses (if nested)
2. Exponents (`^`)
3. Multiplication (`*`), Division (`/`), Modulo (`%`)
4. Addition (`+`), Subtraction (`-`)

```zephyr
§ Example: 2 + 3 * 4 = 14, not 20
calculation # MO:(2 + 3 * 4);
result # INT:0;
result ? w:'calculation';
result ? push:;  § Output: 14
```

## Tips for Math Objects

1. **Always use single quotes** for variable names: `'variable'` not `variable`
2. **Use direct values** without quotes: `10` not `"10"`
3. **Keep equations simple** — Complex ones are hard to debug
4. **Update when needed** — Change the equation if your logic changes
5. **Test first** — Print the result to verify it's correct

## Common Math Operations

### Average/Mean

```zephyr
a # INT:10;
b # INT:20;
c # INT:30;
average # MO:('a' + 'b' + 'c' / 3);

result # INT:0;
result ? w:'average';
result ? push:;  § Output: 20 (10+20+30)/3
```

### Percentage

```zephyr
part # INT:25;
total # INT:100;
percent # MO:('part' * 100 / 'total');

result # INT:0;
result ? w:'percent';
result ? push:;  § Output: 25
```

### Distance Formula

```zephyr
x1 # INT:0;
y1 # INT:0;
x2 # INT:3;
y2 # INT:4;

distance_squared # MO:('x2' - 'x1' ^ 2 + 'y2' - 'y1' ^ 2);

result # INT:0;
result ? w:'distance_squared';
result ? push:;  § Output: 25
```

## Summary

| Task | Example |
|------|---------|
| Create Math Object | `mo # MO:('a' + 'b');` |
| Get result | `result ? w:'mo';` |
| Update equation | `mo ? w:('a' * 'b');` |
| Use in condition | `CO:('mo' > 10)` |
| Division | `MO:('a' / 'b')` |
| Remainder | `MO:('a' % 'b')` |
| Power | `MO:('a' ^ 'b')` |

## Next Steps

- Use Math Objects in [Functions](07-Functions.md) for reusable calculations
- Combine with [IF Statements](03-IF-Statement.md) for conditional logic
- Try in [LOOPs](04-LOOP.md) for calculations in loops
