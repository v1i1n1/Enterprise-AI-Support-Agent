from enterprise_agent.rag.vectorstore import create_vector_store


def create_retriever():

    vector_store = create_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 2
        }
    )

    return retriever