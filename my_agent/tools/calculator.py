def calculator(operation: str, a: float, b: float) -> str:
    """Perform arithmetic. Operations: add, subtract, multiply, divide, power, sqrt.    
    """
    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        if b == 0:
            return "Error: division by zero"
        return str(a / b)
    elif operation == "power":
        return str(a ** b)
    elif operation == "sqrt":
        return str(a ** 0.5)
    else:
        return f"Unknown operation: {operation}"