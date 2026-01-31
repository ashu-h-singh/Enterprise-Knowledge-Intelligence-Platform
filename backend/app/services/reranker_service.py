from sentence_transformers import SentenceTransformer, util


class ReRankerService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def rerank(self, query, docs, top_n=3):
        query_emb = self.model.encode(query, convert_to_tensor=True)
        doc_embs = self.model.encode(
            [d.page_content for d in docs],
            convert_to_tensor=True
        )

        scores = util.cos_sim(query_emb, doc_embs)[0]

        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, _ in ranked[:top_n]]
