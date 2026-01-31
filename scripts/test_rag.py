from backend.app.services.rag_service import RAGService

VECTOR_DB_PATH = "data/vector_store"

rag = RAGService(VECTOR_DB_PATH)

question = "What is the password rotation policy?"

response = rag.ask(question)

print("\n QUESTION:")
print(response["question"])

print("\n ANSWER:")
print(response["answer"])

print("\n SOURCES:")
for src in response["sources"]:
    print("-", src)
