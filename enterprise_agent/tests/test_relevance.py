from enterprise_agent.rag.vectorstore import create_vector_store


vector_store = create_vector_store()


queries = [
    "My VPN is not connecting",
    "How do I reset my corporate password?",
    "How do I configure corporate email?",
    "What is the capital of France?",
    "Write a Python program to calculate factorial",
    "Who is Elon Musk?"
]


for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)

    results = vector_store.similarity_search_with_score(
        query,
        k=2
    )

    for index, (document, score) in enumerate(results, start=1):

        print(f"\nRESULT {index}")
        print("SCORE:", score)
        print("CONTENT:")
        print(document.page_content[:300])