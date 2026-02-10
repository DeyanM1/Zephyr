def prime_factors(number: int):
    factors: list[int] = []

    # Handle factor 2 separately
    while number % 2 == 0:
        factors.append(2)
        number = number // 2
    

    # Check odd numbers from 3 upward
    divisor = 3
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors.append(divisor)
            number = number // divisor
        divisor += 2

    # If remainder is a prime number > 2
    if number > 1:
        factors.append(number)

    return factors


print(prime_factors(120))
