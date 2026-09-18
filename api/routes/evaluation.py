"""Evaluation: run + dashboard + history/report persistence."""
from __future__ import annotations
import json, time, pathlib
from fastapi import APIRouter
from api.schemas import EvalItem
from api.dependencies import get_workflow

router = APIRouter()
HIST = pathlib.Path("evaluation/history")
REPS = pathlib.Path("evaluation/reports")

def _score(expected: str, predicted: str) -> float:
    e, p = expected.lower().split(), predicted.lower().split()
    if not e or not p:
        return 0.0
    overlap = len(set(e) & set(p))
    return round(overlap / max(len(set(e)), 1), 3)

@router.post("/evaluation/run")
def run_eval(dataset_name: str = "default", items: list[EvalItem] = []):
    wf = get_workflow()
    results = []
    for it in items:
        st = wf.run(it.question)
        results.append({
            "question": it.question,
            "expected_answer": it.expected_answer,
            "predicted_answer": st.answer,
            "grounded": st.grounded,
            "citations": st.citations,
            "score": _score(it.expected_answer, st.answer),
        })
    # Aggregate over ALL rows (fixes results[0]-only bug)
    scores = [r["score"] for r in results] or [0.0]
    metrics = {
        "count": len(results),
        "avg_score": round(sum(scores) / len(scores), 3),
        "grounded_rate": round(sum(1 for r in results if r["grounded"]) / max(len(results), 1), 3),
    }
    ts = int(time.time())
    HIST.mkdir(parents=True, exist_ok=True)
    REPS.mkdir(parents=True, exist_ok=True)
    (HIST / f"{dataset_name}-{ts}.json").write_text(json.dumps({"metrics": metrics, "results": results}, ensure_ascii=False), encoding="utf-8")
    (REPS / f"{dataset_name}-{ts}.html").write_text(f"<html><body><h1>{dataset_name}</h1><p>{metrics}</p></body></html>", encoding="utf-8")
    return {"dataset": dataset_name, "metrics": metrics, "results": results}

@router.get("/evaluation/dashboard")
def dashboard():
    HIST.mkdir(parents=True, exist_ok=True)
    datasets = []
    for f in sorted(HIST.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            datasets.append({"name": f.stem, "history_count": 1, "latest_report": str(f), "latest_metrics": d.get("metrics", {})})
        except Exception:
            continue
    return {"datasets": datasets}
