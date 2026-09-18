"""API Schemas."""
from __future__ import annotations
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

class ChatResponse(BaseModel):
    answer: str
    grounded: bool
    citations: list[dict] = []

class BatchRequest(BaseModel):
    questions: list[str] = Field(min_length=1, max_length=20)

class BatchResponse(BaseModel):
    results: list[ChatResponse]

class EvalItem(BaseModel):
    question: str
    expected_answer: str = ""
