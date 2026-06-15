from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Ensure project root is importable when Streamlit launches from any cwd.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from analytics.metrics import UsageMetricsStore
from app.settings import get_settings
from rag.service import KnowledgeAssistantService


st.set_page_config(
    page_title="Engineering Knowledge Assistant — BridgeOps",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Tighter font on metric labels */
    [data-testid="stMetricLabel"] { font-size: 0.75rem; color: #888; }

    /* Confidence badges */
    .badge-high   { background:#d4edda; color:#155724; padding:3px 10px; border-radius:12px; font-size:0.82rem; font-weight:600; }
    .badge-medium { background:#fff3cd; color:#856404; padding:3px 10px; border-radius:12px; font-size:0.82rem; font-weight:600; }
    .badge-low    { background:#f8d7da; color:#721c24; padding:3px 10px; border-radius:12px; font-size:0.82rem; font-weight:600; }
    .badge-gap    { background:#e2e3e5; color:#383d41; padding:3px 10px; border-radius:12px; font-size:0.82rem; font-weight:600; }

    /* Citation cards */
    .citation-card {
        background: #f8f9fa;
        border-left: 3px solid #0d6efd;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 4px;
        font-size: 0.88rem;
    }
    .citation-card .doc-title { font-weight: 600; }
    .citation-card .doc-meta  { color: #6c757d; font-size: 0.80rem; }

    /* Answer box */
    .answer-box {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 16px 20px;
        line-height: 1.65;
        font-size: 0.95rem;
    }

    /* Sidebar header */
    [data-testid="stSidebar"] h2 { font-size: 1rem; margin-bottom: 4px; }

    /* Make primary button stand out more */
    [data-testid="stButton"] button[kind="primary"] {
        background-color: #0d6efd;
        border-radius: 6px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Service singletons ─────────────────────────────────────────────────────────

@st.experimental_singleton
def get_service() -> KnowledgeAssistantService:
    service = KnowledgeAssistantService(get_settings())
    service.build_or_load_index(rebuild=False)
    return service


@st.experimental_singleton
def get_metrics_store() -> UsageMetricsStore:
    return UsageMetricsStore(get_settings().usage_metrics_path)


# ── Helper components ──────────────────────────────────────────────────────────

def _confidence_badge(level: str) -> str:
    cls = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(level, "badge-low")
    return f'<span class="{cls}">{level} confidence</span>'


def _divider() -> None:
    # Streamlit 1.12 compatibility: st.divider was introduced later.
    if hasattr(st, "divider"):
        st.divider()
    else:
        st.markdown("---")


def _toast(message: str) -> None:
    # Streamlit 1.12 compatibility: st.toast was introduced later.
    if hasattr(st, "toast"):
        st.toast(message)
    else:
        st.success(message)


def render_sidebar_metrics(metrics: dict) -> None:
    st.subheader("Usage")
    c1, c2 = st.columns(2)
    c1.metric("Questions", metrics["total_questions"])
    c2.metric("👍 Helpful", metrics["helpful_responses"])

    gap_count = metrics.get("knowledge_gap_count", 0)
    total = max(metrics["total_questions"], 1)
    st.metric("Knowledge Gaps", f"{gap_count} ({gap_count/total*100:.0f}%)")

    top_equipment = metrics.get("top_searched_equipment", {})
    if top_equipment:
        frame = (
            pd.DataFrame(
                [{"Equipment": k, "Queries": v} for k, v in top_equipment.items()]
            )
            .sort_values("Queries", ascending=False)
            .head(6)
        )
        fig = px.bar(
            frame,
            x="Queries",
            y="Equipment",
            orientation="h",
            height=200,
            color_discrete_sequence=["#0d6efd"],
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=24, b=0),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis_title=None,
            xaxis_title=None,
            title=dict(text="Top Equipment", font=dict(size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)


def render_citation_card(citation: object) -> None:
    st.markdown(
        f"""<div class="citation-card">
            <div class="doc-title">📄 {citation.title}</div>
            <div class="doc-meta">{citation.document_type} &nbsp;·&nbsp; <code>{citation.source_reference}</code></div>
        </div>""",
        unsafe_allow_html=True,
    )


# ── Main app ───────────────────────────────────────────────────────────────────

def main() -> None:
    settings = get_settings()
    service = get_service()
    metrics_store = get_metrics_store()

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.image(
            "https://img.shields.io/badge/BridgeOps-Knowledge%20Layer-0d6efd?style=flat-square",
            width=200,
        )
        st.caption(
            "Multilingual RAG over engineering documentation. "
            "Traceable answers with knowledge-gap detection."
        )
        _divider()

        with st.expander("⚙️ System", expanded=False):
            st.write(f"**Documents:** `{settings.raw_documents_dir.name}`")
            st.write(f"**Vector store:** `{settings.vector_store_dir.name}`")
            if st.button("🔄 Rebuild index"):
                with st.spinner("Rebuilding…"):
                    service.build_or_load_index(rebuild=True)
                st.success("Index rebuilt.")

        _divider()
        render_sidebar_metrics(metrics_store.summary())

    # ── Header ─────────────────────────────────────────────────────────────────
    st.title("🔧 Engineering Knowledge Assistant")
    st.caption(
        "Ask in English or German — the assistant retrieves the most relevant "
        "procedures, vendor specs, and RCAs from the BridgeOps knowledge base."
    )

    # ── Sample questions ───────────────────────────────────────────────────────
    with st.expander("💡 Example questions", expanded=False):
        examples = [
            "How do I start Packaging Line 4?",
            "What LED state confirms normal S7-1500 operation?",
            "How do I verify SICK laser sensor accuracy?",
            "What is the SEW coupling alignment tolerance?",
            "Welche Ursachen wurden für Vibrationsalarme dokumentiert?",
            "How do I safely enter the robot cell?",
            "What caused the vision false-reject spike on 2026-03-15?",
            "What cable testing procedure is required for EtherCAT connections?",
        ]
        cols = st.columns(2)
        for i, ex in enumerate(examples):
            if cols[i % 2].button(ex, key=f"ex_{i}"):
                st.session_state["prefill_question"] = ex

    # ── Query input ────────────────────────────────────────────────────────────
    prefill = st.session_state.pop("prefill_question", "")

    col_q, col_lang = st.columns([4, 1])
    with col_q:
        question = st.text_input(
            "Ask an engineering question",
            value=prefill,
            placeholder="e.g. How do I calibrate the laser dimensioning station?",
        )
    with col_lang:
        language_choice = st.selectbox(
            "Language",
            options=["Auto", "English", "Deutsch"],
        )

    search_clicked = st.button("🔍 Search knowledge base")

    # ── Results ────────────────────────────────────────────────────────────────
    if search_clicked and question.strip():
        preferred_language = {"English": "en", "Deutsch": "de"}.get(language_choice)

        with st.spinner("Searching knowledge base…"):
            answer = service.ask(question, preferred_language=preferred_language)

        metrics_store.record_question(question, answer.retrieved_documents)
        if answer.knowledge_gap_detected:
            metrics_store.record_knowledge_gap()

        _divider()

        # Layout: answer + citations side by side
        ans_col, cite_col = st.columns([3, 2])

        with ans_col:
            st.subheader("Answer")

            # Confidence / gap status bar
            if answer.knowledge_gap_detected:
                st.markdown(
                    f'<span class="badge-gap">⚠️ Knowledge gap detected</span> '
                    f'<span style="color:#6c757d;font-size:0.82rem;">{answer.knowledge_gap_reason}</span>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    _confidence_badge(answer.confidence)
                    + f'<span style="color:#6c757d;font-size:0.82rem;margin-left:8px;">score {answer.confidence_score:.2f}</span>',
                    unsafe_allow_html=True,
                )

            st.markdown("")
            st.markdown(
                f'<div class="answer-box">{answer.answer}</div>',
                unsafe_allow_html=True,
            )

            # Feedback
            st.markdown("##### Was this helpful?")
            fb1, fb2, _ = st.columns([1, 1, 3])
            if fb1.button("👍 Yes", key="fb_yes"):
                metrics_store.record_feedback(helpful=True)
                _toast("Thanks for the feedback!")
            if fb2.button("👎 No", key="fb_no"):
                metrics_store.record_feedback(helpful=False)
                _toast("Noted. We'll use this to improve.")

        with cite_col:
            st.subheader("Source Citations")
            for citation in answer.citations:
                render_citation_card(citation)

            if not answer.citations:
                st.info("No citations returned for this query.")

        # Retrieved document metadata (collapsible)
        with st.expander("📊 Retrieved Document Details", expanded=False):
            rows = [doc.model_dump() for doc in answer.retrieved_documents]
            if rows:
                df = pd.DataFrame(rows)
                # Format score as percentage-style float
                if "score" in df.columns:
                    df["score"] = df["score"].map(lambda x: f"{x:.3f}")
                st.dataframe(df, width=None, height=None)
            else:
                st.write("No documents retrieved.")


if __name__ == "__main__":
    main()

