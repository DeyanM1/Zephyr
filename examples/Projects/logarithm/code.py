def log(base: int, y: int, epsilon: float = 1e-10):
    x = 1.0
    fx = base**x - y
    fpx = (base**x) * 0.69314718056
    x_new = x - fx / fpx

    while (x_new - x) * (x_new - x) >= epsilon * epsilon:
        x = x_new
        fx = base**x-y
        fpx = (base**x) * 0.69314718056
        x_new = x - fx / fpx

    return x_new
print(log(2, 8))  # Output: 3
