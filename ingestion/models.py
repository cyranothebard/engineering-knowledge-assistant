from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class DocumentMetadata(BaseModel):
    document_id: str = Field(min_length=3)
    title: str = Field(min_length=3)
    document_type: str = Field(min_length=2)
    department: str = Field(min_length=2)
    equipment: str = Field(min_length=2)
    process: str = Field(min_length=2)
    site: str = Field(min_length=2)
    language: str = Field(pattern="^(en|de)$")
    revision: str = Field(min_length=1)
    criticality: str = Field(pattern="^(Low|Medium|High)$")
    author: str = Field(min_length=2)
    created_date: date
    filename: str = Field(min_length=3)

    @field_validator(
        "document_id",
        "title",
        "document_type",
        "department",
        "equipment",
        "process",
        "site",
        "revision",
        "criticality",
        "author",
        "filename",
    )
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Field cannot be blank")
        return normalized


class ChunkRecord(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    document_type: str
    equipment: str
    language: str
    score_hint: Optional[float] = None
    content: str
    source_reference: str
