from __future__ import annotations

import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.settings import Settings
from ingestion.loaders import load_documents

TRANSLATION_HINTS = {
    "vibrationsalarm": "vibration alarm bearing wear",
    "ursachen": "causes root cause reasons",
    "welche": "which what",
    "start": "startup start-up anfahren",
    "anfahren": "startup start",
    "abschalten": "shutdown stop",
    "qualitaet": "quality inspection false reject",
    "netzwerk": "network latency ethernet communication",
    "sperren": "lockout tagout loto safety isolation",
    "wartung": "maintenance preventive procedure",
    "vision": "camera inspection false reject",
    "laser": "dimensioning calibration sensor",
}


def _augment_content(document: Document) -> str:
    metadata = document.metadata
    normalized = document.page_content.lower()
    dynamic_hints = []
    for term, synonyms in TRANSLATION_HINTS.items():
        if term in normalized or term in metadata["title"].lower():
            dynamic_hints.append(synonyms)

    metadata_block = (
        f"Title: {metadata['title']}\n"
        f"Document type: {metadata['document_type']}\n"
        f"Department: {metadata['department']}\n"
        f"Equipment: {metadata['equipment']}\n"
        f"Process: {metadata['process']}\n"
        f"Site: {metadata['site']}\n"
        f"Language: {metadata['language']}\n"
        f"Criticality: {metadata['criticality']}\n"
        f"Aliases: {' '.join(dynamic_hints)}\n\n"
    )
    return metadata_block + document.page_content


def build_chunks(settings: Settings) -> list[Document]:
    settings.processed_documents_dir.mkdir(parents=True, exist_ok=True)
    documents = load_documents(settings.raw_documents_dir)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    chunks: list[Document] = []
    chunk_exports: list[dict[str, object]] = []

    for document in documents:
        enriched = Document(
            page_content=_augment_content(document),
            metadata=document.metadata,
        )
        split_docs = splitter.split_documents([enriched])
        for index, chunk in enumerate(split_docs, start=1):
            chunk_id = f"{chunk.metadata['document_id']}-chunk-{index:02d}"
            chunk.metadata = {
                **chunk.metadata,
                "chunk_id": chunk_id,
            }
            chunks.append(chunk)
            chunk_exports.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": chunk.metadata["document_id"],
                    "title": chunk.metadata["title"],
                    "document_type": chunk.metadata["document_type"],
                    "equipment": chunk.metadata["equipment"],
                    "language": chunk.metadata["language"],
                    "source_reference": chunk.metadata["source_reference"],
                    "content": chunk.page_content,
                }
            )

    with settings.chunk_export_path.open("w", encoding="utf-8") as handle:
        for record in chunk_exports:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    return chunks
