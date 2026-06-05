# File Management

File objects allow your Zephyr program to create, read, and modify files on your computer. This is useful for saving data, logging information, or working with text files.

## Understanding File Objects

File objects are special because:
- Their path **cannot be changed** after creation (it's write-protected)
- Each File object manages one file
- You can read from, write to, and delete files

## Creating a File Object

```zephyr
<VariableName> # FILE:<*Path>;
```

- **Path**: The file path (can be absolute or relative)
- Default file name is `unnamed_file.txt` if you don't specify a path

## Examples

### Create a File (Default Name)

```zephyr
file # FILE:;  § Creates "unnamed_file.txt"
```

### Create a File (Specific Path)

```zephyr
myfile # FILE:./data.txt;      § Relative path
datafile # FILE:/tmp/output.txt;  § Absolute path
```

## Changing File Path

You can change which file you're working with using `? w:`:

```zephyr
file # FILE:./first.txt;

file ? w:./second.txt;  § Now working with different file
```

## File Operations

### Write Content to a File

Use `? cSET:` to set the file's content:

```zephyr
file # FILE:./message.txt;
file ? cSET:"Hello, World!";  § Write text to file
```

### Clear File Content

Use `? cFLUSH:` to delete all content (empties the file):

```zephyr
file # FILE:./data.txt;
file ? cFLUSH:;  § Empty the file
```

### Rename a File

Use `? gRENAME:` to change the file name:

```zephyr
file # FILE:./old_name.txt;
file ? gRENAME:new_name.txt;  § File is now new_name.txt
```

### Delete a File

Use `? gDEL:` to delete the file completely:

```zephyr
file # FILE:./temp.txt;
file ? gDEL:;  § File is deleted
```

## Practical File Examples

### Example 1: Save Program Output

```zephyr
output_file # FILE:./output.txt;

log_entry # PT:"Program started at ";
log_entry ? w:++|"2024-01-15";

output_file ? cSET:'log_entry';
```

### Example 2: Accumulate Data

```zephyr
data_file # FILE:./data.txt;

§ Write initial content
data_file ? cSET:"Data Log";

§ Add more content (note: cSET replaces all content)
current_data # PT:"Data Log\nEntry 1: Test\nEntry 2: Success";
data_file ? cSET:'current_data';
```

### Example 3: Save User Input

```zephyr
name # PT:"";
name ? INPUT:"Enter your name: ";

database # FILE:./users.txt;
database ? cSET:'name';  § Save the name to file
```

### Example 4: Logging with Timestamps

```zephyr
log_file # FILE:./program.log;

message # PT:"[LOG] Event occurred";
log_file ? cSET:'message';

§ Later, rename for archiving
log_file ? gRENAME:program.log.backup;
```

## Working with File Paths

### Relative Paths

Relative paths are relative to where you run the program:

```zephyr
file # FILE:./data.txt;         § Current directory
file # FILE:../data.txt;        § Parent directory
file # FILE:./subfolder/data.txt;  § Subfolder
```

### Absolute Paths

Absolute paths start from the root:

```zephyr
file # FILE:/home/user/data.txt;    § Linux/Mac
file # FILE:C:\Users\data.txt;      § Windows
```

## File Value

The value of a File object is the path it points to:

```zephyr
file # FILE:./myfile.txt;
file ? push:;  § Output: ./myfile.txt (or the full path)
```

## Important Notes

### File Path Cannot Be Changed After Creation

Unlike other variables, you can create a new File object to work with a different file:

```zephyr
file1 # FILE:./first.txt;
file1 ? cSET:"First file";

§ Cannot change file1's path
file1 ? w:./second.txt;  § This changes which file is being worked on
```

### cSET Replaces Content

`cSET` replaces all file content. It doesn't append:

```zephyr
file # FILE:./data.txt;
file ? cSET:"Line 1";
file ? cSET:"Line 2";  § File now contains only "Line 2"
```

### File Operations Need Real Paths

Your file paths must be actual locations on your system:

```zephyr
file # FILE:./test.txt;     § Valid - creates in current directory
file ? cSET:"Hello";
```

## File Management Best Practices

1. **Use clear file names** - Name files based on content: `data.txt`, `log.txt`
2. **Organize in folders** - Use subfolders to organize files
3. **Check file operations** - Ensure paths exist before writing
4. **Use absolute paths for important data** - More reliable than relative
5. **Clean up temporary files** - Delete temp files when done

## Common File Patterns

### Pattern 1: Simple Data Storage

```zephyr
data_file # FILE:./saved_data.txt;

user_data # PT:"User: Alice, Score: 100";
data_file ? cSET:'user_data';
```

### Pattern 2: Logging

```zephyr
log_file # FILE:./application.log;

status # PT:"Status: Running";
log_file ? cSET:'status';
```

### Pattern 3: File Rotation

```zephyr
current_log # FILE:./current.log;
current_log ? cSET:"Log entry 1";

§ Rotate/archive the old log
current_log ? gRENAME:old.log;

§ Create new log
new_log # FILE:./current.log;
new_log ? cSET:"Log entry 1 (new)";
```

### Pattern 4: Backup

```zephyr
original # FILE:./important.txt;
original ? cSET:"Important data";

backup # FILE:./important.txt.backup;
backup ? cSET:"Important data";
```

## Tips for Working with Files

1. **Remember cSET replaces everything** - Don't use it if you want to append
2. **Use meaningful file names** - Makes programs easier to understand
3. **Think about file locations** - Will relative paths work when you move files?
4. **Test your file operations** - Make sure files are created where expected
5. **Clean up old files** - Use gDEL to remove temporary files

## Summary

| Task | Example |
|------|---------|
| Create file | `file # FILE:./data.txt;` |
| Set content | `file ? cSET:"Hello";` |
| Clear content | `file ? cFLUSH:;` |
| Rename file | `file ? gRENAME:newname.txt;` |
| Delete file | `file ? gDEL:;` |
| Change path | `file ? w:./other.txt;` |
| Get file path | `file ? push:;` |

## Next Steps

- Combine file operations with [LOOPs](04-LOOP.md) to write multiple entries
- Use with [Simple Variables](01-simpleVariable.md) to save data
- Try file operations with [User Input](01-simpleVariable.md) to save entered data
