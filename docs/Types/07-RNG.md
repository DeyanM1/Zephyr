# Random Number Generator

Supported types: `INT`, `PT`, `FLOAT`

RNG objects generate a random number within a specified range. They are useful for simulations, random decisions, or game logic.

* Define:

*`NumberType`* is the type of the result variable either *`INT`* or *`FLOAT`*

```

rng # RNG:<*RangeMin>|<*RangeMax>|<*NumberType>;

```

* change Range:

```

rng ? w:<*RangeMin>|<*RangeMax>|<*- NumberType>;

```