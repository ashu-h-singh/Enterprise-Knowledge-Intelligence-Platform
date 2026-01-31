from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS


class RetrievalService:
    def __init__(self, vector_db_path: str):
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        self.vector_store = FAISS.load_local(
            vector_db_path,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query: str, top_k: int = 5):
        return self.vector_store.similarity_search(query, k=top_k)

    def retrieve_with_metadata(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None
    ):
        return self.vector_store.similarity_search(
            query=query,
            k=top_k,
            filter=filters
        )

    def hybrid_retrieve(self, query: str, top_k: int = 5):
        semantic = self.vector_store.similarity_search(query, k=top_k)
        lexical = self.vector_store.similarity_search(query, k=top_k * 2)

        combined = {
            doc.page_content: doc
            for doc in semantic + lexical
        }

        return list(combined.values())[:top_k]
