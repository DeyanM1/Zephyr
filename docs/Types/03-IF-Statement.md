# IF-Statement

IF statements execute a block of code only if the related Conditional Object evaluates to true. They optionally allow an ELSE block for false conditions.


* Define:

**`commandsInIF/ELSE`** refers to the count of individual commands in the if/else block.
Blank lines or lines with just a comment are not counted.

```zephyr

statement # IF:<*conditionalObjectName>;

statement ? START:<*commandsInIF>;

statement ? ELSE:<*commandsInELSE>;

statement ? END:;

```

* Change condition:

```

if ? w:<*ConditionalObjectName>;

```

* Example:
  
```zephyr
conditionalObject # CO:('a' > 'b')

statement # IF:conditionalObject;

statement ? START:0;
~ A is greater than b

statement ? ELSE:0;
~ B is greater than A

statement ? END:;
```
