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
LOOP = Loops
CO = Conditional Object

  
~1 = True
~0 = False
```


## Commands

```
? - For using Variables
# - For Declaring Variables
```

  

# Tutorials

## Buildin Functions
Are functions that can be used without a definition
```
__ ? JUMP:<lINE>; Jumps to a certain !!function!! Not LINE
```
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

At type change result is the value of the Variable
```
# Declare MO 
<Variable Name> # MO:; -> With Undefined state

# Pass equation
<Variable Name> ? (<equation>):;
Format: ('a'+'b')  

# change equation
<Variable Name> ? w:<Equation>;
```
## Functions
At type change result is the value of the Variable
Return Types: RES -> Result
```
# Declare Function
<Variable Name> # FUNC:<returnType>|(~1/~0); [1] With Undefined state ; [2] if the used variables can change if you call the function after variable change

# Pass 
<Variable Name> ? (<equation>)
Format: ('a'+'b')

# Functions have to be called to activate:
<Variable Name> ? call:;
```

## Loops
Forever loop repeat maximum 65536 times
conditional object can be boolean value to make loop infinite

```
# Declare Loop
<Variable Name> # LOOP:<Conditional Object name>;

conditional object can be boolean value to make loop infinite


# End Loop
<Variable Name> ? END:;
```

## Conditional Objects
Returns ~1 / ~0
Conditions: <  > != == <= >=
```
# Declare Conditional Object
<Variable Name> # CO:(<condition>);
Format: ('a'>'b')
```
At change type value is the return and can be printed