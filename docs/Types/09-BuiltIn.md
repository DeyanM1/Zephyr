# Built-in

Variable state cannot be changed. Always named `__`.

Built-in commands control program flow, timing, persistence, and library imports. They provide core functionality without requiring explicit definition.

* Wait:

```

__ ? wait:<*SecondsToWait>;

```

* Jump relative:

```

__ ? jump:<*RelativePositionInCode>;

```

* Jump absolute:

```

__ ? jumpTo:<*AbsolutePositionInCode>;

```

* Export variables:

```

__ ? export:<*ExportPath>;  ~ Defaults to `.zpkg` matching `.zph` filename

```

* Import variables:

```

__ ? load:<*ImportPath>;

```

* Import library:

```

__ ? LIB:<*LibFilePath>;

```