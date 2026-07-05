# Math

Math provides usueful mathematic functions.

--- 

## Properties

- **`convertibleInto`** -> `None`
- **`convertValue`** -> Cant convert

- **INFO:** when using a function the caluclated var is written to the variable entered

## Setup

Before using Math, import the library:

```zephyr
__ ? LIB:MATH.py;
```

## Methods

### Define
Creates a MATH interface. No arguments are needed.

```zephyr
math # MATH:;
```

### Factorial
Calculate the Factorial of the value at the given Var.

```zephyr
math ? fact:<* variableName>;
math ? fact:myVar;
```


### Absolute
Calculate the Absolute of the value at the given Var.

```zephyr
math ? abs:<* variableName>;
math ? abs:myVar;
```


### PI 
Set the Value of PI at the given Var.

```zephyr
math ? setPi:<* variableName>;
math ? setPi:myVar;
```


### sqrt
Calculate the square Root of the value at the given Var.

```zephyr
math ? sqrt:<* variableName>;
math ? sqrt:myVar;
```

### Max
Get the biggest number of the positive Collection of a List

```zephyr
math ? max:<*- listVarName>|<*- TargetVarName>;
math ? max:myList|biggestNum;
```