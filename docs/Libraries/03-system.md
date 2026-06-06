# System

The System library provides control over basic system behavior, including program termination and working directory management.

---



## Setup

Before using System, import the library:

```zephyr
__ ? LIB:"./lib/system.py";
```

## Methods

### Define
Creates a System interface. No arguments are needed.

```zephyr
system # system:;
```

### Exit
Terminates the program with an optional error code. Default error code is 0 (success).

```zephyr
system ? exit:<*- ErrorCode>;
system ? exit:0;
```

**ErrorCode values:**
- `0` — Success (program completed normally)
- Any non-zero integer — Indicates an error or failure condition

### Get Current Working Directory (getCWD)
Retrieves the current working directory and stores it in a text variable.

```zephyr
system ? getCWD:<* variableNameToSaveTo>;
system ? getCWD:pathVariable;
```



## Notes

- Exit codes are standard Unix convention: 0 for success, non-zero for errors.
- The program terminates immediately when `exit` is called.
- The `getCWD` method returns the directory path as a text string suitable for further operations.
- All System operations are blocking—the program waits for completion before proceeding.
