# System Library

The System library provides access to system-level operations like checking the current directory and exiting with specific codes. These commands help manage how your Zephyr program interacts with the operating system.

## Importing System Library

First, import the System library:

```zephyr
__ ? LIB:./lib/system.py;
```

## Creating a System Object

After importing, create a System object:

```zephyr
system # system:;
```

No additional arguments are needed. The variable is immutable (cannot be changed).

## System Operations

### Getting Current Working Directory

Use `? getCWD:` to get the current working directory (folder where the program runs):

```zephyr
system ? getCWD:<*variableNameToSaveTo>;
```

The directory path is saved to the specified variable.

### Example: Get Current Directory

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

current_dir # PT:"";
system ? getCWD:current_dir;

current_dir ? push:;  § Output: The current working directory
```

### Exiting the Program

Use `? exit:` to stop the program with an exit code:

```zephyr
system ? exit:<*- ErrorCode>;
```

- **ErrorCode**: Optional exit code (0 = success, others = error)
- Default: 0 (success)

### Example: Normal Exit

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

message # PT:"Program complete!";
message ? push:;

system ? exit:0;  § Exit successfully
```

### Example: Error Exit

```zephyr
error_code # INT:1;
system ? exit:'error_code';  § Exit with error code 1
```

## Practical System Examples

### Example 1: Display Current Directory

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

cwd # PT:"";
system ? getCWD:cwd;

message # PT:"Working directory: ";
message ? w:++|'cwd';
message ? push:;
```

### Example 2: Exit on Error

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

value # INT:0;
value ? INPUT:"Enter a positive number: ";

is_valid # CO:('value' > 0);

check # IF:is_valid;
check ? START:2;
value ? push:;
value ? w:"is a valid number";
check ? ELSE:1;
system ? exit:1;  § Exit with error
check ? END:;
```

### Example 3: Directory-Aware File Operations

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

cwd # PT:"";
system ? getCWD:cwd;

file_path # PT:'cwd';
file_path ? w:++|"/output.txt";

output_file # FILE:'file_path';
output_file ? cSET:"Program ran in: ";
output_file ? w:++|'cwd';

status # PT:"File saved to: ";
status ? w:++|'file_path';
status ? push:;
```

### Example 4: Exit Codes for Scripts

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

result # INT:0;
result ? INPUT:"Enter 1 for success, 0 for failure: ";

is_success # CO:('result' == 1);

check # IF:is_success;
check ? START:1;
system ? exit:0;  § Success exit
check ? ELSE:1;
system ? exit:1;  § Error exit
check ? END:;
```

### Example 5: Conditional Exit

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

counter # INT:0;

loop # LOOP:~1;  § Infinite loop (controlled by exit)
loop ? START:3;

counter ? w:++;
counter ? push:;

is_done # CO:('counter' == 5);

check # IF:is_done;
check ? START:1;
system ? exit:0;  § Exit when done
check ? ELSE:0;
check ? END:;

loop ? END:;
```

## Understanding Exit Codes

Exit codes are numbers that indicate success or failure:

| Code | Meaning | Use |
|------|---------|-----|
| 0 | Success | Program completed successfully |
| 1 | General error | Unspecified error occurred |
| 2 | Misuse | Command misused |
| 127 | Not found | File not found |
| 128+ | Signal | Killed by signal |

### Using Exit Codes in Scripts

Exit codes allow other programs to know if your program succeeded:

```bash
§ Run Zephyr program
python src/zcli.py program.zph

§ Check exit code in bash
echo $?  § Displays the exit code
```

## Practical Scenarios

### Scenario 1: Validation Program

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

input_value # INT:0;
input_value ? INPUT:"Enter a number: ";

valid # CO:('input_value' > 0);

if_valid # IF:valid;
if_valid ? START:1;
system ? exit:0;  § Success - valid input
if_valid ? ELSE:1;
system ? exit:1;  § Error - invalid input
if_valid ? END:;
```

### Scenario 2: Processing Pipeline

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

cwd # PT:"";
system ? getCWD:cwd;

message # PT:"Processing in: ";
message ? w:++|'cwd';
message ? push:;

§ Do some work...

message ? w:"Complete!";
message ? push:;

system ? exit:0;
```

### Scenario 3: Multi-Program Workflow

```zephyr
§ Program 1: process_data.zph
__ ? LIB:./lib/system.py;
system # system:;

data # PT:"processed successfully";

output_file # FILE:./result.txt;
output_file ? cSET:'data';

system ? exit:0;  § Signal success
```

Then in a shell script, you could call multiple programs:

```bash
python src/zcli.py process_data.zph
if [ $? -eq 0 ]; then
    python src/zcli.py analyze_results.zph
else
    echo "Processing failed"
    exit 1
fi
```

## Common Use Cases

### Use Case 1: Error Handling

```zephyr
file_exists # BOOL:~0;  § Check if file exists

if_exists # IF:file_exists;
if_exists ? START:1;
if_exists ? w:~1;  § File found
if_exists ? ELSE:1;
system ? exit:1;  § Exit with error
if_exists ? END:;
```

### Use Case 2: Status Reporting

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

cwd # PT:"";
system ? getCWD:cwd;

status # PT:"Running in: ";
status ? w:++|'cwd';
status ? push:;
```

### Use Case 3: Clean Exit

```zephyr
__ ? LIB:./lib/system.py;
system # system:;

cleanup # PT:"Cleaning up...";
cleanup ? push:;

system ? exit:0;
```

## Tips for Using System

1. **Use exit codes** - Return 0 for success, non-zero for errors
2. **Document your codes** - Document what each code means
3. **Get working directory early** - Use getCWD before file operations
4. **Plan exit strategy** - Know when your program should end
5. **Test exit codes** - Verify they're correct for your OS

## Summary

| Task | Example |
|------|---------|
| Import system | `__ ? LIB:./lib/system.py;` |
| Create system | `system # system:;` |
| Get directory | `system ? getCWD:dir_var;` |
| Exit success | `system ? exit:0;` |
| Exit error | `system ? exit:1;` |

## Common Mistakes

### Mistake 1: Exiting in Wrong Place

```zephyr
§ WRONG: Exits before doing work
system ? exit:0;

message # PT:"This never prints";
message ? push:;
```

**Fix**: Place exit at the end

```zephyr
message ? push:;
system ? exit:0;  § After work
```

### Mistake 2: Wrong Variable Type for getCWD

```zephyr
§ WRONG: Using INT for directory path
cwd # INT:0;
system ? getCWD:cwd;  § ERROR! Should be PT
```

**Fix**: Use PT for directory

```zephyr
cwd # PT:"";
system ? getCWD:cwd;
```

## Troubleshooting

### Program Exits Unexpectedly

1. Check if `system ? exit:` was called
2. Look for error conditions that trigger exit
3. Add print statements to track execution
4. Verify exit codes in script output

### Can't Get Working Directory

1. Make sure System library is imported
2. Verify variable name is correct
3. Use PT type for directory variable
4. Try printing the variable to verify

## Next Steps

- Combine with [File Management](../Types/09-FileManagement.md)
- Use with [Python Library](02-Python.md)
- Try in shell scripts for program workflows
