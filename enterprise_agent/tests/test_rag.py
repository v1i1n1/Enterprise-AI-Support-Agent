from enterprise_agent.rag.rag_chain import rag_query


print("\n===== RAG TEST =====")


question = "My VPN is not connecting. What should I do?"


answer = rag_query(question)


print("\nQuestion:")
print(question)


print("\nRAG Answer:")
print(answer)