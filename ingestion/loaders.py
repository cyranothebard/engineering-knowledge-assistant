from __future__ import annotations

import json
from pathlib import Path

from langchain_core.documents import Document
from pypdf import PdfReader

from ingestion.models import DocumentMetadata


def _read_pdf_text(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _read_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        return _read_pdf_text(file_path)
    return file_path.read_text(encoding="utf-8").strip()


def _load_manifest(raw_documents_dir: Path) -> list[DocumentMetadata]:
    manifest_path = raw_documents_dir / "manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [DocumentMetadata(**entry) for entry in payload]


def load_documents(raw_documents_dir: Path) -> list[Document]:
    documents: list[Document] = []
    for metadata in _load_manifest(raw_documents_dir):
        file_path = raw_documents_dir / metadata.filename
        content = _read_text(file_path)
        documents.append(
            Document(
                page_content=content,
                metadata={
                    **metadata.model_dump(mode="json"),
                    "source_reference": metadata.filename,
                },
            )
        )
    return documents
