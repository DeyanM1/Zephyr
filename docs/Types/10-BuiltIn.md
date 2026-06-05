# Built-in Commands

Built-in commands are special system operations accessed through the `__` variable (two underscores). These commands control program flow, timing, data persistence, and library imports.

## Important: Built-in Variable

The `__` variable is always available and cannot be redeclared. It provides access to all system-level operations.

## Program Timing

### Wait

Pause your program for a specified number of seconds:

```zephyr
__ ? wait:2;  § Wait 2 seconds
```

### Examples

```zephyr
message # PT:"Starting...";
message ? push:;

__ ? wait:3;  § Pause for 3 seconds

message ? w:"Done!";
message ? push:;
```

## Program Flow Control: Jumps

### Jump Relative

Jump forward or backward by a relative number of lines:

```zephyr
__ ? jump:5;  § Jump 5 lines forward
```

Positive numbers jump forward, negative numbers jump backward:

```zephyr
§ Line 1
msg # PT:"First";

§ Line 4
__ ? jump:3;  § Jump to line 7 (skip lines 5-6)

§ Line 6 (skipped)
msg ? w:"Skipped";

§ Line 8 (execution continues here)
msg ? w:"After jump";
```

### Jump Absolute

Jump to a specific line number in your program:

```zephyr
__ ? jumpTo:10;  § Go to line 10
```

### Important Notes About Jumps

- Jump is **not recommended for beginners** - Use IF and LOOP instead
- Use with caution - Can create spaghetti code
- Position counting starts from the beginning of the file
- Jumps out of bounds cause errors

## Data Persistence: Export and Import

### Export Variables

Save all current variables to a file:

```zephyr
__ ? export:./saved_state.zpkg;
```

Default filename (if no path specified):

```zephyr
__ ? export:;  § Creates file matching .zph filename with .zpkg extension
```

### Import Variables

Load previously saved variables from a file:

```zephyr
__ ? load:./saved_state.zpkg;
```

### Practical Example

```zephyr
§ Declare variables
score # INT:100;
name # PT:"Alice";

§ Save them
__ ? export:./game_state.zpkg;

§ Later, load them
__ ? load:./game_state.zpkg;

§ Variables are restored
score ? push:;  § Output: 100
name ? push:;   § Output: Alice
```

## Importing Libraries

### Import Library

Load external libraries (functions/features) into your program:

```zephyr
__ ? LIB:./lib/GPIO.py;
```

Libraries can be:
- **Local**: `./lib/GPIO.py` (in your project)
- **System**: `/path/to/lib/system.py`

### Common Libraries

```zephyr
§ GPIO - Hardware control
__ ? LIB:./lib/GPIO.py;

§ Python - Run Python code
__ ? LIB:./lib/python.py;

§ System - System operations
__ ? LIB:./lib/system.py;
```

## Complete Built-in Examples

### Example 1: Timed Greeting

```zephyr
__ ? wait:1;

hello # PT:"Welcome to Zephyr!";
hello ? push:;

__ ? wait:2;

hello ? w:"This program waited 2 seconds...";
hello ? push:;

__ ? wait:1;
```

### Example 2: Save Game State

```zephyr
§ Play the game and accumulate state
level # INT:5;
score # INT:1500;
items # PT:"Sword,Shield";

§ Save progress
__ ? export:./my_game_progress.zpkg;

progress # PT:"Game saved!";
progress ? push:;
```

### Example 3: Load and Continue

```zephyr
§ Load previous state
__ ? load:./my_game_progress.zpkg;

level ? push:;    § Outputs saved level
score ? push:;    § Outputs saved score
items ? push:;    § Outputs saved items

§ Continue playing...
```

### Example 4: Using Libraries

```zephyr
§ Import GPIO library
__ ? LIB:./lib/GPIO.py;

§ Now can use GPIO functions (see GPIO documentation)
gpio # GPIO:BCM;
gpio ? SETUP:17|OUT;
```

## Practical Scenarios

### Scenario 1: Progress Tracking

```zephyr
progress # INT:0;
progress ? INPUT:"Enter progress percentage: ";

message # PT:"Progress: ";
message ? w:++|'progress';
message ? w:++|"%";
message ? push:;

__ ? export:./progress.zpkg;
```

### Scenario 2: Delayed Execution

```zephyr
instructions # PT:"Processing...";
instructions ? push:;

__ ? wait:3;

instructions ? w:"Processing complete!";
instructions ? push:;
```

### Scenario 3: Game Session

```zephyr
game_active # BOOL:~1;

loop # LOOP:game_active;
loop ? START:3;

play_turn # PT:"";
play_turn ? INPUT:"Enter your move: ";

score # INT:0;
score ? w:++|10;

game_active ? w:--;  § Decrement to check exit condition

loop ? END:;

__ ? export:./final_score.zpkg;
```

## Built-in Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `wait` | Pause program | `__ ? wait:2;` |
| `jump` | Jump relative lines | `__ ? jump:5;` |
| `jumpTo` | Jump to line | `__ ? jumpTo:10;` |
| `export` | Save variables | `__ ? export:./save.zpkg;` |
| `load` | Load variables | `__ ? load:./save.zpkg;` |
| `LIB` | Import library | `__ ? LIB:./lib/GPIO.py;` |

## Tips for Built-in Commands

1. **Use wait sparingly** - Slows down your program
2. **Export before important operations** - Save state before risky code
3. **Load at program start** - Load saved state early
4. **Avoid jumps if possible** - Use IF and LOOP instead
5. **Import libraries early** - Load libraries before using them

## Common Mistakes

### Mistake 1: Jump Out of Bounds

```zephyr
§ WRONG: Jumping beyond program end
__ ? jumpTo:1000;  § Program only has 50 lines - ERROR!
```

### Mistake 2: Forgetting Library Extension

```zephyr
§ WRONG: Missing extension
__ ? LIB:GPIO;  § ERROR! Should be GPIO.py

§ CORRECT:
__ ? LIB:GPIO.py;
```

### Mistake 3: Loading Non-Existent File

```zephyr
§ WRONG: File doesn't exist
__ ? load:./missing_file.zpkg;  § ERROR!
```

## Next Steps

- Learn more about [File Management](09-FileManagement.md)
- Explore [Libraries](../Libraries/00-ZLM.md)
- Check out specific libraries like [GPIO](../Libraries/01-GPIO.md)
