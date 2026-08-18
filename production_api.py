from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

import time


load_dotenv()


# ==========================================
# Primary LLM
# ==========================================

primary_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ==========================================
# Prompt
# ==========================================

prompt = ChatPromptTemplate.from_template(
    """
Answer the following question clearly and
concisely.

Question:
{question}
"""
)


# ==========================================
# Primary Request
# ==========================================

def primary_request(data):

    prompt_value = prompt.invoke(data)

    return primary_llm.invoke(prompt_value)


# ==========================================
# Retry + Fallback
# ==========================================

def reliable_request(data):

    max_retries = 2

    for attempt in range(1, max_retries + 1):

        try:

            print(f"Attempt {attempt}")

            response = primary_request(data)

            return response

        except Exception as e:

            print(f"Primary request failed: {e}")

            if attempt < max_retries:

                print("Retrying...")
                time.sleep(1)

            else:

                print("Using fallback response.")

                return (
                    "The AI service is temporarily unavailable. "
                    "Please try again shortly."
                )


# ==========================================
# Runnable
# ==========================================

reliable_chain = RunnableLambda(
    reliable_request
)


# ==========================================
# FastAPI
# ==========================================

app = FastAPI(
    title="Production Ready AI API",
    version="1.0",
    description="AI API with retry and fallback handling"
)


# ==========================================
# LangServe Route
# ==========================================

add_routes(
    app,
    reliable_chain,
    path="/ai"
)


# ==========================================
# Start Server
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )