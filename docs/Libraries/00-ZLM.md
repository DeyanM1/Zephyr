# Zephyr Library Manager (ZLM)

The Zephyr Library Manager (zlm.py) is a tool for installing and removing libraries. Libraries extend Zephyr's functionality with additional features like hardware control, Python integration, and system operations.

## Understanding Libraries

Libraries are reusable code modules that add new capabilities to Zephyr:

- **GPIO**: Control hardware pins and devices
- **Python**: Run Python code from Zephyr
- **System**: Perform system-level operations
- Custom libraries created by developers

Libraries must be imported into your program before you can use them.

## Installing Libraries

### Basic Installation

Install libraries to a specific directory:

```bash
python zlm.py install --path "src/lib/" GPIO.py moreMath.py
```

This command:
- Installs GPIO.py and moreMath.py
- Places them in the `src/lib/` directory
- Makes them available for local projects

### Default Installation

If you don't specify a path, libraries go to a `lib` directory in your current location:

```bash
python zlm.py install GPIO.py
```

Creates: `./lib/GPIO.py`

### Global Installation

Install libraries system-wide (available to all Zephyr projects):

```bash
python zlm.py install --global GPIO.py
```

**Note**: Global installation is disabled by default for security.

## Uninstalling Libraries

Remove globally installed libraries:

```bash
python zlm.py uninstall GPIO.py
```

**Important**: This removes globally installed libraries only. To remove local project libraries, delete them manually from your project directory.

## Using Libraries in Your Program

Once installed, import a library using the built-in `LIB` command:

```zephyr
__ ? LIB:./lib/GPIO.py;
```

After importing, you can use the library's features (see library-specific documentation).

## Example Workflow

### Step 1: Install the Library

```bash
python zlm.py install --path "src/lib/" GPIO.py
```

### Step 2: Create Your Program

```zephyr
§ File: blink.zph

§ Import the GPIO library
__ ? LIB:./lib/GPIO.py;

§ Now you can use GPIO functions
gpio # GPIO:BCM;
gpio ? SETUP:17|OUT;
gpio ? SET:17|1;
```

### Step 3: Run Your Program

```bash
python src/zcli.py blink.zph
```

## Best Practices

### Local vs Global Installation

**Use local installation for:**
- Project-specific libraries
- Custom libraries you created
- Testing new versions
- Team collaboration (libraries are in your repo)

**Use global installation for:**
- Standard libraries used across many projects
- System libraries (if enabled)
- Common utilities

### Organizing Libraries

Keep libraries organized in your project:

```
my_project/
  ├── src/
  │   ├── main.zph
  │   └── lib/
  │       ├── GPIO.py
  │       ├── python.py
  │       └── system.py
  └── data/
```

### Library Management

1. **Check what's installed**: Look in your lib directory
2. **Document dependencies**: Note which libraries your programs need
3. **Keep backups**: Save copies of important libraries
4. **Version control**: Commit libraries to your repository

## Common Library Installation Commands

### Basic Libraries

```bash
§ GPIO - Hardware control
python zlm.py install --path "src/lib/" GPIO.py

§ Python - Python integration
python zlm.py install --path "src/lib/" python.py

§ System - System operations
python zlm.py install --path "src/lib/" system.py
```

### Multiple Libraries at Once

```bash
python zlm.py install --path "src/lib/" GPIO.py python.py system.py
```

## Troubleshooting

### Library Not Found

```zephyr
§ Error: Library file not found
__ ? LIB:./lib/GPIO.py;  § Make sure the path is correct
```

**Solutions**:
1. Check the file exists: `ls ./lib/GPIO.py`
2. Verify the spelling
3. Use absolute paths if relative paths don't work
4. Reinstall the library

### Feature Not Available

If a library import succeeds but features don't work:

1. Verify the library is the right one
2. Check the library's documentation
3. Ensure dependencies are installed
4. Reinstall the library

## Advanced: Creating Custom Libraries

You can create your own libraries by writing Python code. See each library's documentation for structure and examples.

## Library Documentation

After installing, see these guides for library-specific features:

- [GPIO Library](01-GPIO.md) - Control hardware pins
- [Python Library](02-Python.md) - Run Python code
- [System Library](03-system.md) - System operations

## Summary

| Task | Command |
|------|---------|
| Install local | `python zlm.py install --path "src/lib/" LIB.py` |
| Install global | `python zlm.py install --global LIB.py` |
| Uninstall | `python zlm.py uninstall LIB.py` |
| Use in program | `__ ? LIB:./lib/LIB.py;` |

## Next Steps

- Explore [GPIO Library](01-GPIO.md) for hardware control
- Learn [Python Library](02-Python.md) integration
- Try [System Library](03-system.md) commands
