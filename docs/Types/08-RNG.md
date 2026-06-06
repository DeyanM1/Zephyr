# Random Number Generator

An RNG (Random Number Generator) object generates a random number within a specified range. RNG objects are useful for simulations, random decisions, and game logic.

---


## Properties

- **`convertibleInto`** -> `PT`, `INT`, `FLOAT`, `BOOL`
- **`convertValue`** -> Random Number generated


## Methods

### Define
Creates a new RNG object with a specified range and output type.

```zephyr
rng # RNG:<*RangeMin>|<*RangeMax>|<*NumberType>;
dice # RNG:1|6|INT;
```

- **`RangeMin`** — Minimum value (inclusive)
- **`RangeMax`** — Maximum value (inclusive)
- **`NumberType`** — Type of random number: `INT` or `FLOAT`

### Write (w)
Changes the range and optionally the number type.

```zephyr
rng ? w:<*RangeMin>|<*RangeMax>|<*- NumberType>;
dice ? w:1|20|INT;
```



## Notes

- The `NumberType` parameter specifies whether the random number is an `INT` (integer) or `FLOAT` (floating point).
- The range is inclusive of both minimum and maximum values.
- Each access to the RNG generates a new random number within the specified range.
