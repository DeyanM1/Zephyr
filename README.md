# Zephyr

# Usage:

**values with * can be variablenames in ''**
**values with - are optional in the current command**

## Simple Vars:
Variable can be changed into: INT, PT, FLOAT
```
var # <Vartype>:<*- Value>; // Define SimpleVar| Vartype can be INT, PT, FLOAT
var ? w:<*NewValue>; // change Value
var ? w:++|<*- incrementBy>; // Increment INT/FLOAT by incrementBy. if not set increment 1
var ? w:-|<*- decrementBy>; // Decrement INT/FLOAT by decrementBy. if not set decrement 1
var ? push:; // Print value of PT to console 
var ? INPUT:<*- Message> // Takes input and overrides previous value. optionalMessage is printed Before
```

## Condtitional Object:
Variable can be changed into: INT, PT, FLOAT
OnChange: value is eval of condition
```
co # CO:<*- ConditionScript>; # Define CO
co ? w:<*conditionScript>;

conditionScript in format: ('a'>'b')
```

## IF
Variable cant be changed.
```
if # IF:<*- ConditionalObjectName>;
if ? w:<*ConditionalObjectName>;
if ? START:<*commandsInIF>;
if ? ELSE: <*commandsInELSE>;
if ? END:;
```

## LOOP
Variable can be changed into: INT, PT, FLOAT
OnChange: count of times looped
```
loop # LOOP:<*- conditionalObjectName>;
loop ? w:<*ConditionalObjectName>;
loop ? START:<*commandsInLOOP>;
loop ? END:;
```

## Math Object
Variable can be changed into: INT, PT, FLOAT
OnChange: value is result of equation
info: result is calculated on equationScript set/change
```
mo # MO:<*- equationScript>;
mo ? w:<* equationScript>;
```

## Function
Variable can be changed into: INT, PT, FLOAT
OnChange: value is result of equation
info: result is calculated on call
```
func # FUNC:<resultType>|<*- disableVariableChange>|<*- mathObjectName>
func ? w:<* mathObjectName>;
func ? call:;
```

## Random Number Generator
Variable can be changed into: INT, PT, FLOAT
OnChange: value is generated random Number
```
rng # RNG:<*- rangeMin>|<*- rangeMax>|<*- numberType>;
rng ? w:<* rangeMin>|<* rangeMax>|<* numberType>;

```

## BuildIn
Variable cant be changed.
Info: doesnt have to be defined. name is always __
```
__ ? wait:<* secondsToWait>;
__ ? jump:<* relativePositionInCode>;
__ ? jumpTo:<* absolutePositionInCode>;

__ ? export:<*- exportPath>; // exports all currently used Variables. <exportPath> can be relative to cwd or absolute. if unset output file is the name of the .zph file with .zpkg ending
__ ? load:<*- importPath>; // imports all variables saved in .zpkg                                                                                                . <importPath> is the same as exportPath

__ ? LIB:<* libFilePath>; // import library. <libFilePath> is the relative or absolute path of the python file with .py extension
```



## File
Variable cant be changed.
OnChange: value is absolute Path of opened File
```
file # FILE:<*- path>; // <path> is absolute or relative path to current working dir. if not set uses unnamed_file.txt in cwd.
file ? w:<* path>; // <path> is absolute or relative path to current working dir.

file ? cSET:<* content>; // cSET replaces all the content of the opened file with <content>
file ? cFLUSH:; // cleares the content of the FILE

file ? gRENAME:<* newName>; // renames the current file to <newName>
file ? gDEL:; // deletes the current FILE

```


## GPIO
OnChange: value is status of last read pin
```
lib # LIB:GPIO; // Import GPIO

gpio # GPIO:<* pinoutType>; // define the GPIO library. <pinoutType> is BCM or Board
gpio ? SETUP:<* pinNum>|<* pinType>; // Set pin to input or output. <pinNum> is integer id of the pin. <pinType> is either IN or OUT
gpio ? SET:<* pinNum>|<* pinValue>; // Set pin to HIGH or LOW. <pinValue> is integer 1/0.
gpio ? READ:<* pinNum>; // Read value of pin. only works if pin is set to INPUT
gpio ? CLEAN:; // cleans all pins. Good practise to cleanup after usage
```