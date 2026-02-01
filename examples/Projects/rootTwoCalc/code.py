# Number of digits you want
digits = 10

# Scale up 2 by 10^(2*digits) to preserve precision
n = 2 * 10**(2*digits)

# Initial guess
x = 10**digits

while digits != 0:
    x = (x + n // x) // 2
    digits -= 1

# Insert decimal point
s = str(x)
sqrt2 = s[0] + '.' + s[1:]
print(sqrt2)