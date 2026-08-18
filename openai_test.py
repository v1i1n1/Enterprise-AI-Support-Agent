from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

response = llm.invoke("Explain what an AI Agent is in simple words.")

print(response.content)