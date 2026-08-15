from enterprise_agent.rag.retriever import create_retriever


retriever = create_retriever()


query = "My VPN is not connecting. What should I do?"


results = retriever.invoke(query)


print("\n===== RETRIEVER TEST =====")

print("\nQuery:")
print(query)


print("\nRetrieved Documents:")


for index, document in enumerate(results):

    print(
        f"\n===== RESULT {index + 1} ====="
    )

    print(document.page_content)

    print("\nMetadata:")

    print(document.metadata)