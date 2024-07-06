
# Z-Lang

My own Varaible based programming language

  
  
# Syntax
## Writing
VARIABLES ARE LOWERCASE!

```
<VariableName> <Command>:<Argument1>|<Argument2>|<...>;

```

  

## Types

```
PT = Printable Text
MO = Math Object
INT = Integer

  

~1 = True
~0 = False

```


## Commands

```
? - For using Variables
# - For Declaring Variables, changing Types
```

  

# Tutorials

## Variables

```
# Declare Variables
<Variable Name> # <Type>:<Value>(|<~1>/<~0>); <- For absolutes

 
# change value
<Variable Name> ? w:<Value>; Value has to be the right type


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