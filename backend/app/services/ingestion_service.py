import os
from typing import Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS


class DocumentIngestionService:
    def __init__(
        self,
        docs_path: str,
        vector_db_path: str,
        department: Optional[str] = None,
        access_level: str = "user"
    ):
        """
        docs_path: path where raw documents are stored
        vector_db_path: path to store FAISS index
        department: logical owner of the document (e.g. hr, finance, security)
        access_level: who can access this document (admin/user)
        """
        self.docs_path = docs_path
        self.vector_db_path = vector_db_path
        self.department = department
        self.access_level = access_level

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

    def load_documents(self):
        documents = []

        for file in os.listdir(self.docs_path):
            if file.lower().endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(self.docs_path, file))
                docs = loader.load()

                for doc in docs:
                    # Core metadata
                    doc.metadata["source"] = file

                    # RBAC metadata (Step 7)
                    doc.metadata["department"] = self.department
                    doc.metadata["access_level"] = self.access_level

                    documents.append(doc)

        return documents

    def process_documents(self, documents):
        """
        Split documents into semantically meaningful chunks.
        """
        return self.text_splitter.split_documents(documents)

    def store_embeddings(self, chunks):
        """
        Create embeddings and persist FAISS vector store.
        """
        vector_store = FAISS.from_documents(
            chunks,
            self.embedding_model
        )

        vector_store.save_local(self.vector_db_path)
        return vector_store

    def run(self):
        print("Loading documents...")
        documents = self.load_documents()

        if not documents:
            raise ValueError("No documents found for ingestion.")

        print("Chunking documents...")
        chunks = self.process_documents(documents)

        print("Creating embeddings and storing in FAISS...")
        self.store_embeddings(chunks)

        print("Ingestion complete.")
