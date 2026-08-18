from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv


load_dotenv()


# ==========================================
# 1. Create LLM
# ==========================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ==========================================
# 2. Create Prompt
# ==========================================

prompt = ChatPromptTemplate.from_template(
    """Answer the following question in simple words:

Question:
{question}
"""
)


# ==========================================
# 3. Output Parser
# ==========================================

parser = StrOutputParser()


# ==========================================
# 4. Create LCEL Chain
# ==========================================

chain = prompt | llm | parser


# ==========================================
# 5. Create FastAPI Application
# ==========================================

app = FastAPI(
    title="My AI API",
    version="1.0",
    description="Simple LangServe AI API"
)


# ==========================================
# 6. Expose Chain as REST API
# ==========================================

add_routes(
    app,
    chain,
    path="/ai"
)


# ==========================================
# 7. Run Server
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )