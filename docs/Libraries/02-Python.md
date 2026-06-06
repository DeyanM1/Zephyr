# Python

The Python library allows Zephyr programs to execute Python code directly from within Zephyr scripts. This enables integration with Python libraries and advanced system operations.

---

## Setup

Before using Python, import the library:

```zephyr
__ ? LIB:"./lib/python.py";
```

## Methods

### Define
Creates a Python interface. No arguments are needed.

```zephyr
python # python:;
```

### Run (run)
Executes a Python command or statement.

```zephyr
python ? run:<* pythonCommand>;
python ? run:(print("Hello World"));
```

## Python Command Format

Python commands are written in Zephyr as follows:

- Enclose Python code in parentheses
- Use double quotes instead of single quotes for strings
- To use a Zephyr variable value, reference it with quotes



## Notes

- Python commands run with full access to Python standard library.
- Use double quotes for Python strings, not single quotes.
- Be careful when executing untrusted Python code, as it runs with the same permissions as the Zephyr interpreter.

