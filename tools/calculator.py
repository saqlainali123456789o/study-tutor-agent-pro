from crewai.tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = (
        "Perform arithmetic calculations for educational problems. "
        "Use this tool for arithmetic, algebraic expressions, "
        "percentages, ratios, finance calculations, and statistics."
    )

    def _run(self, expression: str) -> str:
        """
        Evaluate a basic mathematical expression safely.
        """

        if not expression or not expression.strip():
            return "No mathematical expression was provided."

        expression = expression.strip()

        allowed = set(
            "0123456789"
            "+-*/().,% "
        )

        if not all(char in allowed for char in expression):
            return (
                "Invalid expression. "
                "Only basic arithmetic characters are supported."
            )

        try:
            # Convert percentage notation such as 15%
            # into decimal form.
            expression = expression.replace("%", "/100")

            result = eval(
                expression,
                {"__builtins__": {}},
                {},
            )

            return str(result)

        except Exception as exc:
            return f"Calculation error: {exc}"
