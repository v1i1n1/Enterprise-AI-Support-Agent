from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. Create the prompt
prompt = ChatPromptTemplate.from_template(
    """You are an AI tutor specializing in Generative AI.

Explain {topic} in simple words for a beginner.
Give a technically accurate explanation.
Do not confuse it with blockchain or other technologies.
"""
)


# 2. Create the LLM
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# 3. Create the output parser
parser = StrOutputParser()


# 4. Create the LangChain
chain = prompt | llm | parser


# 5. Send input to the chain
response = chain.invoke({
    "topic": "LangChain"
})


# 6. Display the result
print(response)