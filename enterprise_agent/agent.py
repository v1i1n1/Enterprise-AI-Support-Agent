from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from enterprise_agent.memory import checkpointer

from enterprise_agent.tools import (
    lookup_ticket,
    create_ticket,
    search_rag_knowledge_base
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
    search_rag_knowledge_base
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

- For common IT problems such as VPN, password, laptop, or email
  issues, use search_rag_knowledge_base first.

- Use search_rag_knowledge_base as the primary knowledge source
  for enterprise troubleshooting, procedures, policies, and
  internal documentation.

- If a ticket ID is provided, use lookup_ticket.

- Do NOT immediately create a ticket for a new troubleshooting
  request unless the user explicitly asks for one.

- If the user says the recommended troubleshooting steps did
  not solve the issue, create a support ticket.

- When using the RAG knowledge base, provide the relevant
  information completely and accurately. Do not unnecessarily
  omit important troubleshooting steps.

- Do not invent ticket information or knowledge-base information.

- Use the conversation history to understand follow-up questions.
""",

    checkpointer=checkpointer
)