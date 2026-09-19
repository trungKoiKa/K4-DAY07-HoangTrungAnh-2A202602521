from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k=top_k)
        if not results:
            return "Không tìm thấy tài liệu phù hợp để trả lời câu hỏi."

        context = []
        for index, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})
            source = metadata.get("source_url") or metadata.get("source") or metadata.get("doc_id")
            context.append(f"[{index}] Nguồn: {source or result.get('id', 'không rõ')}\n{result['content']}")

        context_text = "\n\n".join(context)
        prompt = (
            "Chỉ trả lời dựa trên ngữ cảnh được cung cấp. "
            "Nếu ngữ cảnh không đủ thông tin, hãy nói rõ là không tìm thấy câu trả lời. "
            "Trích dẫn số đoạn [1], [2], ... đã dùng.\n\n"
            f"Ngữ cảnh:\n{context_text}\n\n"
            f"Câu hỏi: {question}\nTrả lời:"
        )
        return self.llm_fn(prompt)
