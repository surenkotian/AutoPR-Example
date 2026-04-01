def multiply(a, b):
    return a * b

def divide(a, b):
    """Divide two numbers with zero division protection."""
    return a / b if b != 0 else 0
