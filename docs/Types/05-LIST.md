# List

A List is an ordered collection of values of a single type. Its value represents the current pointer position. Lists support random access to elements and dynamic position changes.

---


## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`
- **`convertValue`** -> Value at current Pointer position

## Methods

### Define
Creates a new List with a specified value type.

```zephyr
list # LIST:<*ValueType>|<*-InitialValue1>|<*-InitialValue2>|...;
myList # LIST:INT|5|1;
```

- **`ValueType`** — Type of values stored: `INT`, `PT`, or `FLOAT`
- **`InitialValue`** — (Optional) initial value to store

### Set Pointer (SET)
Moves the pointer to a specified position. Valid positions are any integer positive and negative except 0.

```zephyr
list ? SET:<* position>; 
myList ? SET:2;
```

### Write (w)
Writes a value at the current pointer position.

```zephyr
list ? w:<*- value>; 
myList ? w:10;
```

### Length

To get the length of either the pos or neg values of a list use  ? LGTH.

```zephyr
list ? LGTH:<* CollectionType>|<* targetVar>

length # INT:;
list ? LGTH:POS|length;
```

- **CollectionType**: Either POS or NEG to select one of the two collections
- **targetVar**: name of the Variable the length value is pasted into


### Copy

Copies the pos / neg values of a list to a target list with a compatible ValueType

```zephyr
list ? copy:<* targetVar>;

list1 # LIST:INT|1|2|3;
list2 # LIST:PT;

list1 ? copy:list2;
```

- **targetVar**: The name of the Variable the content is pasted into.

## Reading from a List

To read a value from a list and assign it to another variable, use single quotes with the list name:

```zephyr
result ? w:'myList';              § Read value at current pointer
result ? w:'myList<2>';           § Read value at position 2
result ? w:'myList<'index'>';     § Read value at position stored in variable index
result ? w:'myList<'myList<2>'>;  § Nested list access (can nest infinitely)
```

- The infinite nesting can be used everywhere a value can be replaced with a variable (*)



## Notes

- Pointer positions are 1-indexed and can be any integer except 0 (positive or negative).
- Attempting to read from an unset position may result in undefined behavior.
- List values can be read using nested variable syntax with single quotes.
