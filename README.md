# Zephyr

# Usage:

**values with * can be variablenames in ''**
**values with - are optional in the current command**

## Simple Vars:
Variable can be changed into: INT, PT, FLOAT
```
var # <Vartype>:<*- Value>; // Define SimpleVar| Vartype can be INT, PT, FLOAT
var ? w:<*NewValue>; // change Value
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
rng # RNG:<*- numberType>|<*- rangeMin><*- rangeMax>;
rng ? w:<* numberType>|<* rangeMin><* rangeMax>;

```

## BuildIn
Variable cant be changed.
Info: doesnt have to be defined. name is always __
```
__ ? wait:<* secondsToWait>;
__ ? jump:<* relativePositionInCode>;
__ ? jumpTo:<* absolutePositionInCode>;
```


## Library
Variable cant be changed.
```
lib # LIB:<*- libName>;
lib ? w:<* libName>;

```