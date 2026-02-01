


def is_prime(currentNum: int):
    # Only proceed if number is at least 2
    if currentNum >= 2:
        i = 2
        prime_flag = True
        while i * i <= currentNum:
            if currentNum % i == 0:
                prime_flag = False
            i += 1
        # Only print if still prime
        if prime_flag:
            print("IS Prime ", currentNum)

# Print primes up to 20 using while
num = 2
while num <= 1000:
    is_prime(num)  # Function handles printing
    num += 1
