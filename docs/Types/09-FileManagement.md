# File Management

A File object manages file operations including opening, reading, writing, renaming, and deleting files. File objects allow Zephyr programs to store and manipulate external data. The variable's value is the absolute path to the file.

- **`g`** means global - ex. change file name

- **`c`** means content - modifies content

---

## Properties

- **`convertibleInto`** -> `None`
- **`convertValue`** -> None
   

## Methods

### Define
Creates or opens a file at the specified path.

```zephyr
file # FILE:<*Path>; 
file # FILE:"data.txt";
```

- **`Path`** — File path either relative or absolute (defaults to `'unnamed_file.txt'` if not provided)


### Write (w)
Changes the file path to point to a different file.

```zephyr
file ? w:<*Path>;
file ? w:"newfile.txt";
```

### Set Content (cSET)
Writes content to the file, replacing any existing content.

```zephyr
file ? cSET:<*Content>;
file ? cSET:"Hello, World!";
```

### Clear Content (cFLUSH)
Removes all content from the file.

```zephyr
file ? cFLUSH:;
```

### Read Content (cREAD)
Reads the content of a file and loads it onto a PT or LIST

```zephyr
file ? cREAD:<* targetVarname>|<*- cleanLines>;

content # LIST:;
file ? cREAD:content|~1;
```

- **targetVarName**: name of the variable the content is pasted into. Allowed Types are: `PT`, `LIST`. At PT the lines are combined to a single string. At LIST the lines are split and put on the Positive List Collection
- **cleanLines**: Boolean switch if the lines are cleaned (remove Whitespaces, linebreaks)


### Rename (gRENAME)
Renames the file to a new name.

```zephyr
file ? gRENAME:<*NewName>;
file ? gRENAME:"renamed.txt";
```

### Delete (gDEL)
Deletes the file permanently.

```zephyr
file ? gDEL:;
```


## Notes

- The file's value field stores the absolute path to the current file.
- Writing with `cSET` overwrites all existing file content.
- Use `cFLUSH` to clear content without deleting the file itself.
- File names should include the file extension (e.g., `.txt`, `.log`).
- All path operations are system-dependent.
