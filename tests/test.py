a = "1.24"
b = "a"

print(str(float(a) + float(b)) if a.replace('.', '', 1).isdigit() and b.replace('.', '', 1).isdigit() else a + b)
