from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence


# 1. Create the LLM
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# 2. Create the first prompt
explanation_prompt = ChatPromptTemplate.from_template(
    """You are a Generative AI tutor.

Explain {topic} to a beginner.
Keep the explanation simple and technically accurate.
"""
)


# 3. Create the second prompt
question_prompt = ChatPromptTemplate.from_template(
    """Based on the explanation below, generate 3 interview questions.

Explanation:
{explanation}
"""
)


# 4. Create output parser
parser = StrOutputParser()


# 5. First chain
explanation_chain = explanation_prompt | llm | parser


# 6. Complete sequential chain
chain = RunnableSequence(
    explanation_chain,
    lambda explanation: question_prompt.invoke({
        "explanation": explanation
    }),
    llm,
    parser
)


# 7. Run the chain
response = chain.invoke({
    "topic": "Retrieval-Augmented Generation"
})


# 8. Print result
print(response)