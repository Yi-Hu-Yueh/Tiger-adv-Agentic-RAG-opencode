"""FastAPI app — single GET /, middleware, error envelope."""
from __future__ import annotations
import time, uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from core.qdrant_factory import close_qdrant_client
from api.routes.health import router as health_router
from api.routes.chat import router as chat_router
from api.routes.evaluation import router as eval_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_qdrant_client()

app = FastAPI(title="Tiger-adv-Agentic-RAG-opencode", version="1.0.0", lifespan=lifespan)

@app.middleware("http")
async def add_ids(request: Request, call_next):
    rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    t0 = time.time()
    resp = await call_next(request)
    resp.headers["X-Request-ID"] = rid
    resp.headers["X-Execution-Time"] = str(round(time.time() - t0, 3))
    return resp

@app.exception_handler(Exception)
async def internal_handler(request: Request, exc: Exception):
    # Generic message outward; details stay in server log
    print(f"[ERROR] {request.url.path}: {repr(exc)[:500]}")
    return JSONResponse(status_code=500, content={"success": False, "error": "INTERNAL_ERROR", "message": "internal error"})

app.include_router(health_router, tags=["health"])
app.include_router(chat_router, tags=["chat"])
app.include_router(eval_router, tags=["evaluation"])

@app.get("/", include_in_schema=False)
def root():
    return {"service": "Tiger-adv-Agentic-RAG-opencode", "docs": "/docs", "health": "/health"}
