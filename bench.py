"""Run the group's five benchmark questions on one chunking strategy.

All members should use the same corpus, questions, embedding backend and top-k.
Change only CHUNKER to compare individual strategies fairly.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv

from src.chunking import FixedSizeChunker, RecursiveChunker, SentenceChunker  # alternative strategies
from src.embeddings import EMBEDDING_PROVIDER_ENV, LocalEmbedder, MockEmbedder
from src.models import Document
from src.store import EmbeddingStore


DATA_DIR = Path("data/university_services")
GROUP_REPORT = Path("report/REPORT_NHOM.md")
OUTPUT_FILE = Path("ket_qua_benchmark.txt")
FILTER_QUERY_NUMBER = 5

# R3's strategy. Other members change this line to their own chunker.
CHUNKER = SentenceChunker(max_sentences_per_chunk=3)


def read_document(path: Path) -> tuple[dict[str, str], str]:
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.startswith("---"):
        raise ValueError(f"Missing YAML frontmatter: {path}")
    parts = raw.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Unclosed YAML frontmatter: {path}")

    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith('"'):
            value = json.loads(value)
        else:
            value = value.split(" #", 1)[0].strip()
        metadata[key.strip()] = value

    if metadata.get("doc_id") != path.stem or not metadata.get("audience"):
        raise ValueError(f"Invalid doc_id or audience metadata: {path}")
    return metadata, parts[2].strip()


def read_group_queries() -> list[tuple[int, str, str, str]]:
    """Use the five questions and gold references already in REPORT_NHOM.md."""
    report = GROUP_REPORT.read_text(encoding="utf-8")
    heading = "### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)"
    next_heading = "### Tổng hợp chất lượng truy xuất của nhóm"
    if heading not in report or next_heading not in report:
        raise ValueError("Benchmark question table is missing from REPORT_NHOM.md")
    section = report.split(heading, 1)[1].split(next_heading, 1)[0]

    questions = []
    for line in section.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        columns = [column.strip() for column in line.strip().strip("|").split("|")]
        if len(columns) != 4:
            raise ValueError(f"Expected four columns in benchmark row: {line}")
        number, query, gold_answer, gold_doc_id = columns
        questions.append((int(number), query, gold_answer, gold_doc_id.strip("` ")))

    if [number for number, *_ in questions] != [1, 2, 3, 4, 5]:
        raise ValueError("REPORT_NHOM.md must contain exactly five numbered queries")
    return questions


def select_embedder() -> tuple[str, Callable[[str], list[float]]]:
    load_dotenv(override=False)
    provider = os.getenv(EMBEDDING_PROVIDER_ENV, "mock").strip().lower()
    if provider == "mock":
        return provider, MockEmbedder()
    if provider == "local":
        return provider, LocalEmbedder()
    raise ValueError("bench.py supports EMBEDDING_PROVIDER=mock or local")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    paths = sorted(DATA_DIR.glob("*.md"))
    if not 5 <= len(paths) <= 10:
        raise ValueError(f"Expected 5-10 Markdown documents in {DATA_DIR}, found {len(paths)}")
    questions = read_group_queries()

    documents: list[Document] = []
    for path in paths:
        metadata, body = read_document(path)
        for index, chunk in enumerate(CHUNKER.chunk(body)):
            documents.append(
                Document(
                    id=f"{path.stem}#{index}",
                    content=chunk,
                    metadata={**metadata, "doc_id": path.stem, "chunk_index": index},
                )
            )

    provider, embedder = select_embedder()
    store = EmbeddingStore(embedding_fn=embedder)
    store.add_documents(documents)

    lines = [
        f"Strategy: {CHUNKER.__class__.__name__} {vars(CHUNKER)}",
        f"Embedding provider: {provider}",
        f"Loaded {store.get_collection_size()} chunks from {len(paths)} documents.",
    ]
    if provider == "mock":
        lines.append("Mock scores do not represent semantic retrieval quality.")

    for number, query, gold_answer, gold_doc_id in questions:
        filters = [None, {"audience": "student"}] if number == FILTER_QUERY_NUMBER else [None]
        for metadata_filter in filters:
            lines.extend(
                [
                    "",
                    f"Q{number}: {query}",
                    f"Gold answer: {gold_answer}",
                    f"Gold doc_id: {gold_doc_id}; metadata_filter={metadata_filter}",
                ]
            )
            results = store.search_with_filter(query, top_k=3, metadata_filter=metadata_filter)
            for rank, result in enumerate(results, start=1):
                excerpt = " ".join(result["content"].split())[:240]
                lines.append(
                    f"  Top-{rank}: score={result['score']:.3f}; "
                    f"doc_id={result['metadata']['doc_id']}; "
                    f"chunk={result['id']}; audience={result['metadata'].get('audience')}"
                )
                lines.append(f"    {excerpt}")

    output = "\n".join(lines) + "\n"
    OUTPUT_FILE.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
