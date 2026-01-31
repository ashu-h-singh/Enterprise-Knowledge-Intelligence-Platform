from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.reranker_service import ReRankerService


# Safety Thresholds
MIN_DOCS_REQUIRED = 2
MIN_CONTEXT_CHARS = 500
MAX_CONTEXT_CHARS = 3000


class RAGService:
    def __init__(self, vector_db_path: str):
        self.retriever = RetrievalService(vector_db_path)
        self.reranker = ReRankerService()

        # Local LLM (Ollama)
        self.llm = Ollama(
            model="llama3",
            temperature=0
        )

        # Grounded prompt (hallucination control)
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are an enterprise AI assistant.

RULES:
- Use ONLY the information provided in the context
- Do NOT use outside knowledge
- If the answer is not clearly present, say "I don't know"
- Be concise and factual

Context:
{context}

Question:
{question}

Answer:
"""
        )

    def _build_context(self, docs):
        context = ""
        for doc in docs:
            if len(context) + len(doc.page_content) > MAX_CONTEXT_CHARS:
                break
            context += doc.page_content + "\n\n"
        return context.strip()

    def ask(self, question: str, user: dict):
        """
        question: user query
        user: dict containing username and role (admin/user)
        """

        # 1. RBAC filter based on user role
        user_role = user.get("role")
        filters = {
            "access_level": user_role
        }

        # 2. Secure retrieval with metadata filtering
        docs = self.retriever.retrieve_with_metadata(
            query=question,
            filters=filters
        )

        # 3. Re-rank retrieved documents
        docs = self.reranker.rerank(question, docs)

        # 4. Retrieval confidence check
        if len(docs) < MIN_DOCS_REQUIRED:
            return {
                "answer": "I don't have enough reliable information to answer this question.",
                "sources": []
            }

        # 5. Build context
        context = self._build_context(docs)

        # 6. Context sufficiency check
        if len(context) < MIN_CONTEXT_CHARS:
            return {
                "answer": "The available documents do not contain sufficient information to answer confidently.",
                "sources": []
            }

        # 7. Build grounded prompt
        prompt = self.prompt.format(
            context=context,
            question=question
        )

        # 8. Generate answer
        answer = self.llm.invoke(prompt).strip()

        # 9. Post-generation hallucination check
        if answer.lower().startswith("i don't know"):
            return {
                "answer": answer,
                "sources": []
            }

        # 10. Source enforcement
        sources = list(
            {doc.metadata.get("source") for doc in docs if doc.metadata.get("source")}
        )

        if not sources:
            return {
                "answer": "I cannot verify the source of this information.",
                "sources": []
            }

        # 11. Final response
        return {
            "answer": answer,
            "sources": sources
        }
