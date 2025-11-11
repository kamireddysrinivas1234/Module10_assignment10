
from typing import Union
Number = Union[int, float]
def add(a: Number, b: Number) -> Number: return a + b
def subtract(a: Number, b: Number) -> Number: return a - b
def multiply(a: Number, b: Number) -> Number: return a * b
def divide(a: Number, b: Number) -> Number:
    if b == 0: raise ZeroDivisionError("Division by zero.")
    return a / b
