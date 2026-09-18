"""Calculator tool — AST-safe arithmetic."""
from __future__ import annotations
import ast

_ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.USub, ast.UAdd, ast.FloorDiv)

def calc(expr: str) -> float:
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ValueError(f"unsupported: {type(node).__name__}")
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            raise ValueError("only numbers allowed")
    return eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, {})
