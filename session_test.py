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


# -----------------------------
# User 1
# -----------------------------

user1_config = {
    "configurable": {
        "thread_id": "user-1"
    }
}


agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My name is Vinod."
            }
        ]
    },
    user1_config
)


# -----------------------------
# User 2
# -----------------------------

user2_config = {
    "configurable": {
        "thread_id": "user-2"
    }
}


agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My name is Rahul."
            }
        ]
    },
    user2_config
)


# -----------------------------
# Ask User 1
# -----------------------------

response1 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is my name?"
            }
        ]
    },
    user1_config
)


print("User 1:", response1["messages"][-1].content)


# -----------------------------
# Ask User 2
# -----------------------------

response2 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is my name?"
            }
        ]
    },
    user2_config
)


print("User 2:", response2["messages"][-1].content)