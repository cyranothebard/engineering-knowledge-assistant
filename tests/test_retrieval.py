from __future__ import annotations

from app.settings import get_settings
from rag.service import KnowledgeAssistantService


def test_cross_language_retrieval_returns_startup_source() -> None:
    settings = get_settings()
    service = KnowledgeAssistantService(settings)
    service.build_or_load_index(rebuild=True)
    answer = service.ask("Wie starte ich Packaging Line 4?", preferred_language="de")
    titles = [citation.title for citation in answer.citations]
    assert "Packaging Line 4 Startup SOP" in titles
    assert answer.query_language == "de"


def test_knowledge_gap_detected_for_ml_validation_query() -> None:
    settings = get_settings()
    service = KnowledgeAssistantService(settings)
    service.build_or_load_index(rebuild=False)
    answer = service.ask("What is our approved machine learning validation process?", preferred_language="en")
    assert answer.knowledge_gap_detected is True
