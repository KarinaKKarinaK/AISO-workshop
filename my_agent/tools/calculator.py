def calculator(operation: str, a: float, b: float = 0) -> str:
    """Use this tool to perform ANY mathematical calculation. You MUST call this tool whenever you need to do arithmetic.

    Supported operations:
    - "add": returns a + b
    - "subtract": returns a - b
    - "multiply": returns a * b
    - "divide": returns a / b
    - "power": returns a raised to the power of b (a^b)
    - "sqrt": returns the square root of a (b is ignored)
    - "round": rounds a to b decimal places

    For multi-step calculations, call this tool multiple times. For example, to compute (2^47) / 378:
      Step 1: calculator("power", 2, 47) -> get result X
      Step 2: calculator("divide", X, 378) -> get final answer

    Args:
        operation: One of "add", "subtract", "multiply", "divide", "power", "sqrt", "round"
        a: The first number
        b: The second number (optional for sqrt, number of decimal places for round)

    Returns:
        The result of the calculation as a string.
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
    elif operation == "round":
        return str(round(a, int(b)))
    else:
        return f"Unknown operation: {operation}"
