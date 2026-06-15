from __future__ import annotations

import json
import re
from typing import Literal, Optional, Union

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from analytics.metrics import UsageMetricsStore
from app.settings import Settings
from ingestion.pipeline import build_chunks
from rag.retrieval import RetrievalEngine, RetrievalResult


class Citation(BaseModel):
    title: str
    document_type: str
    source_reference: str


class RetrievedDocument(BaseModel):
    title: str
    document_type: str
    equipment: str
    language: str
    source_reference: str
    score: float


class AnswerPackage(BaseModel):
    answer: str
    confidence: Literal["High", "Medium", "Low"]
    confidence_score: float
    query_language: Literal["en", "de"]
    knowledge_gap_detected: bool
    knowledge_gap_reason: Optional[str] = None
    citations: list[Citation]
    retrieved_documents: list[RetrievedDocument]


class KnowledgeAssistantService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.retrieval_engine = RetrievalEngine(settings)
        self.metrics_store = UsageMetricsStore(settings.usage_metrics_path)

    def build_or_load_index(self, rebuild: bool = False) -> dict[str, Union[int, str]]:
        if self.retrieval_engine.has_index() and not rebuild:
            return {
                "collection_name": "engineering_knowledge",
                "chunks_indexed": self._indexed_chunk_count(),
                "persist_directory": str(self.settings.vector_store_dir),
            }

        chunks = build_chunks(self.settings)
        return self.retrieval_engine.build_store(chunks, rebuild=True)

    def ask(self, question: str, preferred_language: Optional[str] = None) -> AnswerPackage:
        question = question.strip()
        query_language = preferred_language or self._detect_language(question)
        results = self.retrieval_engine.search(question)
        knowledge_gap_detected, gap_reason = self._assess_gap(question, results)
        answer = self._generate_answer(question, query_language, results, knowledge_gap_detected)
        citations = self._build_citations(results)
        retrieved_documents = self._build_retrieved_documents(results)
        confidence_score = results[0].score if results else 0.0
        package = AnswerPackage(
            answer=answer,
            confidence=self._confidence_label(confidence_score, len(results)),
            confidence_score=round(confidence_score, 3),
            query_language=query_language,
            knowledge_gap_detected=knowledge_gap_detected,
            knowledge_gap_reason=gap_reason,
            citations=citations,
            retrieved_documents=retrieved_documents,
        )
        self.metrics_store.record_question(question=question, retrieved_documents=[doc.model_dump() for doc in retrieved_documents])
        return package

    def _indexed_chunk_count(self) -> int:
        if not self.settings.chunk_export_path.exists():
            return 0
        return sum(1 for _ in self.settings.chunk_export_path.open("r", encoding="utf-8"))

    def _detect_language(self, question: str) -> Literal["en", "de"]:
        normalized = question.lower()
        german_markers = ["welche", "wie", "warum", "dokumentiert", "genehmigt", "verfahren", "für", "wurden"]
        if any(marker in normalized for marker in german_markers) or any(char in normalized for char in "äöüß"):
            return "de"
        return "en"

    def _assess_gap(self, question: str, results: list[RetrievalResult]) -> tuple[bool, Optional[str]]:
        if len(results) < self.settings.gap_min_sources:
            return True, "Insufficient relevant documents retrieved"
        if results[0].score < self.settings.gap_min_score:
            return True, "Top retrieval score below confidence threshold"
        if self._content_coverage_ratio(question, results) < 0.34:
            return True, "Retrieved documents do not sufficiently cover the core query terms"
        return False, None

    def _content_coverage_ratio(self, question: str, results: list[RetrievalResult]) -> float:
        stopwords = {
            "what",
            "which",
            "how",
            "why",
            "our",
            "the",
            "and",
            "for",
            "with",
            "approved",
            "process",
            "welche",
            "wie",
            "warum",
            "wurden",
            "ist",
            "der",
            "die",
            "das",
            "und",
            "fuer",
            "verfahren",
        }
        tokens = {
            token
            for token in re.findall(r"[a-zA-Z0-9äöüß]+", question.lower())
            if len(token) >= 5 and token not in stopwords
        }
        if not tokens or not results:
            return 1.0

        combined_content = " ".join(
            f"{result.metadata['title']} {result.content}".lower() for result in results[:2]
        )
        matched = sum(1 for token in tokens if token in combined_content)
        return matched / len(tokens)

    def _build_citations(self, results: list[RetrievalResult]) -> list[Citation]:
        citations: list[Citation] = []
        seen: set[str] = set()
        for result in results:
            key = result.metadata["document_id"]
            if key in seen:
                continue
            seen.add(key)
            citations.append(
                Citation(
                    title=result.metadata["title"],
                    document_type=result.metadata["document_type"],
                    source_reference=result.metadata["source_reference"],
                )
            )
        return citations

    def _build_retrieved_documents(self, results: list[RetrievalResult]) -> list[RetrievedDocument]:
        documents: list[RetrievedDocument] = []
        seen: set[str] = set()
        for result in results:
            key = result.metadata["document_id"]
            if key in seen:
                continue
            seen.add(key)
            documents.append(
                RetrievedDocument(
                    title=result.metadata["title"],
                    document_type=result.metadata["document_type"],
                    equipment=result.metadata["equipment"],
                    language=result.metadata["language"],
                    source_reference=result.metadata["source_reference"],
                    score=round(result.score, 3),
                )
            )
        return documents

    def _generate_answer(
        self,
        question: str,
        query_language: Literal["en", "de"],
        results: list[RetrievalResult],
        knowledge_gap_detected: bool,
    ) -> str:
        if not results:
            return self._gap_only_response(query_language)

        if self.settings.openai_api_key:
            return self._generate_llm_answer(question, query_language, results, knowledge_gap_detected)
        return self._generate_extractive_answer(query_language, results, knowledge_gap_detected)

    def _generate_llm_answer(
        self,
        question: str,
        query_language: Literal["en", "de"],
        results: list[RetrievalResult],
        knowledge_gap_detected: bool,
    ) -> str:
        llm = ChatOpenAI(model=self.settings.openai_chat_model, temperature=0)
        context = [
            {
                "title": result.metadata["title"],
                "document_type": result.metadata["document_type"],
                "source_reference": result.metadata["source_reference"],
                "content": result.content[:1800],
                "score": result.score,
            }
            for result in results
        ]
        instructions = {
            "en": "Answer in English. Be concise, operational, and factual.",
            "de": "Antworte auf Deutsch. Formuliere knapp, operativ und sachlich.",
        }[query_language]
        gap_line = "Potential Knowledge Gap Detected." if knowledge_gap_detected else ""
        prompt = (
            f"{instructions}\n"
            "Use only the retrieved context. If the documents are weak or incomplete, say so directly.\n"
            f"Question: {question}\n"
            f"Retrieved context: {json.dumps(context, ensure_ascii=False)}\n"
            f"{gap_line}"
        )
        response = llm.invoke(prompt)
        return str(response.content).strip()

    def _generate_extractive_answer(
        self,
        query_language: Literal["en", "de"],
        results: list[RetrievalResult],
        knowledge_gap_detected: bool,
    ) -> str:
        top_documents = []
        for result in results[:2]:
            snippet = result.content.split("\n\n", 1)[-1][:420].strip()
            snippet = " ".join(snippet.split())
            top_documents.append((result.metadata["title"], snippet))

        if query_language == "de":
            lines = ["Zusammenfassung aus den relevantesten Dokumenten:"]
            for title, snippet in top_documents:
                lines.append(f"- {title}: {snippet}")
            if knowledge_gap_detected:
                lines.append("Potential Knowledge Gap Detected: Die verfügbare Dokumentation ist unvollständig oder nur schwach relevant.")
            return "\n".join(lines)

        lines = ["Summary from the most relevant documents:"]
        for title, snippet in top_documents:
            lines.append(f"- {title}: {snippet}")
        if knowledge_gap_detected:
            lines.append("Potential Knowledge Gap Detected: available documentation appears incomplete or weakly relevant.")
        return "\n".join(lines)

    def _gap_only_response(self, query_language: Literal["en", "de"]) -> str:
        if query_language == "de":
            return "Potential Knowledge Gap Detected: Für diese Frage wurde keine ausreichend relevante, genehmigte Dokumentation gefunden."
        return "Potential Knowledge Gap Detected: no sufficiently relevant approved documentation was found for this question."

    def _confidence_label(self, score: float, result_count: int) -> Literal["High", "Medium", "Low"]:
        if score >= 0.5 and result_count >= 3:
            return "High"
        if score >= 0.25 and result_count >= 2:
            return "Medium"
        return "Low"
