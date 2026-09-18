"""Composition root — builds the active GraphWorkflow."""
from __future__ import annotations
from core.config import SETTINGS
from core.qdrant_factory import get_qdrant_client
from core.providers.ollama_chat import OllamaChat
from core.providers.ollama_embedder import OllamaEmbedder
from core.providers.bge_reranker import BGEReranker
from core.providers.qdrant_retriever import QdrantRetriever
from core.agents.agents import (
    QueryGenerator, QueryRewriter, DocumentGrader,
    AnswerGenerator, HallucinationChecker, CitationGenerator, ReflectionAgent,
)
from core.agents.multi_agent import PlannerAgent, ResearcherAgent, WriterAgent, ReviewerAgent, VerifierAgent
from core.retrievers.retriever_pipeline import RetrieverPipeline
from core.graph.nodes import GraphNodes
from core.graph.router import GraphRouter
from core.graph.workflow import GraphWorkflow

def build_workflow() -> GraphWorkflow:
    client = get_qdrant_client()
    chat = OllamaChat()
    embedder = OllamaEmbedder()
    retriever = QdrantRetriever(client, embedder)
    pipeline = RetrieverPipeline(QueryGenerator(chat), retriever, BGEReranker())
    nodes = GraphNodes(
        pipeline=pipeline,
        rewriter=QueryRewriter(chat),
        grader=DocumentGrader(chat),
        generator=AnswerGenerator(chat),
        checker=HallucinationChecker(chat),
        citation_gen=CitationGenerator(),
        reflector=ReflectionAgent(chat),
        planner=PlannerAgent(),
        agents={
            "researcher": ResearcherAgent(),
            "writer": WriterAgent(),
            "reviewer": ReviewerAgent(),
            "verifier": VerifierAgent(),
        },
    )
    return GraphWorkflow(nodes, GraphRouter())
