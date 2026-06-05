# Conditional Objects

Conditional Objects allow you to test conditions and get true/false results. They're essential for making decisions in your code.

## What is a Conditional Object?

A Conditional Object (CO) evaluates a condition and stores the result as a boolean:
- **`~1`** if the condition is **true** 
- **`~0`** if the condition is **false**

You use Conditional Objects with IF statements and LOOP statements to control what code runs.

## Creating a Conditional Object

To create a Conditional Object, use the `#` base with type `CO`:

```zephyr
<VariableName> # CO:<*ConditionScript>;
```

The condition script is wrapped in parentheses and follows specific syntax.

## Condition Scripts: The Syntax

A condition script evaluates a comparison.


```zephyr
conditionalObject # CO:('a' > 'b');
```

Where `'a'` and `'b'` are variable names or values.


## Comparison Operators

Conditional Objects support these comparison operators:

| Operator | Word Form | Example | Meaning |
|----------|-----------|---------|---------|
| `>` | `greater than` | `('a' > 'b')` | Is a greater than b? |
| `<` | `less than` | `('a' < 'b')` | Is a less than b? |
| `==` | `equal` | `('a' == 'b')` | Is a equal to b? |
| `!=` | `not equal` | `('a' != 'b')` | Is a not equal to b? |
| `>=` | `greater equal` | `('a' >= 'b')` | Is a greater than or equal to b? |
| `<=` | `less equal` | `('a' <= 'b')` | Is a less than or equal to b? |

## Working with Variables

When you use a variable in a condition, enclose its name in single quotes:

```zephyr
age # INT:25;
is_adult # CO:('age' >= 18);
is_adult ? push:;          § Output: 1 (true)
```

You can also directly use values without creating variables first:

```zephyr
check # CO:(5 > 3);        § Output: 1 (true)
check ? push:;
```

## Common Examples

### Comparing Numbers

```zephyr
score # INT:85;
is_high # CO:('score' > 80); § Output: 1 (true, because 85 > 80)
```

### Comparing Text

```zephyr
name # PT:"Alice";
is_alice # CO:('name' == "Alice"); § Output: 1 (true, because names match)
```

### Comparing with Operators

```zephyr
temperature # FLOAT:20.5;

is_warm # CO:('temperature' > 20.0); § Output: 1 (true)

is_freezing # CO:('temperature' < 0.0); § Output: 0 (false)
```

## Changing a Condition

After creating a Conditional Object, you can change its condition using `? w:`:

```zephyr
condition # CO:('a' > 'b'); § Let's say this outputs 0 (false)

condition ? w:('a' < 'b'); § Change the condition -> Now outputs 1 (true)
```

## Using Conditional Objects with Variables

### Example 1: Check Age

```zephyr
age # INT:16;

can_vote # CO:('age' >= 18); § Output: 0 (false, 16 is not >= 18)

age ? w:18;                  § Change age to 18
can_vote ? w:('age' >= 18);  § Update the condition -> Output: 1 (true, 18 is >= 18)
```

### Example 2: Check String Equality

```zephyr
password # PT:"secret123";
correct # CO:('password' == "secret123");
correct ? push:;           § Output: 1 (true)

wrong # CO:('password' == "wrong");
wrong ? push:;             § Output: 0 (false)
```

### Example 3: Numeric Ranges

```zephyr
score # INT:75;

is_passing # CO:('score' >= 60);
is_passing ? push:;        § Output: 1 (true, 75 >= 60)

is_excellent # CO:('score' >= 90);
is_excellent ? push:;      § Output: 0 (false, 75 < 90)

is_too_low # CO:('score' < 60);
is_too_low ? push:;        § Output: 0 (false)
```

## Converting Conditions to Booleans

A Conditional Object stores its result as `~1` (true) or `~0` (false), so you can convert it to a BOOL:

```zephyr
condition # CO:(5 > 3);
condition ? CT:BOOL;       § Convert to boolean  Output: 1
```

## Practical Scenarios

### Scenario 1: Validate User Age

```zephyr
age # INT:0;
age ? INPUT:"Enter your age: ";

is_adult # CO:('age' >= 18);

§ Later, use is_adult in an IF statement (covered in next section)
```

### Scenario 2: Check if Inventory Has Items

```zephyr
inventory_count # INT:5;

has_items # CO:('inventory_count' > 0);     § Output: 

is_empty # CO:('inventory_count' == 0); § Output: 0 (false, not empty)
```

### Scenario 3: Compare Floating Point Numbers

```zephyr
balance # FLOAT:100.50;
minimum # FLOAT:50.00;

sufficient_funds # CO:('balance' >= 'minimum');
sufficient_funds ? push:;  § Output: 1 (true)
```


## How to Debug Conditions

If a condition isn't working as expected, print its result:

```zephyr
age # INT:15;
is_adult # CO:('age' >= 18); § Check what it outputs (should be 0)

§ If result is wrong, check:
§ - Are variable names spelled correctly?
§ - Is the operator correct?
§ - Are you using the right comparison?
```


## Summary

| Task | Example | Output |
|------|---------|--------|
| Create condition | `check # CO:('a' > 'b');` | Creates condition |
| Display result | `check ? push:;` | Shows 1 or 0 |
| Change condition | `check ? w:('a' < 'b');` | Updates the condition |
| Compare numbers | `CO:(5 > 3)` | 1 (true) |
| Compare text | `CO:("hello" == "hello")` | 1 (true) |
| Not equal | `CO:('a' != 'b')` | 1 or 0 depending on values |
