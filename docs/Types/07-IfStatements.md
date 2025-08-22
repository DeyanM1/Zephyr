# IF-Statements

If statements are used to add logic to your program.

**Declare a IF statement**
```zephyr
statement # IF:<conditionalObjectName>|<commandsInIF>;

statement ? ELSE:<commandsInIF>;

statement ? END:;
```

commandsInIF is the count of commands in IF statement

**Example:**
```
conditionalObject # CO:('a' > 'b')

statement # IF:conditionalObject|1;

~ A is greater than b

statement ? ELSE:1;
~ B is greater than A

statement ? END:;
```
