from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from enterprise_agent.rag.splitter import split_documents


# Load environment variables
load_dotenv()


def create_embeddings():

    chunks = split_documents()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return chunks, embeddings