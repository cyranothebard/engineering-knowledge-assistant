from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Settings:
    root_dir: Path = Path(__file__).resolve().parents[1]
    raw_documents_dir: Path = root_dir / "data" / "raw_documents"
    processed_documents_dir: Path = root_dir / "data" / "processed_documents"
    vector_store_dir: Path = root_dir / "data" / "vector_store"
    usage_metrics_path: Path = root_dir / "data" / "usage_metrics" / "metrics.json"
    chunk_export_path: Path = processed_documents_dir / "chunks.jsonl"
    chunk_size: int = 700
    chunk_overlap: int = 120
    retrieval_k: int = 4
    gap_min_score: float = 0.22
    gap_min_sources: int = 2
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    openai_chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

    @property
    def openai_api_key(self) -> Optional[str]:
        return os.getenv("OPENAI_API_KEY")


def get_settings() -> Settings:
    return Settings()
