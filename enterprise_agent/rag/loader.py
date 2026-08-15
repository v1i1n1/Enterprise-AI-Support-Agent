from pathlib import Path

from langchain_community.document_loaders import TextLoader


DOCUMENT_PATH = (
    Path(__file__).parent /
    "documents" /
    "it_support.txt"
)


def load_documents():

    loader = TextLoader(
        str(DOCUMENT_PATH),
        encoding="utf-8"
    )

    documents = loader.load()

    return documents