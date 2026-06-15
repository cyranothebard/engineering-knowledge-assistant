from __future__ import annotations

import math
import shutil
from dataclasses import dataclass
from typing import Union

from langchain_chroma import Chroma

from app.settings import Settings
from rag.embeddings import get_embedding_backend

QUERY_EXPANSIONS = {
    "vibrationsalarme": "vibration alarms bearing wear unbalance",
    "vibration": "vibrationsalarm vibration alarms",
    "welche": "which what",
    "ursachen": "causes reasons root cause",
    "dokumentiert": "documented recorded incident report",
    "start": "startup start-up procedure anfahren",
    "anfahren": "startup start",
    "abschalten": "shutdown stop",
    "netzwerk": "network industrial ethernet",
    "vision": "inspection camera false reject",
    "laser": "dimensioning calibration communication sensor",
    "genehmigt": "approved validated",
    "validierung": "validation governance machine learning",
    "wissensluecke": "knowledge gap missing documentation",
}


@dataclass
class RetrievalResult:
    score: float
    content: str
    metadata: dict


def expand_multilingual_query(query: str) -> str:
    expanded_terms = [query]
    normalized = query.lower()
    for term, expansion in QUERY_EXPANSIONS.items():
        if term in normalized:
            expanded_terms.append(expansion)
    return " ".join(expanded_terms)


class RetrievalEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.embeddings = get_embedding_backend(settings)

    def has_index(self) -> bool:
        return self.settings.vector_store_dir.exists() and any(self.settings.vector_store_dir.iterdir())

    def build_store(self, chunks: list, rebuild: bool = False) -> dict[str, Union[int, str]]:
        if rebuild and self.settings.vector_store_dir.exists():
            shutil.rmtree(self.settings.vector_store_dir)

        self.settings.vector_store_dir.mkdir(parents=True, exist_ok=True)
        Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            collection_name="engineering_knowledge",
            persist_directory=str(self.settings.vector_store_dir),
        )
        return {
            "collection_name": "engineering_knowledge",
            "chunks_indexed": len(chunks),
            "persist_directory": str(self.settings.vector_store_dir),
        }

    def search(self, query: str) -> list[RetrievalResult]:
        vector_store = Chroma(
            collection_name="engineering_knowledge",
            persist_directory=str(self.settings.vector_store_dir),
            embedding_function=self.embeddings,
        )
        expanded_query = expand_multilingual_query(query)
        matches = vector_store.similarity_search_with_score(
            expanded_query,
            k=self.settings.retrieval_k,
        )
        results: list[RetrievalResult] = []
        for document, score in matches:
            distance = max(0.0, float(score))
            bounded_score = 1.0 / (1.0 + math.sqrt(distance))
            results.append(
                RetrievalResult(
                    score=bounded_score,
                    content=document.page_content,
                    metadata=document.metadata,
                )
            )
        return results
