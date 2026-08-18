from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

memory = InMemorySaver()


agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="You are a helpful assistant.",
    checkpointer=memory
)


config = {
    "configurable": {
        "thread_id": "user-1"
    }
}


# First message
agent.invoke(
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


# Second message
agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "I am learning Generative AI."
            }
        ]
    },
    config
)


# Inspect the stored state
state = agent.get_state(config)

print("===== CURRENT STATE =====")
print(state)

print("\n===== MESSAGES =====")

for message in state.values["messages"]:
    print(f"{message.__class__.__name__}: {message.content}")