from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


# Create the OpenAI model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# Create the agent
agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="""You are a helpful AI assistant.

Use the calculator tool whenever a user asks
you to perform a mathematical calculation.

For general questions, answer directly.
Always provide a clear final answer.
"""
)


# Test question
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is an AI Agent?"
        }
    ]
})

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is 125 * 48?"
        }
    ]
})

# Display messages
for message in result["messages"]:
    print("\n---")
    print(message)