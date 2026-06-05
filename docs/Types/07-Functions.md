# Functions

Functions wrap a Math Object to create reusable calculations. Unlike Math Objects that calculate whenever you access them, Functions only calculate when you explicitly call them.

## Understanding Functions

Think of a Function as a recipe:
- **Math Object**: The recipe ingredients (the formula)
- **Function**: The packaged recipe (you call it to get results)

Functions are useful when you want to:
- Reuse the same calculation multiple times
- Keep calculations independent and organized
- Lock in values (optionally)

## Creating a Function

```zephyr
<VariableName> # FUNC:<ResultType>|<*disableVariableChange>|<*MathObjectName>;
```

- **ResultType**: The type of result (INT, PT, FLOAT)
- **disableVariableChange**: Optional - if set, function ignores variable changes after creation
- **MathObjectName**: The Math Object that contains the calculation

## Basic Function Example

```zephyr
§ Create variables for the calculation
a # INT:10;
b # INT:5;

§ Create a Math Object with the formula
add # MO:('a' + 'b');

§ Create a Function using that Math Object
calculator # FUNC:INT||add;
```

## Calling a Function

Use `? call:` to execute a function and get its result:

```zephyr
calculator ? call:;  § Executes the function
```

But wait, this doesn't save the result anywhere. You need to capture it:

```zephyr
result # INT:0;
result ? w:'calculator';  § Get the function result
result ? push:;           § Display it
```

## Complete Function Example

```zephyr
§ Step 1: Create variables
x # INT:10;
y # INT:5;

§ Step 2: Create Math Object
sum_formula # MO:('x' + 'y');

§ Step 3: Create Function
my_sum # FUNC:INT||sum_formula;

§ Step 4: Use the function
result # INT:0;
result ? w:'my_sum';
result ? push:;           § Output: 15
```

## Practical Function Examples

### Example 1: Area Calculator

```zephyr
§ Variables
length # INT:10;
width # INT:5;

§ Formula
area_formula # MO:('length' * 'width');

§ Function
calculate_area # FUNC:INT||area_formula;

§ Use it
area # INT:0;
area ? w:'calculate_area';
area ? push:;             § Output: 50
```

### Example 2: Temperature Conversion Function

```zephyr
celsius # INT:0;

§ Create the conversion formula
fahrenheit_formula # MO:('celsius' * 9 / 5 + 32);

§ Create function
celsius_to_fahrenheit # FUNC:INT||fahrenheit_formula;

§ Convert 25°C
celsius ? w:25;
result # INT:0;
result ? w:'celsius_to_fahrenheit';
result ? push:;           § Output: 77

§ Convert 0°C
celsius ? w:0;
result ? w:'celsius_to_fahrenheit';
result ? push:;           § Output: 32
```

### Example 3: Discount Calculator Function

```zephyr
original_price # FLOAT:100.0;
discount_percent # INT:20;

discount_formula # MO:('original_price' * 'discount_percent' / 100);
calc_discount # FUNC:FLOAT||discount_formula;

discount_amount # FLOAT:0;
discount_amount ? w:'calc_discount';
discount_amount ? push:;  § Output: 20.0

final_price # FLOAT:0;
final_price ? w:('original_price' - 'discount_amount');
final_price ? push:;      § Output: 80.0
```

## Changing Which Math Object a Function Uses

Use `? w:` to change the Math Object:

```zephyr
x # INT:10;
y # INT:5;

add_formula # MO:('x' + 'y');
multiply_formula # MO:('x' * 'y');

calculator # FUNC:INT||add_formula;

result # INT:0;
result ? w:'calculator';
result ? push:;           § Output: 15

§ Switch to multiply
calculator ? w:multiply_formula;

result ? w:'calculator';
result ? push:;           § Output: 50
```

## Functions with Loops

Functions are great inside loops:

```zephyr
base # INT:2;
power_formula # MO:('base' ^ 3);  § cube the base
get_power # FUNC:INT||power_formula;

exponent # INT:1;
keep_going # CO:('exponent' <= 5);
result # INT:0;

loop # LOOP:keep_going;
loop ? START:3;

result ? w:'get_power';
result ? push:;

base ? w:++|1;
exponent ? w:++;

loop ? END:;
```

Output: 8, 27, 64, 125, 216 (cubes of 2, 3, 4, 5, 6)

## Disabling Variable Change

Normally, when you call a function, it uses the current values of variables:

```zephyr
a # INT:10;
add_five # MO:('a' + 5);
calculator # FUNC:INT||add_five;

result # INT:0;
result ? w:'calculator';
result ? push:;  § Output: 15

§ Change a
a ? w:20;

result ? w:'calculator';
result ? push:;  § Output: 25 (uses new value of a)
```

To use only the original values, set the second parameter:

```zephyr
a # INT:10;
add_five # MO:('a' + 5);
locked_calculator # FUNC:INT|~1|add_five;  § Disable variable change

result # INT:0;
result ? w:'locked_calculator';
result ? push:;  § Output: 15

§ Change a
a ? w:20;

result ? w:'locked_calculator';
result ? push:;  § Output: 15 (still uses a=10)
```

## Why Use Functions?

### 1. Code Reusability

Instead of repeating calculations:

```zephyr
§ Without function (repetitive)
result1 ? w:('a' + 'b');
result2 ? w:('a' + 'b');
result3 ? w:('a' + 'b');
```

Use a function:

```zephyr
§ With function (clean)
result1 ? w:'add_values';
result2 ? w:'add_values';
result3 ? w:'add_values';
```

### 2. Organization

Functions help organize related calculations:

```zephyr
§ Geometry functions
area_formula # MO:('length' * 'width');
calculate_area # FUNC:INT||area_formula;

perimeter_formula # MO:('length' * 2 + 'width' * 2);
calculate_perimeter # FUNC:INT||perimeter_formula;
```

### 3. Consistency

When you change the formula once, all calculations update:

```zephyr
formula # MO:('a' + 'b');
my_func # FUNC:INT||formula;

§ Change formula once
formula ? w:('a' * 'b');

§ All uses of my_func now multiply instead of add
```

## Common Function Patterns

### Pattern 1: Simple Wrapper

```zephyr
value # INT:5;
double_formula # MO:('value' * 2);
double # FUNC:INT||double_formula;

result # INT:0;
result ? w:'double';
result ? push:;  § Output: 10
```

### Pattern 2: Multi-Step Calculation

```zephyr
radius # FLOAT:5.0;

§ Area = π * r²
pi # FLOAT:3.14159;
area_formula # MO:('pi' * 'radius' ^ 2);
calc_area # FUNC:FLOAT||area_formula;

area # FLOAT:0;
area ? w:'calc_area';
area ? push:;  § Output: 78.53975
```

### Pattern 3: Conditional Based

You can use the result of a function in conditions:

```zephyr
x # INT:10;
compute_x # MO:('x' ^ 2);  § Square of x
get_x # FUNC:INT||compute_x;

is_big # CO:('get_x' > 50);
is_big ? push:;  § Output: 1 (true, 100 > 50)
```

## Tips for Using Functions

1. **Create Math Object first** - Functions need a Math Object to work
2. **Use meaningful names** - Name functions after what they calculate
3. **Test the formula** - Verify the Math Object works before wrapping it in a function
4. **Document purpose** - Use comments to explain what the function does
5. **Keep formulas simple** - Complex calculations are hard to debug

## Summary

| Task | Example |
|------|---------|
| Create Math Object | `mo # MO:('a' + 'b');` |
| Create Function | `func # FUNC:INT\\|\\|mo;` |
| Call Function | `result ? w:'func';` |
| Change Math Object | `func ? w:new_mo;` |
| Lock variables | `func # FUNC:INT\|~1\|mo;` |

## Next Steps

- Combine functions with [LOOPs](04-LOOP.md)
- Use results in [IF Statements](03-IF-Statement.md)
- Try with [Lists](05-LIST.md) for batch calculations
