from langchain_ollama import ChatOllama
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)

llm_with_tools = llm.bind_tools([calculator])


# Step 1: Ask the model
response = llm_with_tools.invoke(
    "What is 125 * 48?"
)

print("MODEL RESPONSE:")
print(response)

print("\nTOOL CALL:")
print(response.tool_calls)


# Step 2: Extract the tool call
tool_call = response.tool_calls[0]

print("\nTOOL NAME:")
print(tool_call["name"])

print("\nTOOL ARGUMENTS:")
print(tool_call["args"])


# Step 3: Execute the calculator
tool_result = calculator.invoke(tool_call["args"])

print("\nTOOL RESULT:")
print(tool_result)