
# Lysia code

My own Variable based programming language

  
# Syntax
## Writing
VARIABLES ARE LOWERCASE!

```
<VariableName> <Command>:<Argument1>|<Argument2>|<...>;

```

  

## Types

```
PT = Printable Text
INT = Integer
MO = Math Object
FUNC = Function 

  
~1 = True
~0 = False

```


## Commands

```
? - For using Variables
# - For Declaring Variables
```

  

# Tutorials

## Variables

```
# Declare Variables
<Variable Name> # <Type>:<Value>(|<~1>/<~0>); <- For absolutes

 
# change value
<Variable Name> ? w:<Value>; Value has to be the right type
<Variable Name> ? w:++; Increment Value by 1
<Variable Name> ? w:--; Decrement Value by 1


# change type
<Variable Name> ? CT:<Type>;


# print value
<Variable Name> ? push:; -> Variable type has to be PT
```

## Math Objects

```
# Declare MO 
<Variable Name> # MO:; -> With Undefined state

# Pass equation
<Variable Name> ? (<equation>)
Format: ('a'+'b')  
```
## Functions
Return Types: RES -> Result
```
# Declare Function
<Variable Name> # FUNC:<returnType>|(~1/~0); [1] With Undefined state ; [2] if the used variables can change if you call the function after variable change

# Pass 
<Variable Name> ? (<equation>)
Format: ('a'+'b')

# Functions have to be called:
<Variable Name> ? call:;
```