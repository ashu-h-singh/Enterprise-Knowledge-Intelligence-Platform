from backend.app.services.ingestion_service import DocumentIngestionService

DOCS_PATH = "data/raw_docs"
VECTOR_DB_PATH = "data/vector_store"

if __name__ == "__main__":
    ingestion = DocumentIngestionService(
        docs_path=DOCS_PATH,
        vector_db_path=VECTOR_DB_PATH
    )

    ingestion.run()
