import math

def kv_koren(x):
    return math.sqrt(x)

def stepen(x, stepen):
    return x ** stepen

def add_numbers(a: int, b: int) -> int:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("На ноль делить нельзя.")
    return a / b

def max_of_two(a, b):
    if a > b:
        return a
    if b > a:
        return b
    if a == b:
        print("Равны")

def calculator(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        if b == 0:
            raise ValueError("На ноль делить нельзя")
        return a / b
    else:
        return None