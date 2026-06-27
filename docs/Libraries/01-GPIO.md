# GPIO

The GPIO (General Purpose Input/Output) library allows Zephyr programs to interface with hardware pins. It supports pin configuration, reading input signals, writing output signals, and cleanup operations. The variable's value represents the status of the last read pin.

---

## Properties

- **`convertibleInto`** -> `PT`, `FLOAT`, `INT`, `BOOL`
- **`convertValue`** -> State of last read Pin

## Setup

Before using GPIO, import the library:

```zephyr
__ ? LIB:"GPIO.py";
```

## Methods

### Define
Creates a GPIO interface with the specified pinout type.

```zephyr
gpio # GPIO:<*PinoutType>; 
gpio # GPIO:BCM;
```

- **`PinoutType`** — Pin numbering scheme: `BCM` or `Board`

### Write (w)
change the Pinout Type

```zephyr
gpio ? w:<*PinoutType>;
gpio ? w:Board;
```

- **`PinoutType`** — Pin numbering scheme: `BCM` or `Board`

### Setup Pin (SETUP)
Configures a pin for input or output.

```zephyr
gpio ? SETUP:<*PinNum>|<*PinType>;
gpio ? SETUP:17|OUT;
```

**PinType options:**
- `IN` — Input mode
- `OUT` — Output mode

### Set Pin Value (SET)
Writes a digital value to an output pin.

```zephyr
gpio ? SET:<*PinNum>|<*PinValue>;
gpio ? SET:17|1;
```

**PinValue options:**
- `1` — HIGH (logic 1)
- `0` — LOW (logic 0)

### Read Pin Value (READ)
Reads the digital value from an input pin. The result is stored in the GPIO variable's value field.

```zephyr
gpio ? READ:<*PinNum>;
gpio ? READ:17;
```

The pin must be configured as `IN` before reading.

### Clean All Pins (CLEAN)
Resets and cleans up all pins, returning them to default state.

```zephyr
gpio ? CLEAN:;
```


## Notes

- Choose the correct pinout type (`BCM` or `Board`) based on your hardware documentation.
- Input pins must be configured with `SETUP` before calling `READ`.
- Output pins must be configured with `SETUP` before calling `SET`.
- Always call `CLEAN:` at the end of your program to properly release hardware resources.
- Pin numbers vary depending on the chosen pinout scheme.
