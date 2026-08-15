from enterprise_agent.rag.embeddings import create_embeddings


chunks, embeddings = create_embeddings()


print("\n===== EMBEDDING TEST =====")

print(
    "Number of chunks:",
    len(chunks)
)


text = chunks[0].page_content


vector = embeddings.embed_query(text)


print(
    "Embedding vector length:",
    len(vector)
)


print(
    "First 10 values:",
    vector[:10]
)