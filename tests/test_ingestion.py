from __future__ import annotations

from app.settings import get_settings
from ingestion.loaders import load_documents
from ingestion.pipeline import build_chunks


def test_manifest_loads_documents() -> None:
    settings = get_settings()
    documents = load_documents(settings.raw_documents_dir)
    assert len(documents) >= 10
    assert all("document_id" in document.metadata for document in documents)


def test_chunk_builder_exports_chunks() -> None:
    settings = get_settings()
    chunks = build_chunks(settings)
    assert len(chunks) >= len(load_documents(settings.raw_documents_dir))
    assert settings.chunk_export_path.exists()
