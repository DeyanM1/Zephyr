# Files

Files are used to open Files from the computer to read and write to it.

**open a file**
```zephyr
<VariableName> # FILE:<fileName>|~1/~0;
```

always creates a File if not existent
`~1` -> delete content of file and open for edit & write
`~0` (default) -> open for edit & write

**Basic actions**
```zephyr
~ Clear a File
<VariableName> ? clear:<lineNumber>;

~ Delete File
<VariableName> ? delete:~0/~1;

~ Rename a File
<VariableName> ? rename:<newName>|~1/~0;

~ close and repoen a File after editing
<VariableName> ? close:;
<VariableName> ? reopen:;
```
- clear:
`<lineNumber>` -> optional line Number to clear | Variable name supported in `' '`
- delete:
`~1` -> delete only if empty
`~0` (default) -> force delete
- rename:
`~1` -> delete content
`~0` (default) -> keep content

**Write**
```zephyr
~ write to a specific Line
<VariableName> ? w:<pos>|<value>;

~ append to the file
<VariableName> ? a:<value>;

~ insert to the file
<VariableName> ? i:<pos>|<value>;

~ replace a file
<VariableName> ? rep:<listName>|<startingIndex>;
```
- write
`pos` can be every number from 1 | INT Variable names supported in `' '`
`value` can be every char combination except `; ' :` | PT Variable names supported in `' '`
- append
appends always to one after the last line
`value` can be every char combination except `; ' :` | PT Variable names supported in `' '`
- insert
insert a value in a line shifting all values after the pos to the right
`pos` can be every number from 1 | INT Variable names supported in `' '`
`value` can be every char combination except `; ' :` | PT Variable names supported in `' '`
- replace
replaces an entire File with a List
`listName` -> Name of the list variable in `' '`
`startingIndex` -> optional starting index to start replacing with a shift | INT Variable name support

**Read** (Coming Soon)
