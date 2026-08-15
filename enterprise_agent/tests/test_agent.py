from enterprise_agent.agent import agent


print("\n===== AGENT INTEGRATION TEST =====")


response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the status of INC001?"
            }
        ]
    },
    config={
        "configurable": {
            "thread_id": "test-agent-1"
        }
    }
)


final_message = response["messages"][-1].content


print("\nAgent Response:")
print(final_message)