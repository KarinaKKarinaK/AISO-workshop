def calculator(operation: str, a: float, b: float) -> str:
    # calculator tool
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
    elif operation == "round":
        return str(round(a, int(b)))
    else:
        return f"Unknown operation: {operation}"
