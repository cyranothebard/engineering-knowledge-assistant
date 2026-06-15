from __future__ import annotations

from analytics.metrics import UsageMetricsStore


def test_metrics_store_updates_counts(tmp_path) -> None:
    store = UsageMetricsStore(tmp_path / "metrics.json")
    store.record_question(
        question="How do I start Packaging Line 4?",
        retrieved_documents=[{"equipment": "Packaging Line 4"}, {"equipment": "Vision Inspection Cell"}],
    )
    store.record_feedback(helpful=True)
    summary = store.summary()
    assert summary["total_questions"] == 1
    assert summary["helpful_responses"] == 1
    assert summary["top_searched_equipment"]["Packaging Line 4"] == 1
