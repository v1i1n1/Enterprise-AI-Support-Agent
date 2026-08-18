from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Create the prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful Generative AI tutor.

Answer the user's questions clearly and accurately.

Rules:
- Explain concepts in simple language.
- Give an example when useful.
- If you don't know the answer, say that you don't know.
- Do not invent facts.
"""
    ),
    (
        "human",
        "{question}"
    )
])


# Create the LLM
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# Create output parser
parser = StrOutputParser()


# Build the chain
chain = prompt | llm | parser


# Ask the user for a question
question = input("Ask your question: ")


# Execute the chain
response = chain.invoke({
    "question": question
})


# Display the answer
print("\nAI Assistant:")
print(response)