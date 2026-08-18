from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


with SqliteSaver.from_conn_string("agent_memory.db") as checkpointer:

    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt="""You are a helpful personal AI assistant.
Remember relevant information from the conversation.""",
        checkpointer=checkpointer
    )

    config = {
        "configurable": {
            "thread_id": "user-1"
        }
    }

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "My favorite programming language is Python."
                }
            ]
        },
        config
    )

    print("AI:", response["messages"][-1].content)

    print("\nInformation stored successfully.")