from enterprise_agent.rag.splitter import split_documents


chunks = split_documents()


print("\n===== CHUNKING TEST =====")

print(
    "Number of chunks:",
    len(chunks)
)


for index, chunk in enumerate(chunks):

    print(
        f"\n===== CHUNK {index + 1} ====="
    )

    print(chunk.page_content)

    print("\nMetadata:")

    print(chunk.metadata)