# System

The System library provides control over basic system behavior, including program termination and working directory management.

---



## Setup

Before using System, import the library:

```zephyr
__ ? LIB:system.py;
```

## Methods

### Define
Creates a System interface. No arguments are needed.

```zephyr
system # SYSTEM:;
```

### Quit
Terminates the program with an optional error code. Default error code is 0 (success).

```zephyr
system ? quit:<*- ErrorCode>;
system ? quit:0;
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
