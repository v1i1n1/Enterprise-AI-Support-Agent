from enterprise_agent.rag.loader import load_documents


documents = load_documents()


print("\n===== DOCUMENT LOADING TEST =====")

print(
    "Number of documents:",
    len(documents)
)


for document in documents:

    print("\n===== DOCUMENT CONTENT =====")

    print(
        document.page_content[:500]
    )

    print("\n===== METADATA =====")

    print(document.metadata)