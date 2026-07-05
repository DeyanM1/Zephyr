import sys


def build_bracket_map(code_dict):
    bracket_map = {}
    stack = {}
    depth = 0
    ip = 0
    max_ip = max(code_dict.keys())
    
    while ip <= max_ip:
        char = code_dict.get(ip)
        if char == "[":
            stack[depth] = ip
            depth += 1
        elif char == "]":
            depth -= 1
            opening = stack.pop(depth)
            bracket_map[ip] = opening
            bracket_map[opening] = ip
        ip += 1
    
    return bracket_map




def execute(code_str):
    code_dict = {}
    idx = 0
    for char in code_str:
        if char in "+-<>[].,":
            code_dict[idx] = char
            idx += 1
    
    bracket_map = build_bracket_map(code_dict)
    cells = {}   
    ptr = 0       
    ip = 0       
    max_ip = max(code_dict.keys()) if code_dict else 0

    
    while ip <= max_ip:
        cmd = code_dict.get(ip)
        
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
    code = ">++++++++++>+>+[[+++++[>++++++++<-]>.<++++++[>--------<-]+<<<]>.>>[[-]<[>+<-]>>[<<+>+>-]<[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>[-]>+>+<<<-[>+<-]]]]]]]]]]]+>>>]<<<]"
    execute(code)
    