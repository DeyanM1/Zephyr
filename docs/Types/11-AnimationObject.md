# Animation Object

An Animation Object renders animated frames inside the terminal. It supports frame management, timing control, and playback operations to create sequential animations.

---

## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`
- **`convertValue`** -> Current animation position

## Methods

### Define
Creates a new Animation Object with optional initial settings.

```zephyr
ao # AO:<*- initialFrame>|<*- delayInSeconds>|<*- clearScreen>;
animation # AO:"Frame1"|2|~1;
```

- **`InitialFrame`** — (Optional) Initial frame as `PT` or type that can convert into `PT`
- **`DelayInSeconds`** — (Optional) Delay between frames in seconds
- **`ClearScreen`** — (Optional) Whether to clear screen after each frame: `~0` (false) or `~1` (true)


### Write (w)
Adds a new frame to the animation. Accepts any type that can convert to `PT`.

```zephyr
ao ? w:<*FrameToAdd>;
animation ? w:"Frame2";
```

### WriteList (wLIST)
adds a new Frame to the animation. accepts the name of a `LIST`

```zephyr
ao ? wLIST:<* ListVarName>;
animation ? w:myList;
```

### Set Delay (setDelay)
Updates the delay between animation frames. Accepts an integer representing seconds.

```zephyr
ao ? setDelay:<*seconds>;
animation ? setDelay:1;
```

### Clear Screen (clearScreen)
Enables or disables screen clearing between frames. Accepts `~1` (true) or `~0` (false).

```zephyr
ao ? clearScreen:<*bool>;
animation ? clearScreen:~1;
```

### Set Index (setIndex)
Jumps to a specific frame by index and displays it. Accepts an integer.

```zephyr
ao ? setIndex:<*index>; 
animation ? setIndex:3;
```

### Start
Begins playing the animation from the current index. After completion, restarts from index 0.

```zephyr
animation ? start:;
```

### Step
Advances to the next frame and displays it without starting automatic playback.

```zephyr
animation ? step:;
```

### Display
Shows the current frame without changing the index.

```zephyr
animation ? display:;
```

### Reset
Resets the index to 0 without displaying any frames.

```zephyr
animation ? reset:;
```


## Notes

- The animation index starts at 0 for the first frame.
- Delay is specified in seconds.
- Screen clearing applies after each frame is displayed during playback.
- The `start` method plays through all frames and then restarts from frame 0.
- Frames can be strings (`PT` type) or list elements converted to text.
