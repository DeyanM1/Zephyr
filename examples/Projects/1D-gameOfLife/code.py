"""
One-Dimensional Life (Jon Millen's cellular automaton)
https://jonmillen.com/1dlife/index.html

Neighborhood: two cells left, two cells right (YYXYY).
Cells outside the row (past the edges) are treated as dead (0).

The list is 1-indexed: index 0 is an unused placeholder,
real cells live at indexes 1 through n.
"""

RULE_DEAD  = [0, 0, 1, 1, 0]   # next state of a currently DEAD cell, by neighbor total 0-4
RULE_ALIVE = [0, 0, 1, 0, 1]   # next state of a currently ALIVE cell, by neighbor total 0-4

INITIAL_STATE = "0011010001101010001"

state = [None] + list(map(int, INITIAL_STATE))


def display(row):
    print("".join(map(str, row[1:])))


def step(row):
    n = len(row) - 1
    new_row = [None]
    i = 1
    while i <= n:
        if i - 2 >= 1:
            left2 = row[i - 2]
        else:
            left2 = 0

        if i - 1 >= 1:
            left1 = row[i - 1]
        else:
            left1 = 0

        if i + 1 <= n:
            right1 = row[i + 1]
        else:
            right1 = 0

        if i + 2 <= n:
            right2 = row[i + 2]
        else:
            right2 = 0

        total = left2 + left1 + right1 + right2
        current = row[i]

        if current == 0:
            next_state = RULE_DEAD[total]
        else:
            next_state = RULE_ALIVE[total]

        new_row.append(next_state)
        i = i + 1

    return new_row


display(state)

count = 0
while count < 40:
    state = step(state)
    display(state)
    count = count + 1