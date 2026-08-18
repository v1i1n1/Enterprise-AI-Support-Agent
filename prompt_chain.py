from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


prompt = ChatPromptTemplate.from_template(
    """You are a Generative AI tutor.

We are studying Generative AI and LangChain.

In this context, RAG means Retrieval-Augmented Generation.

Explain {topic} to a beginner.

Include:
1. Simple definition
2. Why it is used
3. One real-world example

Do not use alternative meanings of the abbreviation.
"""
)


llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


parser = StrOutputParser()


chain = prompt | llm | parser


response = chain.invoke({
    "topic": "RAG"
})


print(response)