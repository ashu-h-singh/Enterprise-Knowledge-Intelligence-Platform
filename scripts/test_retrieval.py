from backend.app.services.retrieval_service import RetrievalService

VECTOR_DB_PATH = "data/vector_store"

retriever = RetrievalService(VECTOR_DB_PATH)

query = "What is the security policy for passwords?"

results = retriever.retrieve(query)

print("\n Retrieved Chunks:\n")
for i, doc in enumerate(results, 1):
    print(f"Result {i}:")
    print(doc.page_content[:300])
    print("Source:", doc.metadata.get("source"))
    print("-" * 50)
