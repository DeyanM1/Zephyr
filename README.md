# Zephyr

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
LIB = Library

  
~1 = True
~0 = False
```


## Commands

```
? - For using Variables
# - For Declaring Variables

~ - command (ignoring whole line)
```

  

# Tutorials

## Build-in Functions
Are functions that can be used without a definition
```
__ ? JUMP:<lINE>; Jumps to a certain !!function!! Not LINE
```
## Variables

```
# Declare Variables
<Variable Name> # <Type>:<Value>(|<~1>/<~0>); <- For absolutes

# change type
<Variable Name> # CT:<Type>;

# change value
<Variable Name> ? w:<Value>; Value has to be the right type
```
### INT
```
<Variable Name> ? w:++; Increment Value by 1
<Variable Name> ? w:--; Decrement Value by 1
```
### PT
```

<Variable Name> ? push:; -> print value
<Variable Name> ? INPUT:<optional Input message>; -> takes user input
```
### Random Number Generator
types: INT
```
<Variable Name> # RNG:<Random number type>|<range>;
<range> Format: 0->30 (30 & 0 inclusive)

# change range
<variable Name> ? CR:<range>;


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


## Predefined Variables
You can define variables in a python script and use them in
the file goes inside the lib library
filename without extension
```
__ ? PredefVars:<filename>
```

## create Predefined Variable Files
### Structure
#### File Structure
predefVar files are in lib directory: 

    lib/
    └── examplePredefVars.json
    main.py
    functions.py
    code.lys

#### Code Structure
Types supported: INT, PT, MO, FUNC, CO, RNG
```json
{
    "<Variable Name>": {
        "type": "<Variable Type>",
        "value": "<Variable Value>",
        "const": false
        <etc>
    }
}
```

## Libraries
Create custom function for Zephyr code
Library file name without extension eg. ".py"
```zephyr
# Declare Library
<Variable Name> # LIB:<library file name>;

# Use Library
<Variable Name> ? <Function>:<Params>;
```


# Create Library
## Structure
#### File Structure
libraries are in lib directory: 

    lib/
    └── exampleLibrary.py
    main.py
    functions.py
    code.lys
#### Code Structure
1. search function:
search function is necessary; checking if statements can be change
```python
def search(name, func, base, paramsList, codeLine):  # Takes necessary parameters
    match func: # Checks function char
        case "?": # If char is "?"
            match base: # checks Base function
                case "add10": # If base is add10: run add10 function
                    vars = add10(vars, vars[paramsList[0]]) # edits variables from add10 function
    
    return vars # returns edited variables to compiler

def add10(vars, var):
    a = int(var.value)
    b = a + 10
    var.value = str(b)
    
    vars.update({var.name: var}) # updates variables
    return vars # returns edited variables
```
Custom function can be added
