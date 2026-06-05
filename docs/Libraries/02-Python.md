# Python Library

The Python library allows you to execute Python code directly from your Zephyr program. This is useful for advanced operations, data processing, or integrating existing Python libraries.

## Importing Python Library

First, import the Python library:

```zephyr
__ ? LIB:./lib/python.py;
```

## Creating a Python Object

After importing, create a Python object:

```zephyr
python # python:;
```

No additional arguments are needed. The variable is immutable (cannot be changed).

## Running Python Commands

### Basic Syntax

```zephyr
python ? run:<*pythonCommand>;
```

The command is written as a string in double quotes (not single quotes).

### Example

```zephyr
__ ? LIB:./lib/python.py;
python # python:;

python ? run:(print("Hello from Python!"));
```

## Python Command Format

### Using Parentheses for Direct Commands

```zephyr
python ? run:(print("Direct command"));
python ? run:(import time);
python ? run:(x = 5 + 3);
```

### Using Variables as Commands

```zephyr
command # PT:"print('Hello')";
python ? run:'command';
```

Note: No parentheses when using variables.

## Important Notes

### Use Double Quotes, Not Single Quotes

```zephyr
§ CORRECT: Double quotes inside the parentheses
python ? run:(print("Hello"));

§ WRONG: Single quotes cause errors
python ? run:(print('Hello'));
```

### Accessing Zephyr Variables in Python

When using variables from your Zephyr program, don't use parentheses:

```zephyr
value # INT:42;

§ CORRECT: Use variable without parentheses
python ? run:'value';

§ WRONG: This would fail
python ? run:(value);
```

## Practical Python Examples

### Example 1: Simple Output

```zephyr
__ ? LIB:./lib/python.py;
python # python:;

python ? run:(print("Hello from Python"));
python ? run:(print("This runs Python code"));
```

### Example 2: Basic Math in Python

```zephyr
python ? run:(result = 5 + 3);
python ? run:(print(result));
```

### Example 3: String Operations

```zephyr
python ? run:(text = "Hello" + " " + "World");
python ? run:(print(text));
```

### Example 4: Lists in Python

```zephyr
python ? run:(numbers = [1, 2, 3, 4, 5]);
python ? run:(print(sum(numbers)));
```

### Example 5: Using Zephyr Variables in Python

```zephyr
name # PT:"Alice";
age # INT:30;

python ? run:(print("Name: " + 'name'));
python ? run:(print("Age: " + str('age')));
```

### Example 6: Loops in Python

```zephyr
python ? run:(
  for i in range(1, 6):
      print(i)
));
```

### Example 7: Conditional Logic

```zephyr
python ? run:(
  x = 10
  if x > 5:
      print("x is greater than 5")
  else:
      print("x is 5 or less")
));
```

## Combining Zephyr and Python

### Example 1: Process Data

```zephyr
data # PT:"10,20,30,40,50";
result # PT:"";

python ? run:(
  numbers = [int(x) for x in 'data'.split(",")]
  total = sum(numbers)
  print(f"Total: {total}")
));
```

### Example 2: Generate Data

```zephyr
__ ? LIB:./lib/python.py;
python # python:;

python ? run:(
  import random
  random_nums = [random.randint(1, 100) for _ in range(5)]
  print(random_nums)
));
```

### Example 3: File Operations

```zephyr
python ? run:(
  with open("data.txt", "w") as f:
      f.write("Hello from Python\n")
      f.write("This is a test\n")
));

python ? run:(
  with open("data.txt", "r") as f:
      content = f.read()
      print(content)
));
```

## Complex Python Commands

### Multi-Line Python

For complex code, you can write multi-line Python:

```zephyr
python ? run:(
  def fibonacci(n):
      if n <= 1:
          return n
      return fibonacci(n-1) + fibonacci(n-2)
  
  for i in range(10):
      print(fibonacci(i))
));
```

### Using Python Libraries

```zephyr
python ? run:(
  import math
  print(math.sqrt(16))  § Output: 4.0
));

python ? run:(
  import json
  data = {"name": "Alice", "age": 30}
  print(json.dumps(data))
));
```

## Best Practices

1. **Use double quotes** - Always in Python commands
2. **Test Python independently** - Verify Python code works first
3. **Keep it simple** - Complex Python is hard to debug
4. **Document integration** - Explain how Python code connects to Zephyr
5. **Handle errors** - Python errors may stop your program

## Practical Scenarios

### Scenario 1: Data Transformation

```zephyr
input_data # PT:"5,10,15,20";
output # PT:"";

python ? run:(
  values = [int(x) for x in 'input_data'.split(",")]
  doubled = [x * 2 for x in values]
  'output' = ",".join(map(str, doubled))
));

output ? push:;
```

### Scenario 2: Statistics

```zephyr
python ? run:(
  numbers = [10, 20, 30, 40, 50]
  average = sum(numbers) / len(numbers)
  print(f"Average: {average}")
));
```

### Scenario 3: Date/Time Operations

```zephyr
python ? run:(
  from datetime import datetime
  now = datetime.now()
  print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
));
```

## Tips for Using Python

1. **Test inline code first** - Make sure Python code works before integrating
2. **Use triple quotes for multi-line** - Helps with complex code
3. **Print for debugging** - Use print() to see what's happening
4. **Escape special characters** - Be careful with quotes
5. **Remember context** - Each command runs in sequence but may share state

## Common Issues

### Issue: Quote Escaping

```zephyr
§ WRONG: Single quotes inside Python
python ? run:(print('Hello'));  § ERROR!

§ CORRECT: Double quotes or escaping
python ? run:(print("Hello"));
```

### Issue: Variable Access

```zephyr
value # INT:42;

§ WRONG: Using parentheses
python ? run:(print(value));  § ERROR!

§ CORRECT: Without parentheses
python ? run:(print('value'));
```

## Summary

| Task | Example |
|------|---------|
| Import | `__ ? LIB:./lib/python.py;` |
| Create | `python # python:;` |
| Run command | `python ? run:(print("Hi"));` |
| Use variable | `python ? run:(print('varname'));` |
| Multi-line | Use parentheses with multiple statements |

## Next Steps

- Combine with [System Library](03-system.md)
- Use with [File Management](../Types/09-FileManagement.md)
- Try with [Variables](../Types/01-simpleVariable.md) for data processing
