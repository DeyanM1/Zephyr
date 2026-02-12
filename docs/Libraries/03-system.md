# System

Using the system library you can control basic system behaviour.



* Import system library:

```

__ ? LIB:./lib/system.py;

```

* Define system:

```

python # system:; § No additional arguments needed

```

* Exit:
Exit quits the program with a given error code

```

system ? exit:<*- ErrorCode>    § Default ErrorCode is 0

```

* getCWD:
getCWD saves the current working directory to a pt variable

```

system ? getCWD:<* variableNameToSaveTo>;

```