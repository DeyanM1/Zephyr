# List

Supported types: `INT`. `FLOAT`. `PT`
Value is current pointer position

* Define:
```

list # LIST:<* ValueType>|<*- value>|<*- pointerPosition>;    § <valueType> can be INT, PT, FLOAT | <value> is the value that is set at the pointer

```

* set Pointer:
```

list ? SET:<* position>;    § position is a integer from -Inf to +Inf without 0. default is 1

```

* write:
```

list ? w:<*- value>;    § Write value to current pointer position

```

* Set var Value from list (read):

this function applies to all functions where a value can be taken from a variable (*)

```

var ? w:'list';             § value at the current pointer position is taken
var ? w:'list<2>';          § Value at the given position in <>
var ? w:'list<'myInt'>';    § Value at the position with the value from the integer myInt.
var ? w:'list<'list<'...'>'>';  § You can infinitly use nested variables in list index

```
