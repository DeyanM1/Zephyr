import math

# Calculate Pi using the Leibniz formula
pi = 0.0
divisor = 1.0
iterations = 5000000

for i in range(1, iterations+1):
    pi = pi + 4.0/divisor - 4.0/(divisor+2.0)
    print(f"Pi approximation after {i} iterations ({round(i/iterations*100, 3)}%): {pi}")
    divisor += 4.0
    
print(f"Final Pi approximation: {pi} / {math.pi}  |  Difference: {abs(math.pi - pi)}")
