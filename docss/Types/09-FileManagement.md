# File Management

Variable state cannot be changed. Value is the absolute path.

File objects manage opening, editing, renaming, and deleting files. They allow Zephyr programs to store and manipulate external data.

* Open file:

```

file # FILE:<*Path>;  § Defaults to 'unnamed_file.txt'

```

* Change file path:

```

file ? w:<*Path>;

```

* Set file content:

```

file ? cSET:<*Content>;

```

* Clear file content:

```

file ? cFLUSH:;

```

* Rename file:

```

file ? gRENAME:<*NewName>;

```

* Delete file:

```

file ? gDEL:;

```