import sys


def build_bracket_map(code_dict):
    """Build a map of bracket positions for O(1) jumps"""
    bracket_map = {}
    stack = {}  # Dict to track bracket depths
    depth = 0
    
    for ip in sorted(code_dict.keys()):
        char = code_dict[ip]
        if char == "[":
            stack[depth] = ip
            depth += 1
        elif char == "]":
            depth -= 1
            opening = stack.pop(depth)
            bracket_map[ip] = opening
            bracket_map[opening] = ip
    
    return bracket_map


def execute(code_str):
    """Execute Brainfuck code - all dicts, no lists"""
    # Convert code to dict: {index: command}
    code_dict = {}
    idx = 0
    for char in code_str:
        if char in "+-<>[].,":
            code_dict[idx] = char
            idx += 1
    
    # Setup - all dicts
    bracket_map = build_bracket_map(code_dict)
    cells = {}           # Memory tape as dict (sparse)
    ptr = 0              # Data pointer
    ip = 0               # Instruction pointer
    
    # Execute
    while ip in code_dict:
        cmd = code_dict[ip]
        
        if cmd == ">":
            ptr += 1
        elif cmd == "<":
            ptr -= 1
        elif cmd == "+":
            cells[ptr] = (cells.get(ptr, 0) + 1) % 256
        elif cmd == "-":
            cells[ptr] = (cells.get(ptr, 0) - 1) % 256
        elif cmd == ".":
            sys.stdout.write(chr(cells.get(ptr, 0)))
        elif cmd == ",":
            cells[ptr] = ord(sys.stdin.read(1))
        elif cmd == "[":
            if cells.get(ptr, 0) == 0:
                ip = bracket_map[ip]
        elif cmd == "]":
            if cells.get(ptr, 0) != 0:
                ip = bracket_map[ip]
        
        ip += 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            execute(f.read())
    else:
        execute(sys.stdin.read())