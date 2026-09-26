import numpy as np
import faiss
from google import genai
from google.genai import types

class GeminiVectorStore:
    def __init__(self, api_key: str, embedding_model: str = "gemini-embedding-001", dimension: int = 768):
        self.client = genai.Client(api_key=api_key)
        self.embedding_model = embedding_model
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.records: list[dict] = []

    def _embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dimension), dtype="float32")
        result = self.client.models.embed_content(
            model=self.embedding_model,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=self.dimension,
            ),
        )
        vectors = np.array([e.values for e in result.embeddings], dtype="float32")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        vectors = vectors / np.clip(norms, 1e-12, None)
        return vectors

    def add(self, records: list[dict]) -> None:
        if not records:
            return
        vectors = self._embed([r["text"] for r in records])
        self.index.add(vectors)
        self.records.extend(records)

    def search(self, query: str, k: int = 6) -> list[dict]:
        if not self.records:
            return []
        result = self.client.models.embed_content(
            model=self.embedding_model,
            contents=[query],
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=self.dimension,
            ),
        )
        q = np.array([result.embeddings[0].values], dtype="float32")
        q /= np.clip(np.linalg.norm(q, axis=1, keepdims=True), 1e-12, None)
        scores, ids = self.index.search(q, min(k, len(self.records)))
        hits = []
        for score, idx in zip(scores[0], ids[0]):
            if idx >= 0:
                item = dict(self.records[idx])
                item["semantic_score"] = float(score)
                hits.append(item)
        return hits

    def hybrid_search(self, query: str, k: int = 6) -> list[dict]:
        semantic = self.search(query, max(k, 8))
        terms = {t.lower() for t in query.split() if len(t) > 2}
        for item in semantic:
            low = item["text"].lower()
            overlap = sum(1 for t in terms if t in low) / max(1, len(terms))
            item["keyword_score"] = overlap
            item["hybrid_score"] = 0.8 * item["semantic_score"] + 0.2 * overlap
        return sorted(semantic, key=lambda x: x["hybrid_score"], reverse=True)[:k]

    def context(self, query: str, k: int = 6) -> str:
        hits = self.hybrid_search(query, k)
        if not hits:
            return "NO UPLOADED SOURCE MATCHES."
        blocks = []
        for h in hits:
            loc = f"page {h['page']}" if h.get("page") else "document"
            blocks.append(f"SOURCE: {h['source']} | {loc}\n{h['text']}")
        return "\n\n---\n\n".join(blocks)
