from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


# Create the model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# Create memory/checkpointer
memory = InMemorySaver()


# Create the agent
agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="""You are a helpful personal AI assistant.

Use the calculator for mathematical calculations.
Answer general questions directly.
Remember information from the conversation when relevant.
""",
    checkpointer=memory
)


# Conversation ID
config = {
    "configurable": {
        "thread_id": "user-1"
    }
}


# First question
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My name is Vinod."
            }
        ]
    },
    config
)

print("\nAI:", response["messages"][-1].content)


# Second question
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is my name?"
            }
        ]
    },
    config
)

print("\nAI:", response["messages"][-1].content)