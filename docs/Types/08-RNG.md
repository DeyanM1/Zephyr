# Random Number Generator (RNG)

Random Number Generator (RNG) objects generate random numbers within a specified range. They're useful for simulations, games, and any program that needs unpredictable values.

## Creating an RNG

```zephyr
<VariableName> # RNG:<*RangeMin>|<*RangeMax>|<*NumberType>;
```

- **RangeMin**: The minimum value (inclusive)
- **RangeMax**: The maximum value (inclusive)
- **NumberType**: The type of random number - `INT` or `FLOAT`

## Examples

### Random Integer (1 to 10)

```zephyr
dice # RNG:1|10|INT;

result # INT:0;
result ? w:'dice';
result ? push:;  § Output: Random number 1-10
```

### Random Decimal

```zephyr
random_decimal # RNG:0|1|FLOAT;

result # FLOAT:0;
result ? w:'random_decimal';
result ? push:;  § Output: Random decimal 0.0-1.0
```

### Negative Range

```zephyr
temp_variation # RNG:-10|10|INT;

result # INT:0;
result ? w:'temp_variation';
result ? push:;  § Output: Random -10 to 10
```

## Using Random Numbers

### Example 1: Dice Roller

```zephyr
six_sided # RNG:1|6|INT;

roll1 # INT:0;
roll2 # INT:0;

roll1 ? w:'six_sided';
roll2 ? w:'six_sided';

total # INT:0;
total ? w:('roll1' + 'roll2');

total ? push:;  § Output: Random 2-12
```

### Example 2: Random Selection

```zephyr
choice # RNG:1|3|INT;
selection # PT:"";

is_one # CO:('choice' == 1);
is_two # CO:('choice' == 2);

check_one # IF:is_one;
check_one ? START:1;
selection ? w:"Rock";
check_one ? ELSE:0;
check_one ? END:;

check_two # IF:is_two;
check_two ? START:1;
selection ? w:"Paper";
check_two ? ELSE:0;
check_two ? END:;

check_three # IF:is_one;
check_three ? w:('choice' == 3);
check_three ? START:1;
selection ? w:"Scissors";
check_three ? ELSE:0;
check_three ? END:;

selection ? push:;  § Output: Rock, Paper, or Scissors randomly
```

### Example 3: Probability

```zephyr
rand # RNG:1|100|INT;
lucky_number # INT:50;

is_lucky # CO:('rand' > 'lucky_number');
outcome # PT:"";

check # IF:is_lucky;
check ? START:1;
outcome ? w:"Lucky!";
check ? ELSE:1;
outcome ? w:"Not lucky!";
check ? END:;

outcome ? push:;  § 50% chance of "Lucky!"
```

## Changing RNG Range

Use `? w:` to modify the range or type:

```zephyr
generator # RNG:1|10|INT;

result # INT:0;
result ? w:'generator';
result ? push:;  § Output: 1-10

§ Change to 1-20
generator ? w:1|20|INT;

result ? w:'generator';
result ? push:;  § Output: 1-20
```

You can also change just the range without specifying a new type:

```zephyr
generator # RNG:1|10|INT;
generator ? w:5|15;  § New range: 5-15 (type stays INT)
```

## Practical RNG Examples

### Example 1: Game Die

```zephyr
die1 # RNG:1|6|INT;
die2 # RNG:1|6|INT;

roll1 # INT:0;
roll2 # INT:0;

roll1 ? w:'die1';
roll2 ? w:'die2';

roll1 ? push:;
roll2 ? push:;

combined # INT:0;
combined ? w:('roll1' + 'roll2');
combined ? push:;  § Sum of two random die rolls
```

### Example 2: Random Password Character

```zephyr
char_code # RNG:65|90|INT;  § ASCII codes for A-Z

char_value # INT:0;
char_value ? w:'char_code';
char_value ? push:;  § Output: 65-90 (letters A-Z)
```

### Example 3: Simulating Coin Flip

```zephyr
coin # RNG:0|1|INT;
result # PT:"";

is_heads # CO:('coin' == 0);

check # IF:is_heads;
check ? START:1;
result ? w:"Heads";
check ? ELSE:1;
result ? w:"Tails";
check ? END:;

result ? push:;  § Output: Heads or Tails
```

## RNG in Loops

Use RNG inside loops to generate multiple random numbers:

```zephyr
generator # RNG:1|100|INT;

counter # INT:1;
keep_going # CO:('counter' <= 5);

loop # LOOP:keep_going;
loop ? START:2;

generator ? push:;  § Print each random number
counter ? w:++;

loop ? END:;
```

Output: 5 random numbers 1-100

## Tips for Using RNG

1. **Define min and max carefully** - Remember both are inclusive
2. **Use INT for whole numbers** - Use FLOAT for decimals
3. **Test your ranges** - Call multiple times to see the variation
4. **Use in conditions** - Good for probability-based logic
5. **Combine with LOOPs** - Generate multiple random numbers easily

## Important Notes

- RNG generates a new random number each time you access it
- If you want to keep a random value, store it in a variable: `var ? w:'rng';`
- Both min and max values are **inclusive** (can appear in results)
- RNG works with negative ranges: `RNG:-50|50|INT`

## Summary

| Task | Example |
|------|---------|
| Create INT RNG | `rng # RNG:1\|10\|INT;` |
| Create FLOAT RNG | `rng # RNG:0\|1\|FLOAT;` |
| Get value | `var ? w:'rng';` |
| Change range | `rng ? w:5\|20\|INT;` |
| Use in condition | `CO:('rng' > 50)` |

## Next Steps

- Use RNG results in [IF Statements](03-IF-Statement.md) for random logic
- Combine with [LOOPs](04-LOOP.md) to generate sequences
- Store results in [Lists](05-LIST.md) for collections of random values
