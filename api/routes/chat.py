"""POST /chat, /chat/batch, /chat/stream."""
from __future__ import annotations
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.schemas import ChatRequest, ChatResponse, BatchRequest, BatchResponse
from api.dependencies import get_workflow

router = APIRouter()

def _to_resp(state) -> ChatResponse:
    return ChatResponse(answer=state.answer, grounded=bool(state.grounded), citations=state.citations)

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    wf = get_workflow()
    state = wf.run(req.question)
    return _to_resp(state)

@router.post("/chat/batch", response_model=BatchResponse)
def chat_batch(req: BatchRequest):
    wf = get_workflow()
    return BatchResponse(results=[_to_resp(wf.run(q)) for q in req.questions])

@router.post("/chat/stream")
def chat_stream(req: ChatRequest):
    wf = get_workflow()
    state = wf.run(req.question)
    answer = state.answer or ""
    # Chunked HTTP streaming of final answer (documented: not token-by-token LLM streaming)
    def gen():
        for i in range(0, len(answer), 200):
            yield answer[i:i+200]
    return StreamingResponse(gen(), media_type="text/plain")
