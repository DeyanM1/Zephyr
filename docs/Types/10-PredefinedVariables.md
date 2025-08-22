# Predefined Variables

Predefined variables allow you to define variables in a json script and use them in Zephyr.

**Load Predefined Variables:**

```zephyr
__ ? predefVars:<filename>;
```

**Predefined Variable File Structure:**

The file extension is .zpkg
```json
{
    "<Variable Name>": {
        "type": "<Variable Type>",
        "value": "<Variable Value>",
        "const": false
    }
}
```
- Place predefined variable files in the `lib/` directory.

!Without Extension!
**Dump Variables used in code**
```zephyr
__ ? dumpVars:<filename>;
```

**Example:**

```zephyr
__ ? predefVars:examplePredefVars;
__ ? dumpVars:usedVars;
```
