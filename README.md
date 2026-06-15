# Engineering Knowledge Assistant

## BridgeOps AI — Portfolio Project #3

**Status:** MVP implementation scaffold complete | **Framework stage:** Knowledge Layer  
**Stack:** Python · Streamlit · LangChain · ChromaDB · OpenAI Embeddings · Pandas · Pydantic · Plotly · Docker

---

## Executive Summary

Manufacturing organizations generate large volumes of engineering knowledge but rarely operationalize it well.

SOPs, maintenance procedures, incident reports, safety instructions, and vendor manuals typically sit across shared folders, PDFs, and tribal knowledge channels. Engineers can spend too long finding trusted answers, and managers struggle to know whether critical knowledge exists at all.

The Engineering Knowledge Assistant demonstrates how fragmented engineering documentation can be transformed into governed operational intelligence through:

- multilingual retrieval across English and German
- traceable AI-generated answers with source citations
- confidence indicators tied to retrieval quality
- knowledge-gap detection when approved documentation is missing or weak
- lightweight usage metrics for continuous improvement

This project is the BridgeOps **Knowledge Layer** positioned between the Industrial IoT Data Platform and future Decision Intelligence capabilities.

---

## Business Problem

Manufacturing organizations accumulate operational knowledge in many forms:

- SOPs
- Maintenance Procedures
- Incident Reports
- Root Cause Analyses
- Safety Documentation
- Vendor Manuals

The problem is not document creation. The problem is governed retrieval and reuse.

Typical outcomes of fragmented knowledge:

- slower troubleshooting
- longer onboarding cycles
- repeated failures
- knowledge silos
- operational risk from undocumented or untraceable decisions

---

## Why Not Just Use ChatGPT?

This project is intentionally different from a general-purpose chatbot.

### Controlled Knowledge Sources

Answers are grounded in approved engineering documents stored in the repository corpus.

### Source Traceability

Every answer returns citations with document title, document type, and source reference.

### Knowledge Governance

The system surfaces potential knowledge gaps when retrieval quality is weak or too few relevant documents are found.

### Organizational Memory

Answers reflect company-specific documentation for BridgeOps Manufacturing GmbH rather than generic internet knowledge.

---

## Architecture

```text
Documents
   ↓
Metadata Validation
   ↓
Chunking Pipeline
   ↓
Embedding Generation
   ↓
Chroma Vector Store
   ↓
Retrieval Engine
   ↓
Answer Generation
   ↓
Answer Package
```

### Answer Package

Each response includes:

- Answer
- Source Citations
- Confidence Indicator
- Retrieved Metadata
- Knowledge Gap Assessment

See [docs/architecture.md](docs/architecture.md) for the logical system view.

---

## Features

### FR-1 Document Ingestion

Supported loaders:

- PDF
- TXT
- Markdown

### FR-2 Metadata Management

Each document requires:

- document_id
- title
- document_type
- department
- equipment
- process
- site
- language
- revision
- criticality
- author
- created_date

Validation is enforced with Pydantic.

### FR-3 Multilingual Retrieval

Users can query in English or German. Retrieval uses bilingual query expansion so German queries can surface English documents and vice versa. Responses are returned in the detected or selected user language.

### FR-4 Conversational Search

The application retrieves relevant documents and chunks before composing an answer.

### FR-5 Source Citations

Every response returns explicit source citations.

### FR-6 Knowledge Gap Detection

The application triggers **Potential Knowledge Gap Detected** when:

- top retrieval score falls below threshold
- insufficient relevant documents are retrieved

### FR-7 Feedback Collection

Users can mark answers as Helpful or Not Helpful in the Streamlit UI.

### FR-8 Lightweight Usage Metrics

Tracked metrics:

- Total questions
- Helpful responses
- Unhelpful responses
- Top searched equipment

---

## Sample Corpus

The included demo corpus represents **BridgeOps Manufacturing GmbH** at the Lindau Manufacturing Facility and covers:

- Packaging Line 4
- Conveyor System A
- Vision Inspection Cell
- Laser Dimensioning Station
- Robot Cell
- Industrial Ethernet Network

Included document types:

- SOP
- RCA
- Incident Report
- Safety Procedure
- Quality Standard
- Engineering Standard

Intentional knowledge gaps remain for:

- Predictive Maintenance Program
- AI Model Validation
- Machine Learning Deployment
- Knowledge Governance Reviews

---

## Repository Structure

```text
engineering-knowledge-assistant/
├── app/
├── frontend/
├── ingestion/
├── rag/
├── analytics/
├── data/
│   ├── raw_documents/
│   ├── processed_documents/
│   ├── usage_metrics/
│   └── vector_store/
├── docs/
├── tests/
├── README.md
├── requirements.txt
└── Dockerfile
```

---

## Quick Start

### Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main build-index --rebuild
streamlit run frontend/streamlit_app.py
```

### Optional OpenAI configuration

If `OPENAI_API_KEY` is present, the application uses OpenAI embeddings and LLM-based answer synthesis.

If no API key is configured, the application falls back to deterministic local embeddings and extractive answer composition so the demo remains runnable offline.

### Docker

```bash
docker build -t engineering-knowledge-assistant .
docker run -p 8501:8501 engineering-knowledge-assistant
```

---

## Evaluation Results

The repository includes a 25-question evaluation set in [docs/evaluation_set.csv](docs/evaluation_set.csv) covering:

- Maintenance
- Quality
- Safety
- Troubleshooting
- Process Knowledge

This enables repeatable assessment of:

- citation quality
- language handling
- retrieval relevance
- knowledge-gap detection behavior

---

## Business Impact

Potential outcomes demonstrated by the project:

- faster troubleshooting
- reduced onboarding time
- improved engineering productivity
- stronger knowledge retention
- reduced dependency on tribal knowledge
- earlier visibility into missing operational documentation

---

## Future Enhancements

Deliberately in scope for future work, not this MVP:

- stronger reranking for retrieval precision
- richer document ingestion for scanned PDFs and tables
- evaluation dashboard and benchmark tracking
- document approval workflows integrated with enterprise systems

Explicitly out of scope:

- agentic workflows
- autonomous actions
- MCP integrations
- fine-tuning
- enterprise authentication and RBAC
- workflow automation platform features
