# Lists

Lists allow you to store multiple values of the same type. 

## Understanding Lists

A list is like a container with numbered slots:

```
List: [ Value1 | Value2 | Value3 | Value4 | Value5 ]
Pos:  [    1   |    2   |   3    |   4    |    5   ]
```

You access values by their position (index). Positions start at 1.

## Creating a List

```zephyr
<VariableName> # LIST:<*ValueType>|<*- value>|<*- pointerPosition>;
```

- **ValueType**: `INT`, `PT`, or `FLOAT`
- **value**: Initial value(s) to store
- **pointerPosition**: Which position to start at (default is 1)

### Examples

```zephyr
numbers # LIST:INT;              § Empty list of integers
colors # LIST:PT|red|blue;   § List with two text values
scores # LIST:INT|10|20|30;      § List with three numbers
```

## Understanding the Pointer

Lists use a **pointer** to track which position you're currently looking at:

```zephyr
numbers # LIST:INT|5|10|15|20;
```

When you create this list, the pointer starts at position 1 (pointing to value 5).

## Moving the Pointer (Setting Position)

Use `? SET:` to move the pointer to a different position:

```zephyr
numbers # LIST:INT|5|10|15|20;

numbers ? SET:1;  § Point to position 1 (value 5)
numbers ? SET:3;  § Point to position 3 (value 15)
numbers ? SET:2;  § Point to position 2 (value 10)
```

Position 0 is not allowed. Positions can be negative or positive (except 0).

## Reading Values from a List

Once the pointer is at the right position, you can use the list value:

### Direct Reference

```zephyr
numbers # LIST:INT|10|20|30;
numbers ? SET:2;

result # INT:0;
result ? w:'numbers';  § Gets value at current pointer (20)
result ? CT:PT;
result ? push:;        § Output: 20
```

### Using Index in Brackets

You can specify a position without moving the pointer:

```zephyr
numbers # LIST:INT|10|20|30;

result # INT:0;
result ? w:'numbers<2>';  § Get value at position 2
result ? CT:PT;
result ? push:;           § Output: 20
```

### Using a Variable as Index

```zephyr
numbers # LIST:INT|10|20|30;
index # INT:3;

result # INT:0;
result ? w:'numbers<'index'>';  § Get value at position 3
result ? CT:PT;
result ? push:;                 § Output: 30
```

### Nested Indexing

```zephyr
indices # LIST:INT|1|2|3;
values # LIST:INT|100|200|300;

result # INT:0;
result ? w:'values<'indices<2>'>';  § Get indices[2]=2, then values[2]=200
result ? CT:PT;
result ? push:;                     § Output: 200
```

## Writing Values to a List

Use `? w:` to set a value at the current pointer position:

```zephyr
numbers # LIST:INT|10|20|30;

numbers ? SET:2;       § Point to position 2
numbers ? w:25;        § Change position 2 to 25
numbers ? SET:1;
numbers ? push:;       § Output: 10
numbers ? SET:2;
numbers ? push:;       § Output: 25
```



## Important Notes

### Position 0 is Invalid

```zephyr
numbers # LIST:INT|10|20|30;
numbers ? SET:0;  § ERROR! Position 0 doesn't exist
```

### Out of Bounds

If you try to access a position that doesn't exist:

```zephyr
numbers # LIST:INT|10|20|30;
numbers ? SET:10;  § Position 10 doesn't exist - ERROR!
```

### Types Must Match

All values in a list must be the same type:

```zephyr
valid # LIST:INT|1|2|3;        § All integers - OK
invalid # LIST:INT|1|two|3;    § ERROR! Mix of INT and PT
```




## Summary

| Task | Example |
|------|---------|
| Create list | `list # LIST:INT\|1\|2\|3;` |
| Point to position | `list ? SET:2;` |
| Get current position | `list ? push:;` |
| Read value | `var ? w:'list<2>';` |
| Read at pointer | `var ? w:'list';` |
| Write value | `list ? SET:2; list ? w:50;` |
| Use variable index | `var ? w:'list<'index'>';` |
