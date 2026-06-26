# Ascii

Ascii provides simple functions to turn ascii codes to chars and reverse.

---

## Properties

- **`convertibleInto`** -> `None`
- **`convertValue`** -> Cant convert

## Setup

Before using ascii, import the library:

```zephyr
__ ? LIB:ascii.py;
```

## Methods

### Define
Creates a Ascii interface. No arguments are needed.

```zephyr
ascii # ASCII:;
```

### ToAscii
Converts a character into a ascii code


```zephyr
ascii ? ToAscii:<* CharToConvert>|<* TargetVarName>; 
```

- **CharToConvert**: Char to convert (Var Type: PT)
- **TargetVarName**: Name of the var where the Num is pasted into (Var Type: INT/FLOAT)


### ToChar
Converts an Ascii Code into a char


```zephyr
ascii ? ToChar:<* NumToConvert>|<* TargetVarName>; 
```

- **NumToConvert**: Num to convert (Var Type INT/FLOAT)
- **TargetVarName**: Name of the var where the char is pasted into
