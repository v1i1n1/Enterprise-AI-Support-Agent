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


# Create the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# Create memory
memory = InMemorySaver()


# Create the agent
agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="""You are a helpful personal AI assistant.

Rules:
- Answer general questions clearly.
- Use the calculator for mathematical calculations.
- Remember relevant information from the conversation.
- If you don't know something, say so.
""",
    checkpointer=memory
)


# Conversation configuration
config = {
    "configurable": {
        "thread_id": "personal-assistant-1"
    }
}


print("===================================")
print("      PERSONAL AI ASSISTANT")
print("===================================")
print("Type 'exit' to stop.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("AI: Goodbye!")
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config
    )

    print("\nAI:", response["messages"][-1].content)
    print()