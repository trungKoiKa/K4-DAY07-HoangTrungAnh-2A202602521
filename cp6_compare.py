"""Run the same five queries on three available chunking strategies.

The A/B question is run both without and with an audience=student filter for
each strategy. Results include naive doc hits and content-aware retrieval
points; agent answers are outside this script's scope.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from bench import DATA_DIR, read_document, read_group_queries, select_embedder
from benchmark_eval import evaluate_results
from src.chunking import FixedSizeChunker, RecursiveChunker, SentenceChunker
from src.embeddings import EMBEDDING_PROVIDER_ENV
from src.models import Document
from src.store import EmbeddingStore


OUTPUT_FILE = Path("ket_qua_cp6.txt")
STRATEGIES = (
    ("FixedSizeChunker", FixedSizeChunker(chunk_size=500, overlap=50)),
    ("SentenceChunker", SentenceChunker(max_sentences_per_chunk=3)),
    ("RecursiveChunker", RecursiveChunker(chunk_size=500)),
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("mock", "local"), default=os.getenv(EMBEDDING_PROVIDER_ENV, "mock"))
    args = parser.parse_args()
    os.environ[EMBEDDING_PROVIDER_ENV] = args.provider
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    provider, embedder = select_embedder()
    sources = [(path, *read_document(path)) for path in sorted(DATA_DIR.glob("*.md"))]
    questions = read_group_queries()
    lines = [
        f"CP6 backend: {provider} ({getattr(embedder, '_backend_name', provider)})",
        f"Corpus: {len(sources)} documents; top_k=3; same five queries for all strategies.",
        "Retrieval points: 2 = gold at top-1 plus all answer phrases; 1 = gold at top-2/3 plus all phrases; otherwise 0.",
        "Agent answers were not run; retrieval points are not the full rubric score.",
    ]
    if provider == "mock":
        lines.append("MockEmbedder uses MD5-derived vectors: ranks and similarity scores are noise, not semantic quality.")

    for name, chunker in STRATEGIES:
        documents = []
        for path, metadata, body in sources:
            for index, chunk in enumerate(chunker.chunk(body)):
                documents.append(
                    Document(
                        id=f"{path.stem}#{index}",
                        content=chunk,
                        metadata={**metadata, "doc_id": path.stem, "chunk_index": index},
                    )
                )
        store = EmbeddingStore(embedding_fn=embedder)
        store.add_documents(documents)
        lengths = [len(document.content) for document in documents]
        lines.extend(
            [
                "",
                f"=== {name} {vars(chunker)} ===",
                f"Chunks: {len(documents)}; avg_length={sum(lengths) / len(lengths):.1f}; max_length={max(lengths)}",
            ]
        )
        doc_hits = content_hits = points = 0
        for number, query, _, gold_doc_id in questions:
            filters = (None, {"audience": "student"}) if number == 5 else (None,)
            for metadata_filter in filters:
                label = "unfiltered" if metadata_filter is None else "audience=student"
                results = store.search_with_filter(query, top_k=3, metadata_filter=metadata_filter)
                evaluation = evaluate_results(number, gold_doc_id, results)
                lines.append(f"Q{number} [{label}] {query}")
                for rank, result in enumerate(results, 1):
                    lines.append(
                        f"  {rank}. {result['id']} doc_id={result['metadata']['doc_id']} "
                        f"audience={result['metadata']['audience']} score={result['score']:.3f}"
                    )
                    lines.append("     " + " ".join(result["content"].split())[:190])
                lines.append(
                    f"  doc_hit={evaluation['doc_hit']}; gold_rank={evaluation['gold_rank']}; "
                    f"answer_in_context={evaluation['answer_in_context']}; "
                    f"retrieval_points={evaluation['retrieval_points']}/2"
                )
                if evaluation["missing_phrases"]:
                    lines.append("  missing=" + "; ".join(evaluation["missing_phrases"]))
                if metadata_filter is None:
                    doc_hits += int(evaluation["doc_hit"])
                    content_hits += int(evaluation["answer_in_context"])
                    points += evaluation["retrieval_points"]
        lines.append(
            f"SUMMARY {name}: doc_hits={doc_hits}/5; content_hits={content_hits}/5; "
            f"retrieval_points={points}/10 (unfiltered Q1-Q5)"
        )

    OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[0])
    print(f"Saved full top-3 and A/B results to {OUTPUT_FILE}")
    print("\n".join(line for line in lines if line.startswith("SUMMARY ")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
