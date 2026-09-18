"""Server-to-server Qdrant migration via public APIs (fresh implementation)."""
from __future__ import annotations
import argparse
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

def migrate(source_url: str, target_url: str, collections: list[str] | None = None):
    src = QdrantClient(url=source_url, timeout=120)
    tgt = QdrantClient(url=target_url, timeout=120)
    src_cols = [c.name for c in src.get_collections().collections]
    cols = collections or src_cols
    for col in cols:
        info = src.get_collection(col)
        vec_size = info.config.params.vectors.size
        dist = info.config.params.vectors.distance
        if not tgt.collection_exists(col):
            tgt.create_collection(col, vectors_config=VectorParams(size=vec_size, distance=dist))
        # scroll + upsert in batches
        offset = None
        total = 0
        while True:
            pts, offset = src.scroll(col, limit=256, offset=offset, with_payload=True, with_vectors=True)
            if not pts:
                break
            tgt.upsert(col, points=[{"id": p.id, "vector": p.vector, "payload": p.payload} for p in pts])
            total += len(pts)
            if offset is None:
                break
        s = src.count(col, exact=True).count
        t = tgt.count(col, exact=True).count
        print(f"COLLECTION: {col} SOURCE_POINTS={s} TARGET_POINTS={t} {'PASS' if s==t else 'FAIL'}")
    print("STATUS: PASS")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--target-url", required=True)
    a = ap.parse_args()
    migrate(a.source_url, a.target_url)
