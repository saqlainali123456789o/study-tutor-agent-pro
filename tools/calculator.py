import ast
import math
import operator as op
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

_ALLOWED = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod, ast.USub: op.neg, ast.UAdd: op.pos}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"sqrt", "log", "log10", "sin", "cos", "tan"}:
        fn = getattr(math, node.func.id)
        return fn(*[_eval(a) for a in node.args])
    if isinstance(node, ast.Name) and node.id == "pi":
        return math.pi
    raise ValueError("Unsupported expression")


def calculate(expression: str) -> float:
    tree = ast.parse(expression, mode="eval")
    return float(_eval(tree.body))


class CalculatorInput(BaseModel):
    expression: str = Field(description="A mathematical expression using numbers, +, -, *, /, **, %, sqrt, log, log10, sin, cos, tan, or pi.")


class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Perform deterministic arithmetic and mathematical calculations."
    args_schema = CalculatorInput

    def _run(self, expression: str) -> str:
        try:
            return str(calculate(expression))
        except Exception as exc:
            return f"Calculation error: {exc}"
