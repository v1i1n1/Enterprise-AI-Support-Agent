from fastapi import FastAPI
from pydantic import BaseModel

from enterprise_agent.agent import agent


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="Enterprise AI Support Agent",
    description="AI-powered IT support agent API",
    version="1.0.0"
)


# ==========================================
# Request Model
# ==========================================

class ChatRequest(BaseModel):

    message: str

    thread_id: str = "api-user-1"


# ==========================================
# Health Check
# ==========================================

@app.get("/")
def root():

    return {
        "status": "running",
        "service": "Enterprise AI Support Agent"
    }


# ==========================================
# Chat Endpoint
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": request.thread_id
            }
        }
    )

    return {
        "response": response["messages"][-1].content
    }