a = 1
b = 1
n = 0
limit = 30

while n < limit:
    temp = b
    b = a + b
    a = temp
    n += 1

phi = b / a
print(phi)
