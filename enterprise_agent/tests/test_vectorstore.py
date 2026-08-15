from enterprise_agent.rag.vectorstore import create_vector_store


vector_store = create_vector_store()


print("\n===== VECTOR STORE TEST =====")

query = "My VPN is not connecting. What should I do?"


results = vector_store.similarity_search(
    query,
    k=2
)


print("\nQuery:")
print(query)


print("\nRetrieved Documents:")

for index, document in enumerate(results):

    print(f"\n===== RESULT {index + 1} =====")

    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)
    