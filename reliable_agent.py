from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


load_dotenv()


# ==========================================
# Primary Tool
# ==========================================

@tool
def primary_service(request: str) -> str:
    """Primary service that may fail."""

    raise RuntimeError("Primary service is temporarily unavailable.")


# ==========================================
# Fallback Tool
# ==========================================

@tool
def fallback_service(request: str) -> str:
    """Backup service used when the primary service fails."""

    return f"Fallback service successfully processed: {request}"


# ==========================================
# Reliable Service Function
# ==========================================

def reliable_service(request: str):

    max_retries = 2

    for attempt in range(1, max_retries + 1):

        try:

            print(f"Primary attempt {attempt}")

            result = primary_service.invoke({
                "request": request
            })

            return result

        except Exception as e:

            print(f"Primary failed: {e}")

            if attempt < max_retries:
                print("Retrying...")

    print("Primary service failed after retries.")
    print("Switching to fallback service...")

    return fallback_service.invoke({
        "request": request
    })


# ==========================================
# Test Reliable Service
# ==========================================

result = reliable_service(
    "Process customer support request"
)

print("\nFinal Result:")
print(result)


# ==========================================
# Create LLM
# ==========================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ==========================================
# Create Agent
# ==========================================

agent = create_agent(
    model=llm,
    tools=[fallback_service],
    system_prompt="""
You are a reliable AI assistant.

If the primary service fails, a fallback service
should be used to complete the request.
"""
)


# ==========================================
# Agent Test
# ==========================================

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Use the fallback service to process my request."
            }
        ]
    }
)


print("\n===== AGENT RESPONSE =====")
print(response["messages"][-1].content)