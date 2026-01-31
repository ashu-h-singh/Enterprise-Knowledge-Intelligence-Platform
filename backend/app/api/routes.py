from fastapi import APIRouter, HTTPException
from backend.app.services.rag_service import RAGService
from backend.app.models.schemas import QueryRequest, QueryResponse

router = APIRouter()

# Initialize RAG service once (singleton style)
VECTOR_DB_PATH = "data/vector_store"
rag_service = RAGService(VECTOR_DB_PATH)


@router.post("/ask", response_model=QueryResponse)
def ask_question(payload: QueryRequest):
    """
    Secure RAG endpoint with RBAC enforcement.
    """
    try:
        response = rag_service.ask(
            question=payload.question,
            user=payload.user.model_dump()
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
