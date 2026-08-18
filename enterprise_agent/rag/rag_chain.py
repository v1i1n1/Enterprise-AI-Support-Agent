from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from enterprise_agent.rag.retriever import create_retriever


load_dotenv()


# ==========================================
# Create Retriever
# ==========================================

retriever = create_retriever()


# ==========================================
# Create LLM
# ==========================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)


# ==========================================
# RAG Prompt
# ==========================================

prompt = ChatPromptTemplate.from_template(
    """
You are an Enterprise IT Support Assistant.

Answer the user's question using ONLY the
information provided in the context.

If the answer is not present in the context,
say that the information is not available
in the knowledge base.

Do not invent information.

Context:
{context}

User Question:
{question}

Answer:
"""
)


# ==========================================
# RAG Function
# ==========================================

def rag_query(question: str) -> str:

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)

    return response.content