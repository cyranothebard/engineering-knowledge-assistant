# Engineering Knowledge Assistant Architecture

```mermaid
flowchart TD
    DOCS[Approved Engineering Documents\nPDF · TXT · Markdown] --> META[Metadata Validation\nPydantic schema]
    META --> CHUNK[Chunking Pipeline\nRecursive splitter]
    CHUNK --> EMBED[Embedding Generation\nOpenAI or deterministic local fallback]
    EMBED --> STORE[Chroma Vector Store]
    STORE --> RETRIEVE[Retrieval Engine\nMultilingual query expansion]
    RETRIEVE --> ANSWER[Answer Generation\nLLM or extractive fallback]
    ANSWER --> PACKAGE[Answer Package\nAnswer · Citations · Confidence · Gap flag]
    PACKAGE --> UI[Streamlit Interface]
    PACKAGE --> METRICS[Usage Metrics\nQuestions · Feedback · Equipment trends]
```

## Design Notes

- Controlled corpus only. No web search.
- Source citations are preserved from document metadata through chunk retrieval.
- Knowledge-gap detection is based on retrieval score and source count, not model self-confidence.
- Corpus replacement requires updating document files and manifest metadata, not application code.
