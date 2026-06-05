# GPIO Library

The GPIO (General Purpose Input/Output) library allows your Zephyr program to control hardware pins on devices like Raspberry Pi. This is useful for controlling LEDs, sensors, motors, and other electronic components.

## What is GPIO?

GPIO pins are physical connections on a microcontroller or single-board computer that can:
- **Output**: Send electrical signals (turn things on/off)
- **Input**: Receive electrical signals (read sensor values)

## Importing GPIO Library

First, import the GPIO library:

```zephyr
__ ? LIB:./lib/GPIO.py;
```

## Pinout Types

GPIO libraries support different pinout naming systems:

| Type | Description | Use Case |
|------|-------------|----------|
| `BCM` | Broadcom numbering | Official Raspberry Pi naming |
| `Board` | Board pin numbering | Physical pin positions on the board |

Choose based on your hardware documentation.

## Setting Up GPIO

### Create a GPIO Object

```zephyr
gpio # GPIO:<*PinoutType>;
```

Example - Using Broadcom numbering:

```zephyr
gpio # GPIO:BCM;
```

Example - Using board numbering:

```zephyr
gpio # GPIO:Board;
```

## Configuring Pins

### Setup a Pin

Define a pin as input or output:

```zephyr
gpio ? SETUP:<*PinNumber>|<*PinType>;
```

- **PinNumber**: The pin number (depends on pinout type)
- **PinType**: `IN` (input) or `OUT` (output)

### Examples

```zephyr
gpio # GPIO:BCM;

gpio ? SETUP:17|OUT;   § Pin 17 as output
gpio ? SETUP:27|IN;    § Pin 27 as input
```

## Writing to Output Pins

### Set Pin Value

Send a signal to an output pin:

```zephyr
gpio ? SET:<*PinNumber>|<*PinValue>;
```

- **PinNumber**: The pin to write to
- **PinValue**: `1` (HIGH) or `0` (LOW)

### Examples

```zephyr
gpio # GPIO:BCM;
gpio ? SETUP:17|OUT;

gpio ? SET:17|1;  § Turn pin 17 HIGH (on)
gpio ? SET:17|0;  § Turn pin 17 LOW (off)
```

## Reading from Input Pins

### Read Pin Value

Read the current state of an input pin:

```zephyr
gpio ? READ:<*PinNumber>;
```

The result is stored in the GPIO object's value.

### Example

```zephyr
gpio # GPIO:BCM;
gpio ? SETUP:27|IN;

gpio ? READ:27;  § Read the pin

value # INT:0;
value ? w:'gpio';  § Get the read value
value ? push:;     § Output: 1 or 0
```

## Cleaning Up

### Clean All Pins

Reset all pins when done:

```zephyr
gpio ? CLEAN:;
```

Always clean up to avoid leaving pins in undefined states.

## Practical GPIO Examples

### Example 1: Blink an LED

```zephyr
§ Setup
gpio # GPIO:BCM;
gpio ? SETUP:17|OUT;

§ Blink loop
counter # INT:1;
keep_going # CO:('counter' <= 10);

loop # LOOP:keep_going;
loop ? START:4;

gpio ? SET:17|1;       § LED on
__ ? wait:1;           § Wait 1 second

gpio ? SET:17|0;       § LED off
__ ? wait:1;           § Wait 1 second

counter ? w:++;

loop ? END:;

gpio ? CLEAN:;         § Clean up
```

### Example 2: Read a Button

```zephyr
gpio # GPIO:BCM;

gpio ? SETUP:27|IN;    § Button input
gpio ? SETUP:17|OUT;   § LED output

counter # INT:1;
keep_going # CO:('counter' <= 20);

loop # LOOP:keep_going;
loop ? START:2;

gpio ? READ:27;        § Read button state

button_pressed # CO:('gpio' == 1);

check # IF:button_pressed;
check ? START:1;
gpio ? SET:17|1;       § Turn LED on if button pressed
check ? ELSE:1;
gpio ? SET:17|0;       § Turn LED off otherwise
check ? END:;

counter ? w:++;

loop ? END:;

gpio ? CLEAN:;
```

### Example 3: Traffic Light

```zephyr
gpio # GPIO:BCM;

§ Setup pins
gpio ? SETUP:17|OUT;  § Red
gpio ? SETUP:27|OUT;  § Yellow
gpio ? SETUP:23|OUT;  § Green

§ Red light
gpio ? SET:17|1;
gpio ? SET:27|0;
gpio ? SET:23|0;

__ ? wait:3;

§ Yellow light
gpio ? SET:17|0;
gpio ? SET:27|1;
gpio ? SET:23|0;

__ ? wait:1;

§ Green light
gpio ? SET:17|0;
gpio ? SET:27|0;
gpio ? SET:23|1;

__ ? wait:3;

gpio ? CLEAN:;
```

### Example 4: Control Multiple LEDs with Pattern

```zephyr
gpio # GPIO:BCM;

led_pins # LIST:INT|17|27|23;

counter # INT:1;
keep_going # CO:('counter' <= 3);

loop # LOOP:keep_going;
loop ? START:3;

gpio ? SET:'led_pins<'counter'>''|1;  § Turn LED on
__ ? wait:1;

gpio ? SET:'led_pins<'counter'>''|0;  § Turn LED off

counter ? w:++;

loop ? END:;

gpio ? CLEAN:;
```

## Best Practices

1. **Always clean up** - Use `? CLEAN:;` at the end
2. **Verify pin numbers** - Wrong pin numbers cause errors
3. **Use comments** - Document which pins control what
4. **Check pinout type** - BCM vs Board numbering is important
5. **Test carefully** - Verify electrical connections before running

## Common Mistakes

### Mistake 1: Forgetting to Clean Up

```zephyr
§ WRONG: No cleanup
gpio # GPIO:BCM;
gpio ? SETUP:17|OUT;
gpio ? SET:17|1;
§ Program ends without cleanup - bad!
```

**Fix**: Always clean up

```zephyr
gpio ? CLEAN:;  § Add before program ends
```

### Mistake 2: Wrong Pin Numbers

```zephyr
§ WRONG: Pin number for Board mode vs BCM
gpio # GPIO:Board;
gpio ? SETUP:11|OUT;  § Physical pin 11
```

**Fix**: Use correct pinout type and numbers

### Mistake 3: Using Input Pin as Output

```zephyr
§ WRONG: Trying to write to input
gpio ? SETUP:27|IN;
gpio ? SET:27|1;  § ERROR! Can't write to input pin
```

**Fix**: Set correct pin type

```zephyr
gpio ? SETUP:27|OUT;  § Set as output first
gpio ? SET:27|1;
```

## Troubleshooting

### "Permission Denied" Error

GPIO access often requires special permissions. Run with `sudo`:

```bash
sudo python src/zcli.py program.zph
```

### Pins Not Responding

1. Check physical connections
2. Verify pin numbers match your hardware
3. Make sure SETUP was called first
4. Test with a simple program first

## Safety Considerations

- **Power levels**: Ensure signals match your hardware's requirements
- **Current limits**: Don't exceed pin current ratings
- **Voltage**: Most GPIO is 3.3V or 5V (check your device)
- **Static electricity**: Ground yourself before handling components

## Summary

| Task | Example |
|------|---------|
| Import GPIO | `__ ? LIB:./lib/GPIO.py;` |
| Create GPIO | `gpio # GPIO:BCM;` |
| Setup pin | `gpio ? SETUP:17\|OUT;` |
| Set HIGH | `gpio ? SET:17\|1;` |
| Set LOW | `gpio ? SET:17\|0;` |
| Read pin | `gpio ? READ:27;` |
| Cleanup | `gpio ? CLEAN:;` |

## Next Steps

- Learn [Python Library](02-Python.md) for more advanced control
- Try [System Library](03-system.md) for system operations
- Combine GPIO with [LOOPs](../Types/04-LOOP.md) for automated control
