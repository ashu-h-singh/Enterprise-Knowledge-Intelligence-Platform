from pydantic import BaseModel, Field
from typing import List, Optional


# =========================
# 👤 USER & AUTH SCHEMAS
# =========================

class User(BaseModel):
    """
    Represents a system user.
    Used for RBAC enforcement.
    """
    username: str
    role: str = Field(
        ...,
        description="User role: admin or user"
    )


# =========================
# 📄 DOCUMENT METADATA
# =========================

class DocumentMetadata(BaseModel):
    """
    Metadata attached to each document chunk.
    Used for filtering, security, and auditing.
    """
    source: str
    department: Optional[str] = None
    access_level: str = Field(
        ...,
        description="Access level required to view this document (admin/user)"
    )


# =========================
# ❓ QUERY REQUEST
# =========================

class QueryRequest(BaseModel):
    """
    Input payload for /ask API.
    """
    question: str
    user: User


# =========================
# ✅ RAG RESPONSE
# =========================

class QueryResponse(BaseModel):
    """
    Output response returned by RAG system.
    """
    answer: str
    sources: List[str]


# =========================
# 📤 DOCUMENT UPLOAD
# =========================

class DocumentUploadRequest(BaseModel):
    """
    Metadata provided during document upload.
    """
    department: Optional[str] = None
    access_level: str = Field(
        ...,
        description="Who can access this document (admin/user)"
    )


class DocumentUploadResponse(BaseModel):
    """
    Response after successful document ingestion.
    """
    message: str
    document_name: str
