import ast
from pathlib import Path

def extractErrors(filepath, class_name, method_name, var_name) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=filepath)

    # Extract Class
    class_node = next(
        (n for n in ast.walk(tree)
         if isinstance(n, ast.ClassDef) and n.name == class_name),
        None
    )
    if class_node is None:
        return ""

    # Extract function
    method_node = next(
        (n for n in class_node.body
         if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == method_name),
        None
    )
    if method_node is None:
        return ""

    # Extract variable
    for node in ast.walk(method_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var_name:
                    try:
                        return ast.literal_eval(node.value)
                    except ValueError:
                        # value isn't a simple literal (e.g. a function call or expression)
                        var = ast.get_source_segment(source, node.value)
                        if var:
                            return var
                            
        elif isinstance(node, ast.AnnAssign):  # handles `x: int = 5`
            if isinstance(node.target, ast.Name) and node.target.id == var_name:
                if node.value:
                    try:
                            return ast.literal_eval(node.value)
                    except ValueError:
                            var = ast.get_source_segment(source, node.value)
                            if var:
                                return var
    return ""

def splitRawErrors(errors: str):
    tree = ast.parse(errors, mode="eval")
    dict_node = tree.body
    
    def unwrap(node):
        if isinstance(node, ast.Constant):
            return node.value              # plain string literal -> real string, no quotes
        if isinstance(node, ast.JoinedStr):
            return ast.unparse(node)[2:-1] # f"...": drop leading f" and trailing "
        return ast.unparse(node)           # fallback, just in case
    
    entries = []
    for key_node, value_node in zip(dict_node.keys, dict_node.values):  # pyright: ignore[reportAttributeAccessIssue]
        key = ast.literal_eval(key_node)
        elts = value_node.body.elts[:-2]           # drop length-expr and SyntaxError
        values = [unwrap(e) for e in elts]
        entries.append((key, *values))
    
    return entries


def generateEntry(error: tuple):
    entry = f"| {error[0]} | {error[2]} | {error[1]} |\n"
    return entry

def main():
    errors = extractErrors("src/functions.py", "ZError", "process", "errors")
    errors = splitRawErrors(errors)

    errorsFile = Path("./docs/Errors.md")

    headers = ["# Errors\n\n## Error Codes\n\n\n| Code | Name | Description |\n|------|------|-------------|\n"]
    entries = []

    for error in errors:
        entry = generateEntry(error)
        entries.append(entry)

    with errorsFile.open("w") as f:
        f.writelines(headers)
        f.writelines(entries)

    



if __name__ == "__main__":
    main()
