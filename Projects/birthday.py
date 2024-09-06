"""
"Geburtstagsparadoxon"
Es geht darum, die Wahrscheinlichkeit zu berechnen, 
dass in einer Gruppe von n Personen mindestens zwei den gleichen Geburtstag haben.
"""




n = 2
iMax = 5
i = 0


prob = 1.0

while i < 5:
    # Calculate probability of unique birthdays up to n
    probMO = (prob * ((365 - (n - 1)) / 365))
    prob = probMO
    
    probability_same_birthdayNum = (1-prob) * 100
    print(f"[{i}] - {probability_same_birthdayNum}%")
    
    n += 1
    i += 1
