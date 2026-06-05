# Animation Objects

Animation Objects allow you to display animated frames in the terminal. You can create sequences of text frames and display them with timing and effects.

## Understanding Animation Objects

An Animation Object is like a slideshow for the terminal:
- Store multiple frames (text screens)
- Display them in sequence
- Control timing between frames
- Optionally clear the screen between frames

## Creating an Animation Object

```zephyr
<VariableName> # AO:<*- initialFrame>|<*- delayInSeconds>|<*- clearScreen>;
```

- **initialFrame**: Starting frame(s) - can be a single PT value or a LIST of PT values
- **delayInSeconds**: Delay between frames (INT)
- **clearScreen**: Should the screen clear between frames? (~1 for yes, ~0 for no)

## Basic Example

```zephyr
animation # AO:"Frame 1"|1|~1;
```

- Initial frame: "Frame 1"
- Delay: 1 second between frames
- Clear screen: Yes (~1)

## Animation Operations

### Add a Frame

Use `? w:` to add frames to the animation:

```zephyr
animation # AO:"Start"|1|~1;

animation ? w:"Frame 2";
animation ? w:"Frame 3";
animation ? w:"The End";
```

### Set Delay Between Frames

Use `? setDelay:` to change the timing:

```zephyr
animation # AO:"First"|2|~1;

animation ? setDelay:1;  § Change to 1 second delay
```

### Set Clear Screen

Use `? clearScreen:` to control screen clearing:

```zephyr
animation # AO:"Frame"|1|~0;  § No clearing

animation ? clearScreen:~1;  § Enable clearing
```

### Set Current Index

Jump to a specific frame:

```zephyr
animation # AO:"Frame 1"|1|~1;
animation ? w:"Frame 2";
animation ? w:"Frame 3";

animation ? setIndex:2;  § Jump to frame 2
```

### Display Current Frame

Show the current frame without advancing:

```zephyr
animation ? display:;
```

### Step Forward

Advance to the next frame:

```zephyr
animation ? step:;
```

### Start Animation

Play the animation automatically:

```zephyr
animation ? start:;
```

### Reset Index

Go back to frame 1:

```zephyr
animation ? reset:;
```

## Practical Animation Examples

### Example 1: Simple Loading Animation

```zephyr
loader # AO:"|"|1|~0;

loader ? w:"|/";
loader ? w:"|−";
loader ? w:|"\";

loader ? start:;  § Play the animation
```

### Example 2: Story Scene

```zephyr
story # AO:"Once upon a time..."|2|~1;

story ? w:"In a land far away...";
story ? w:"There was a hero...";
story ? w:"Who saved the kingdom!";
story ? w:"The End.";

story ? start:;  § Display the story
```

### Example 3: Progress Indicator

```zephyr
progress # AO:"[    ]"|1|~0;

progress ? w:"[=   ]";
progress ? w:"[==  ]";
progress ? w:"[=== ]";
progress ? w:"[====]";
progress ? w:"Complete!";

progress ? start:;
```

### Example 4: Blinking Text

```zephyr
message # PT:"IMPORTANT";
blink # AO:'message'|1|~1;

blink ? w:"";
blink ? w:'message';
blink ? w:"";

blink ? start:;  § Blinks between message and blank
```

### Example 5: Frame-by-Frame Display

```zephyr
slides # AO:"Slide 1"|0|~1;

slides ? w:"Slide 2";
slides ? w:"Slide 3";

slides ? display:;  § Show slide 1
__ ? wait:2;        § Wait 2 seconds

slides ? step:;     § Move to slide 2
slides ? display:;
__ ? wait:2;

slides ? step:;     § Move to slide 3
slides ? display:;
```

## Creating Animations with Lists

You can create animations using a list of frames:

```zephyr
frames # LIST:PT:"Welcome"|"Loading..."|"Done!";

animation # AO:'frames'|1|~1;
animation ? start:;
```

## Practical Scenarios

### Scenario 1: Game Over Screen

```zephyr
game_over # AO:"GAME OVER"|1|~1;

game_over ? w:"Final Score: 1000";
game_over ? w:"Press Enter to continue";

game_over ? start:;
```

### Scenario 2: Processing Steps

```zephyr
process # AO:"Initializing..."|1|~1;

process ? w:"Loading data...";
process ? w:"Processing...";
process ? w:"Saving results...";
process ? w:"Done!";

process ? start:;
```

### Scenario 3: Error Animation

```zephyr
error # AO:"ERROR!"|0|~1;

error ? w:"";  § Blink effect

error_loop # LOOP:~1;  § Infinite loop (change to ~0 to exit)
error_loop ? START:1;
error_loop ? END:;
```

### Scenario 4: Title Screen

```zephyr
title # AO:"========"|1|~1;

title ? w:"  GAME  ";
title ? w:"========";
title ? w:"";
title ? w:"Press Start";

title ? start:;
```

## Animation Control

### Manual Control (Step by Step)

```zephyr
animation # AO:"Frame 1"|0|~1;
animation ? w:"Frame 2";
animation ? w:"Frame 3";

animation ? display:;  § Show Frame 1
__ ? wait:1;

animation ? step:;     § Move to Frame 2
animation ? display:;
__ ? wait:1;

animation ? step:;     § Move to Frame 3
animation ? display:;
```

### Automatic Playback

```zephyr
animation # AO:"Frame 1"|1|~1;
animation ? w:"Frame 2";
animation ? w:"Frame 3";

animation ? start:;  § Auto-plays with 1 second delay
```

## Tips for Animations

1. **Set realistic delays** - Too fast is unreadable, too slow is boring
2. **Use ~1 for clearScreen** - Better for visual effects
3. **Keep frames readable** - Terminal width and height matter
4. **Test different delays** - Find what looks good
5. **Use with `wait`** - Add pauses between animations

## Common Animation Patterns

### Pattern 1: Pulse Effect

```zephyr
pulse # AO:"*"|1|~1;
pulse ? w:"* *";
pulse ? w:"* * *";

pulse ? start:;
```

### Pattern 2: Countdown

```zephyr
countdown # AO:"3"|1|~1;
countdown ? w:"2";
countdown ? w:"1";
countdown ? w:"GO!";

countdown ? start:;
```

### Pattern 3: Typewriter Effect

```zephyr
text1 # PT:"H";
text2 # PT:"He";
text3 # PT:"Hel";
text4 # PT:"Hell";
text5 # PT:"Hello";

typewriter # AO:'text1'|0|~1;
typewriter ? w:'text2';
typewriter ? w:'text3';
typewriter ? w:'text4';
typewriter ? w:'text5';

typewriter ? start:;
```

## Animation Limitations

- Terminal width/height affects display
- Very fast animations may appear as flicker
- Complex ASCII art may not render correctly
- All frames should be strings (PT or convertible to PT)

## Summary

| Task | Example |
|------|---------|
| Create animation | `ao # AO:"Frame1"\|1\|~1;` |
| Add frame | `ao ? w:"Frame2";` |
| Set delay | `ao ? setDelay:2;` |
| Clear screen | `ao ? clearScreen:~1;` |
| Jump to frame | `ao ? setIndex:3;` |
| Display frame | `ao ? display:;` |
| Next frame | `ao ? step:;` |
| Auto-play | `ao ? start:;` |
| Reset | `ao ? reset:;` |

## Next Steps

- Combine animations with [LOOPs](04-LOOP.md)
- Add interactivity with [Simple Variables](01-simpleVariable.md) for user input
- Use with [Built-in](10-BuiltIn.md) timing functions (`wait`)
