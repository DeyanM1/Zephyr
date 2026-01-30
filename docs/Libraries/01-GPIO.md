# GPIO

Value represents the status of the last read pin.

GPIO objects allow programs to interface with hardware pins for input and output. They support pin setup, reading, writing, and cleanup.

* Import GPIO library:

```

__ ? LIB:./lib/GPIO.py;

```

* Define GPIO setup:

```

gpio # GPIO:<*PinoutType>;   ~ PinoutType: BCM or Board

```

* Configure pin:

```

gpio ? SETUP:<*PinNum>|<*PinType>;   ~ PinType: IN or OUT

```

* Set pin value:

```

gpio ? SET:<*PinNum>|<*PinValue>;   ~ PinValue: 1 (HIGH) or 0 (LOW)

```

* Read pin value:

```

gpio ? READ:<*PinNum>;   ~ Requires pin set to IN

```

* Clean all pins:

```

gpio ? CLEAN:;

```
