from __future__ import annotations

import json
from pathlib import Path


class UsageMetricsStore:
    def __init__(self, metrics_path: Path) -> None:
        self.metrics_path = metrics_path
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.metrics_path.exists():
            self._write(
                {
                    "total_questions": 0,
                    "helpful_responses": 0,
                    "unhelpful_responses": 0,
                    "knowledge_gap_count": 0,
                    "top_searched_equipment": {},
                }
            )

    def load(self) -> dict:
        return json.loads(self.metrics_path.read_text(encoding="utf-8"))

    def record_question(self, question: str, retrieved_documents: list) -> None:
        metrics = self.load()
        metrics["total_questions"] += 1
        # Support both Pydantic model instances and plain dicts
        equipments = set()
        for document in retrieved_documents:
            eq = document.get("equipment") if isinstance(document, dict) else getattr(document, "equipment", None)
            if eq:
                equipments.add(eq)
        for equipment in equipments:
            current = metrics["top_searched_equipment"].get(equipment, 0)
            metrics["top_searched_equipment"][equipment] = current + 1
        self._write(metrics)

    def record_knowledge_gap(self) -> None:
        metrics = self.load()
        metrics.setdefault("knowledge_gap_count", 0)
        metrics["knowledge_gap_count"] += 1
        self._write(metrics)

    def record_feedback(self, helpful: bool) -> None:
        metrics = self.load()
        key = "helpful_responses" if helpful else "unhelpful_responses"
        metrics[key] += 1
        self._write(metrics)

    def summary(self) -> dict:
        data = self.load()
        data.setdefault("knowledge_gap_count", 0)
        return data

    def _write(self, payload: dict) -> None:
        self.metrics_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
