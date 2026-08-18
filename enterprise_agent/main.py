from enterprise_agent.agent import agent


# ==========================================
# Interactive Chat
# ==========================================

print()
print("==========================================")
print("     ENTERPRISE AI SUPPORT AGENT")
print("==========================================")
print("Type 'exit' to stop.")
print()


while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":

        print("AI: Goodbye!")

        break

    if not user_input:

        continue

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "user-1"
            }
        }
    )

    print()
    print(
        "AI:",
        response["messages"][-1].content
    )
    print()