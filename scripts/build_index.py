"""Build / update a Qdrant collection from local documents.

Pipeline: scan -> split -> embed (Ollama bge-m3) -> upsert (Qdrant).
Payload contract (must match core/providers/qdrant_retriever.py):
  repo, source, relative_path, filename, extension, chunk_index, text

Usage:
  python scripts/build_index.py --source data/my_docs --collection my_docs --repo my_docs
  python scripts/build_index.py --source data/my_docs --collection enterprise_rag --repo my_docs --append
"""
from __future__ import annotations
import argparse
import json
import pathlib
import sys
import uuid

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.http.models import Distance, VectorParams

from core.config import SETTINGS
from core.qdrant_factory import get_qdrant_client
from core.providers.ollama_embedder import OllamaEmbedder

SUPPORTED = {".md", ".mdx", ".txt", ".py", ".ipynb", ".json", ".yaml", ".yml"}


def iter_files(source: pathlib.Path):
    for p in sorted(source.rglob("*")):
        if p.is_file() and p.suffix.lower() in SUPPORTED:
            yield p


def read_text(p: pathlib.Path) -> str:
    if p.suffix.lower() == ".ipynb":
        try:
            nb = json.loads(p.read_text(encoding="utf-8"))
            parts = []
            for cell in nb.get("cells", []):
                src = cell.get("source", "")
                parts.append("".join(src) if isinstance(src, list) else str(src))
            return "\n\n".join(parts)
        except Exception:
            return ""
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="local docs folder")
    ap.add_argument("--collection", default=SETTINGS.collection)
    ap.add_argument("--repo", default="custom")
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--chunk-size", type=int, default=1000)
    ap.add_argument("--chunk-overlap", type=int, default=200)
    ap.add_argument("--append", action="store_true", help="keep existing collection; default recreates when absent only")
    ap.add_argument("--recreate", action="store_true", help="drop and recreate collection first")
    a = ap.parse_args()

    src = pathlib.Path(a.source)
    if not src.is_dir():
        raise SystemExit(f"source not found: {src}")

    client = get_qdrant_client()
    if a.recreate and client.collection_exists(a.collection):
        client.delete_collection(a.collection)
        print(f"deleted collection {a.collection}")
    if not client.collection_exists(a.collection):
        client.create_collection(
            a.collection,
            vectors_config=VectorParams(size=SETTINGS.vector_size, distance=Distance.COSINE),
        )
        print(f"created collection {a.collection} (size={SETTINGS.vector_size}, COSINE)")
    elif not a.append and not a.recreate:
        print(f"collection {a.collection} exists; appending (use --recreate to rebuild)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=a.chunk_size, chunk_overlap=a.chunk_overlap
    )
    embedder = OllamaEmbedder()

    files = list(iter_files(src))
    print(f"files: {len(files)}")
    batch_points: list[dict] = []
    total = 0

    def flush():
        nonlocal batch_points, total
        if not batch_points:
            return
        texts = [p["payload"]["text"] for p in batch_points]
        vecs = embedder.embed_documents(texts)
        for p, v in zip(batch_points, vecs):
            p["vector"] = v
        client.upsert(a.collection, points=batch_points, wait=True)
        total += len(batch_points)
        print(f"upserted {total}")
        batch_points = []

    for f in files:
        text = read_text(f)
        if not text.strip():
            continue
        try:
            rel = str(f.relative_to(src))
        except ValueError:
            rel = f.name
        for idx, chunk in enumerate(splitter.split_text(text)):
            batch_points.append(
                {
                    "id": str(uuid.uuid4()),
                    "payload": {
                        "repo": a.repo,
                        "source": str(f),
                        "relative_path": rel,
                        "filename": f.name,
                        "extension": f.suffix.lower(),
                        "chunk_index": idx,
                        "text": chunk,
                    },
                }
            )
            if len(batch_points) >= a.batch_size:
                flush()
    flush()

    count = client.count(a.collection, exact=True).count
    print(f"COLLECTION: {a.collection} POINTS={count} CHUNKS_ADDED={total} STATUS: PASS")


if __name__ == "__main__":
    main()
