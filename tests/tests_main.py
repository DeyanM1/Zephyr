import importlib
import json
from typing import Any, Dict, Type, TypedDict


class class1:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def print(self):
        print(self.x)


class class2:
    def __init__(self, z) -> None:
        self.z = z


objects = {
    "a": class1(1, 2),
    "b": class2("x")
}

class SerializedObject(TypedDict):
    __class__: str
    __state__: Dict[str, Any]

def serialize_object(obj: Any) -> SerializedObject:
    cls: Type[Any] = obj.__class__
    return {
        "__class__": f"{cls.__module__}.{cls.__qualname__}",
        "__state__": obj.__dict__
    }
def serialize_dict(
    obj_dict: Dict[str, Any],
    path: str
) -> None:
    data: Dict[str, SerializedObject] = {
        key: serialize_object(value)
        for key, value in obj_dict.items()
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_class(path: str) -> Type[Any]:
    module_path: str
    class_name: str

    module_path, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

def deserialize_object(data: SerializedObject) -> Any:
    cls: Type[Any] = load_class(data["__class__"])
    obj: Any = cls.__new__(cls)
    obj.__dict__.update(data["__state__"])
    return obj

def deserialize_dict(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data: Dict[str, SerializedObject] = json.load(f)

    return {
        key: deserialize_object(value)
        for key, value in data.items()
    }


print(restored)
restored["a"].print()

