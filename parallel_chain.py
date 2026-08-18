from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


# 1. Create the LLM
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# 2. Prompt for explanation
explanation_prompt = ChatPromptTemplate.from_template(
    """Explain {topic} in simple words for a beginner.

Keep the explanation technically accurate.
"""
)


# 3. Prompt for interview questions
question_prompt = ChatPromptTemplate.from_template(
    """Generate 3 interview questions about {topic}.

Keep them suitable for a beginner.
"""
)


# 4. Output parser
parser = StrOutputParser()


# 5. Create two independent chains
explanation_chain = explanation_prompt | llm | parser

question_chain = question_prompt | llm | parser


# 6. Run both chains in parallel
parallel_chain = RunnableParallel(
    explanation=explanation_chain,
    questions=question_chain
)


# 7. Execute
response = parallel_chain.invoke({
    "topic": "AWS Lambda"
})


# 8. Display results
print("===== EXPLANATION =====")
print(response["explanation"])

print("\n===== INTERVIEW QUESTIONS =====")
print(response["questions"])