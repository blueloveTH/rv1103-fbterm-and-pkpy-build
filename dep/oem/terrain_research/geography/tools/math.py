import math

def float_mod(a: float, b: float) -> float:
    return a - b * math.floor(a / b)