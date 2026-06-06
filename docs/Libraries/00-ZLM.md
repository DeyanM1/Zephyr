# Zephyr Library Manager (ZLM)

The Zephyr Library Manager (zlm.py) is a tool for installing and removing libraries. Libraries extend Zephyr's functionality with additional features.

## Understanding Libraries

- Libraries are new Variable Types.
- Libraries must be imported into your program before you can use them.

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

If you don't specify a path, libraries go to a `lib` directory in your current working directory:

```bash
python zlm.py install <LibraryName>
python zlm.py install GPIO.py
```

Creates: `./lib/GPIO.py`

### Global Installation

Install libraries system-wide (available to all Zephyr projects):

```bash
python zlm.py install --global <LibraryName>
python zlm.py install --global GPIO.py
```

**Note**: Global installation is disabled by default for security.

## Uninstalling Libraries

Remove locally installed libraries:

```bash
python zlm.py uninstall <LibraryName>
python zlm.py uninstall GPIO.py
```

**Important**: To remove a library from the global installation location include the --global flag.

## Using Libraries 

Once installed, import a library using the built-in `LIB` command:

```zephyr
__ ? LIB:./lib/GPIO.py;
```

After importing, you can use the library's features (see library-specific documentation).



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

### Multiple Libraries at Once

```bash
python zlm.py install --path "src/lib/" GPIO.py python.py system.py
```


## Advanced: Creating Custom Libraries

You can create your own libraries by writing Python code. See each library's documentation for structure and examples.

### Summary

| Task | Command |
|------|---------|
| Install local | `python zlm.py install --path "src/lib/" LIB.py` |
| Install global | `python zlm.py install --global LIB.py` |
| Uninstall | `python zlm.py uninstall LIB.py` |
| Use in program | `__ ? LIB:./lib/LIB.py;` |
