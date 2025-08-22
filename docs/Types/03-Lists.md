# Lists

Lists are variables that hold multiple values of the same type. It will fill spaces between values with null values.
Lists don't support type changes

POS = 1 to +Inf
NEG-POS = -1 to -Inf

OptionalData from 1 to +Inf

Supported types: Variables
**Declare a list:**

- usage:
```zephyr
~ define
myList # LIST:<ElementsType>|optionalData;
myList ? SET:<pos>|<data>;
myList ? SET:'myPosVar'|'myPosValue';

~ read to supported types from a LIST
myNum # INT:0;
myNum ? w:'myList<pos>';
```
- define
**`optionalData Syntax`**: `..|5,1,5,2`  /  `..|test1,test2,test3`
**`pos`**: can be from 1 to +Inf or from -1 to -Inf. | INT, LIST Variable name support if in `' '`
**`data`**: can be any value which the type supports| PT, LIST Variable name support if in `' '`
- read
**`pos`** must be in `< >`
variable name must be in `' '`

---
## ALIST (Coming Soon)
A Allocated List is a list that does'nt fill spaces between values. It saves memory.
The positioning Commands are like a normal List.
