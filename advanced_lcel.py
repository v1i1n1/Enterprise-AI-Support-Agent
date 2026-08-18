from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv


load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

parser = StrOutputParser()


# --------------------------------
# 1. Summary Chain
# --------------------------------

summary_prompt = ChatPromptTemplate.from_template(
    """Summarize the following text in 3 simple points:

{text}
"""
)

summary_chain = summary_prompt | llm | parser


# --------------------------------
# 2. Keyword Chain
# --------------------------------

keyword_prompt = ChatPromptTemplate.from_template(
    """Extract 5 important keywords from the following text:

{text}
"""
)

keyword_chain = keyword_prompt | llm | parser

# --------------------------------
# 3. Question Generation Chain
# --------------------------------

question_prompt = ChatPromptTemplate.from_template(
    """Generate 3 important questions that can be answered
from the following text:

{text}
"""
)

question_chain = question_prompt | llm | parser


# --------------------------------
# 4. Run Summary + Keywords
#    in parallel
# --------------------------------

parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
    questions=question_chain
)


# --------------------------------
# 5. Final Analysis Prompt
# --------------------------------

analysis_prompt = ChatPromptTemplate.from_template(
    """You are an AI document analyst.

Analyze the document information below.

SUMMARY:
{summary}

KEYWORDS:
{keywords}

QUESTIONS:
{questions}

Provide:

1. Main Topic
2. Key Insights
3. Important Questions
4. Practical Application
5. Short Conclusion

Keep the response clear and concise.
"""
)

# --------------------------------
# 6. Final Analysis Chain
# --------------------------------

analysis_chain = analysis_prompt | llm | parser

# --------------------------------
# 7. Action Items Chain
# --------------------------------

action_prompt = ChatPromptTemplate.from_template(
    """Based on the analysis below, identify 3 practical
action items that an organization could take.

ANALYSIS:
{analysis}

Return the action items as a numbered list.
"""
)

action_chain = action_prompt | llm | parser


# --------------------------------
# 8. Complete Workflow
# --------------------------------

workflow = (
    parallel_chain
    | analysis_chain
    | action_chain
)


# --------------------------------
# 9. Input Document
# --------------------------------

text = """
Artificial intelligence is transforming many industries.
Generative AI models can understand and generate text,
images and code. Organizations are using these systems
for customer support, software development, document
analysis and automation.
"""


# --------------------------------
# 10. Execute
# --------------------------------

result = workflow.invoke({
    "text": text
})


print("===== FINAL ANALYSIS =====")
print(result)