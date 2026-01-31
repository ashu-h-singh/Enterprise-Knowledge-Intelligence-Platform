Enterprise Knowledge Intelligence Platform (EKIP)

🔹 Overview

Enterprise Knowledge Intelligence Platform (EKIP) is a production-style GenAI system that enables organizations to securely query internal documents using Retrieval-Augmented Generation (RAG).

Unlike simple chatbots, EKIP is designed with enterprise requirements in mind:

Role-Based Access Control (RBAC)

Hallucination control

Source-grounded answers

Modular, scalable architecture

Local LLM support (Ollama)

This project demonstrates how real-world companies build internal GenAI knowledge assistants.

🔹 Key Features
✅ Intelligent Document Ingestion

Supports PDF documents

Cleans and chunks documents intelligently

Generates embeddings using Sentence Transformers

Stores vectors in FAISS for fast retrieval

Enriches documents with metadata (department, access level)

✅ Advanced Retrieval-Augmented Generation (RAG)

Semantic retrieval using FAISS

Hybrid retrieval strategy

Re-ranking for improved relevance

Context window optimization

Deterministic, grounded generation

✅ Hallucination Control & Safety

Retrieval confidence gating

Context sufficiency checks

Strict prompt grounding

Explicit “I don’t know” handling

Mandatory source attribution

✅ Role-Based Access Control (RBAC)

User roles: admin, user

Metadata-based filtering at retrieval time

Unauthorized documents are never passed to the LLM

✅ Local LLM (Cost & Privacy Friendly)

Uses Ollama (LLaMA-3) locally

No paid APIs required

Data never leaves the system

✅ Full-Stack Demo

FastAPI backend with schema validation

Streamlit frontend for demo and presentation

Swagger UI for API testing


🔹 System Architecture
Streamlit UI
     ↓
FastAPI Backend
     ↓
RAG Orchestrator
     ↓
Retriever (FAISS + Metadata Filters)
     ↓
Re-ranker
     ↓
Ollama (LLaMA-3)
     ↓
Answer + Sources


Design Principle:

Security, grounding, and access control are enforced before the LLM is invoked.

🔹 Tech Stack
Layer	Technology
Language	Python
Backend	FastAPI
Frontend	Streamlit
LLM	Ollama (LLaMA-3)
Embeddings	Sentence-Transformers
Vector DB	FAISS
RAG Framework	LangChain
Security	RBAC via metadata filtering
🔹 Project Structure
ekip/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── api/
│       ├── services/
│       │   ├── ingestion_service.py
│       │   ├── retrieval_service.py
│       │   ├── reranker_service.py
│       │   └── rag_service.py
│       ├── models/
│       └── core/
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── raw_docs/
│   └── vector_store/
│
├── scripts/
│   └── ingest_docs.py
│
└── README.md
