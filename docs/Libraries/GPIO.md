# GPIO-Library

- usage:
```zephyr
GPIO # LIB:GPIO; ~ import GPIO library
GPIO # INIT:<BoardMode>; ~ BCM or BOARD

GPIO ? SETUP:<PIN>|<Mode>; ~ IN or OUT

GPIO ? SET:<PIN>|<value>; ~ LOW or HIGH
```
- write to Pins:
```zephyr
GPIO # LIB:GPIO;
GPIO # INIT:BCM;

GPIO ? SETUP:4|OUT;
GPIO ? SET:4|HIGH;
```

- read from Pins:
```zephyr
output # INT:0;
GPIO # LIB:GPIO;
GPIO # INIT:BCM;

GPIO ? SETUP:4|IN;
GPIO ? READ:4|output
```
