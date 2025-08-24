import random

def roll_dices(n,f):
    tot = 0
    for j in range(n):
        tot += random.randint(1,f)
    return tot
