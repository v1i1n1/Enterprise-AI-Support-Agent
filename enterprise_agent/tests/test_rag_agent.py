from enterprise_agent.agent import agent


print("\n===== RAG AGENT TEST =====")


response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My corporate VPN is not connecting. What should I do?"
            }
        ]
    },
    config={
        "configurable": {
            "thread_id": "rag-test-debug"
        }
    }
)


print("\n===== MESSAGE FLOW =====")

for message in response["messages"]:

    print("\n------------------------------")

    print("TYPE:", type(message).__name__)

    print("CONTENT:")
    print(message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:

        print("\nTOOL CALLS:")

        print(message.tool_calls)