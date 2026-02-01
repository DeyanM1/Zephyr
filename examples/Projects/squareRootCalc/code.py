def sqrt_estimate(num: int, iterations: int=100):
    if num < 0:
        print("X must not be negative")
    
    else:
        guess = 0

        if num != 0:     
            guess = num / 2.0

            while iterations != 0:
                guess = (guess + num / guess) / 2.0
                iterations -= 1

        print(guess)


# example usage
number = 25112346547395323452345234532453
sqrt_estimate(number)

