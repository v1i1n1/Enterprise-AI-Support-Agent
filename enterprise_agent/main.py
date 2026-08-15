from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from enterprise_agent.memory import checkpointer

from enterprise_agent.tools import (
    lookup_ticket,
    create_ticket,
    search_knowledge_base
)

from enterprise_agent.config import OPENAI_MODEL


# ==========================================
# Load Environment
# ==========================================

load_dotenv()


# ==========================================
# Create LLM
# ==========================================

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0
)


# ==========================================
# Register Tools
# ==========================================

tools = [
    lookup_ticket,
    create_ticket,
    search_knowledge_base
]


# ==========================================
# Create Enterprise Agent
# ==========================================

agent = create_agent(

    model=llm,

    tools=tools,

    system_prompt="""
You are an Enterprise IT Support AI Agent.

Your responsibilities are:

1. Help users troubleshoot IT issues.
2. Look up existing support tickets when a ticket ID is provided.
3. Search the internal knowledge base for troubleshooting
   information before creating a ticket.
4. Create a new support ticket when:
   - The user explicitly asks to create a ticket, OR
   - Troubleshooting has already been attempted and the issue
     is still unresolved.
5. Provide clear and professional responses.

IMPORTANT TOOL-SELECTION RULES:

- For common IT problems such as VPN, password, or laptop issues,
  search the knowledge base first.
- Do NOT immediately create a ticket for a new troubleshooting
  request unless the user explicitly asks for one.
- If the user says the recommended troubleshooting steps did not
  solve the problem, create a support ticket.
- If a ticket ID is provided, use lookup_ticket.
- Do not invent ticket information.
- Use the conversation history to understand follow-up questions.
""",
    checkpointer=checkpointer
)


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
            "configurable":{
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