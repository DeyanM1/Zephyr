# Developing Libraries

## Blank Library

Every library needs an `importHandler` that correctly imports the required classes (e.g. `ZCommand`) from `base.py`. If you instead import directly with `from base import <name>`, it will **not** work when the library is loaded through the zlm installer. A direct import can still be used temporarily for type validation while debugging, but must be commented out (or removed) before shipping the library.

The library's main class must extend `Base` (also imported via the `importHandler`).

It must also define a `load()` function returning a `dict[str, type]`, e.g.:

```python
{"myFunc": MyModule}
```

The key is an optional alternative name for the type and **must not contain spaces**. If left as an empty string (`""`), the class name (`MyModule`) is used instead.

### `__init__`

The main class's `__init__` must accept `self, cmd, activeVars`, and must call `self.registerFunc({...})`.

`registerFunc` takes a dict mapping function names to callables, e.g.:

```python
{"funcName": callable}
```

If a key is left as an empty string, the name of the class is used as the function name instead.

### Blank template

```python
from __future__ import annotations
#from base import ZCommand, ActiveVars, Base    # <- for debugging only. Use importHandler for the final project!

def importHandler(names: list[str]):
    import importlib.util
    from pathlib import Path
    import sys
    base_path = Path(__file__).resolve().parent / "base.py"
    moduleName = base_path.stem
    spec = importlib.util.spec_from_file_location(moduleName, base_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create spec for {base_path}")
    base = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = base
    spec.loader.exec_module(base)
    for name in names:
        globals()[name] = getattr(base, name)

importHandler(["ZCommand", "ActiveVars", "base"])

class Blank(Base):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.registerFunc({})

def load() -> dict[str, type]:
    return {"": Blank}
```
