from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression safely."""

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except ZeroDivisionError:

        return "Error: Division by zero is not allowed."

    except (SyntaxError, NameError, TypeError):

        return "Error: Invalid mathematical expression."

    except Exception as e:

        return f"Error while performing calculation: {e}"


# ==========================================
# TEST TOOL
# ==========================================

tests = [
    "125 * 48",
    "10 / 0",
    "25 + 75",
    "hello * 10"
]


for expression in tests:

    result = calculator.invoke({
        "expression": expression
    })

    print(
        f"{expression} -> {result}"
    )