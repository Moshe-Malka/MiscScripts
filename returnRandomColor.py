import random

def returnRandomColor:
    return ''.join([x for i in range(6) for x in random.choice([a for a in '1234567890abcdef'])])

def returnRandomColorHex:
    return '#'+''.join([x for i in range(6) for x in random.choice([a for a in '1234567890abcdef'])])
