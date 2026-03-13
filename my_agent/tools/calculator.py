import ast
import math
from typing import Any


_BINARY_OPS: dict[type[ast.operator], Any] = {
    ast.Add: lambda x, y: x + y,
    ast.Sub: lambda x, y: x - y,
    ast.Mult: lambda x, y: x * y,
    ast.Div: lambda x, y: x / y,
    ast.Pow: lambda x, y: x**y,
    ast.Mod: lambda x, y: x % y,
}
_UNARY_OPS: dict[type[ast.unaryop], Any] = {
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}
_ALLOWED_FUNCS: dict[str, Any] = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
}
_ALLOWED_CONSTS: dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Only numeric constants are allowed in expressions.")
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return float(_BINARY_OPS[type(node.op)](left, right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return float(_UNARY_OPS[type(node.op)](_eval_node(node.operand)))
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTS:
            return float(_ALLOWED_CONSTS[node.id])
        raise ValueError(f"Unsupported name in expression: {node.id}")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Unsupported function call in expression.")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCS:
            raise ValueError(f"Unsupported function: {func_name}")
        args = [_eval_node(arg) for arg in node.args]
        return float(_ALLOWED_FUNCS[func_name](*args))
    raise ValueError("Unsupported expression.")


def _safe_eval_expression(expression: str) -> float:
    normalized = expression.replace("^", "**").strip()
    parsed = ast.parse(normalized, mode="eval")
    return _eval_node(parsed)


def _format_number(value: float) -> str:
    if math.isfinite(value) and abs(value - round(value)) < 1e-12:
        return str(int(round(value)))
    return str(value)


def calculator(
    operation: str = "",
    a: float = 0.0,
    b: float = 0.0,
    expression: str = "",
    ndigits: int = -1,
) -> str:
    """Perform precise arithmetic for benchmark questions.

    Prefer passing `expression` for multi-step math (e.g. "(347.8*219.6)**0.5").
    You can also call with an operation and one/two numbers.

    Args:
        operation: add, subtract, multiply, divide, power, sqrt, or round.
        a: First number for operation mode.
        b: Second number for operation mode.
        expression: Math expression using numbers/operators/parentheses and
            optional sqrt(), abs(), round(), pi, e.
        ndigits: Optional final rounding digits to apply to the computed result.

    Returns:
        Numeric result as text, formatted for direct answering.
    """
    if a is None:
        a = 0.0
    if b is None:
        b = 0.0
    normalized_operation = operation.strip().lower()

    try:
        if expression.strip():
            result = _safe_eval_expression(expression)
        elif normalized_operation and any(op in normalized_operation for op in "+-*/^()"):
            # If only one string is provided, treat it as an expression candidate.
            result = _safe_eval_expression(normalized_operation)
        elif normalized_operation in {"add", "plus", "+"}:
            result = a + b
        elif normalized_operation in {"subtract", "minus", "-"}:
            result = a - b
        elif normalized_operation in {"multiply", "times", "*", "x"}:
            result = a * b
        elif normalized_operation in {"divide", "/"}:
            result = 0.0 if b == 0 else a / b
        elif normalized_operation in {"power", "pow", "^", "**"}:
            result = a**b
        elif normalized_operation in {"sqrt", "square_root", "root"}:
            result = 0.0 if a < 0 else math.sqrt(a)
        elif normalized_operation in {"round"}:
            digits = int(b)
            result = round(a, digits)
        elif normalized_operation:
            # Last attempt: try parsing operation text as expression.
            result = _safe_eval_expression(normalized_operation)
        else:
            result = a
    except Exception:
        result = 0.0

    if ndigits is not None and ndigits >= 0:
        result = round(float(result), ndigits)

    return _format_number(float(result))
