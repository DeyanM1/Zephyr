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

There are three options on how to import  a lib:
### 1. Absolute Path:
```zepyhr
__ ? LIB:/home/<User>/libs/GPIO.py;
```

### 2. Relative Path:
- Looks in the current working dir inside myLibs
```zepyhr
__ ? LIB:./myLibs/GPIO.py;
```

### 3. Bare Name:
- Looks inside of the global install dir, if none found it looks inside of local ./lib dir in the cwd
```zepyhr
__ ? LIB:GPIO.py;
```

After importing, you can use the library's features (see library-specific documentation).


## Using Libraries

Import a library into your Zephyr script using the built-in `LIB` command:

```zephyr
__ ? LIB:GPIO.py;
```

Zephyr resolves the library path in one of the three ways depending on waht you provide:

---
### 1. Absolute Path

Provide a full path starting from the filesystem root. Zephyr uses it directly with no additional lookup.

```zepyhr
__ ? LIB:/home/user/libs/GPIO.py;
```

### 2. Relative Path

Provide a apth containing a separator (e.g. `./`, `../`, or a subfolder). Zephyr resolves it relative to the **directory of the current `.zph`file**, not the working directory of the process.

```zepyhr
__ ? LIB:./myLibs/GPIO.py;
__ ? LIB:../shared/GPIO.py;
```

---

### 3. Bare Name

Provide just a filename with no path separators. Zephyr searches in this order:

1. **Global library directory** - the path set by you Zephyr installation (e.g `~/.config/Zephyr/libs/`)
2. **Local `lib/` directory** - a `lib/`fodler next to the current `.zph` file

The first match wins. If neither location contains the file, en error is raised.

```zephyr
__ ? LIB:GPIO.py;
```

> **Tip:** The bare name is the recommended way to use officially installed libraries. Use relative paths for project-local modules.



### Organizing Libraries

Keep libraries organized in your project:

```
my_project/
  ├── src/
  │   ├── main.zph
  │   └── lib/
  │       ├── GPIO.py
  │       ├── python.py
  └─      └── system.py
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
