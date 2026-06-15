# Engineering Knowledge Assistant Customer Product Specification

Language: [EN](customer-product-spec.md) | [DE](customer-product-spec-de.md)


## Document Set

This is the master technical specification.

Companion versions:
- [Executive Summary](customer-product-spec-executive-summary.md)
- [Sales Overview](customer-product-spec-sales.md)

## Purpose

This document describes the standardized product pattern for deploying the Engineering Knowledge Assistant for a customer.

It is intended for prospective customers, implementation teams, and technical stakeholders who need to understand:
- the reference architecture
- the document processing pipeline
- the information required from the customer
- deployment models and tradeoffs
- recommended defaults versus optional variations

## Product Summary

The Engineering Knowledge Assistant is a governed retrieval system for engineering documentation.

It is designed to help customers search, reuse, and operationalize content such as:
- SOPs
- maintenance procedures
- incident reports
- root cause analyses
- safety procedures
- quality standards
- vendor manuals or excerpts

The system answers in a traceable way and can flag knowledge gaps when the corpus does not support a confident answer.

## Standardized Architecture

The reference architecture follows a simple controlled pipeline:

```text
Customer Documents
   -> Metadata Validation
   -> Text Extraction / Normalization
   -> Chunking
   -> Embedding Generation
   -> Vector Store
   -> Retrieval Engine
   -> Answer Generation
   -> Citations / Confidence / Gap Signal
   -> Web UI or API
```

### Architectural Principles

1. Controlled sources only.
2. Traceability is mandatory.
3. Knowledge-gap detection is required.
4. Multilingual retrieval is supported where needed.
5. Deployment must adapt to customer security constraints.
6. Document processing is part of the product, not an afterthought.

## Reference Components

### 1. Ingestion Layer

Responsible for bringing customer content into the system.

Supported inputs:
- PDF
- DOCX, if needed as a custom extension
- TXT
- Markdown
- exported HTML or plain text from internal systems, if customer-approved

Recommended default:
- PDF, TXT, and Markdown only for the first deployment

### 2. Metadata Validation Layer

Each document should be validated before indexing.

Required metadata fields:
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

Optional but recommended fields:
- source_system
- approval_status
- validity_start
- validity_end
- change_control_ticket
- confidentiality_level

### 3. Text Processing Layer

Responsibilities:
- extract text from source documents
- remove boilerplate where appropriate
- normalize whitespace and line breaks
- preserve meaningful headings and section structure
- identify tables, lists, warnings, and step sequences

Recommended default:
- retain document section structure in the stored text
- do not aggressively rewrite customer language during ingestion

### 4. Chunking Layer

The assistant works best when documents are split into retrievable chunks that keep local context intact.

Recommended chunking behavior:
- chunk by semantic section boundaries when possible
- keep step lists together
- avoid splitting short safety procedures too aggressively
- keep vendor warnings and tolerances intact

Recommended default settings:
- moderate chunk size
- light overlap
- section-aware splitting

### 5. Embedding and Retrieval Layer

The system embeds chunks into a vector store and retrieves the most relevant passages at query time.

Capabilities:
- multilingual query expansion
- source scoring
- similarity-based retrieval
- ranking across vendor and customer documents

Recommended default:
- one primary vector store per customer
- isolate corpora by customer unless an explicit multi-tenant architecture is required

### 6. Answer Composition Layer

The assistant composes a response from retrieved content.

Each answer should include:
- direct answer text
- citations
- confidence indicator
- knowledge-gap indicator if appropriate
- retrieved document metadata for auditability

### 7. User Interface Layer

Current reference UI:
- Streamlit application for fast interactive demo and operational use

Optional extensions:
- REST API
- Teams/Slack front end
- embedded web widget
- intranet portal integration

## Document Types to Request from Each Customer

For a first deployment, request a focused but representative set of document types.

### Priority Document Types

1. SOPs
2. Maintenance instructions
3. Safety procedures
4. RCA reports
5. Incident reports
6. Quality standards
7. Equipment manuals or approved excerpts

### Suggested Initial Volume

Recommended starting set:
- 25 to 30 vendor or equipment-related documents or excerpts
- 10 to 12 customer-specific operating documents

If the customer does not have that volume ready, start smaller with the most frequently used operational documents and expand iteratively.

## What To Request From the Customer

This is the practical intake checklist for a new customer.

### A. Business Context

Ask the customer for:
- plant or site name
- business unit or division
- primary use cases
- target audience roles
- languages used by the workforce
- known pain points in retrieval or onboarding
- business goals for the rollout

### B. Equipment and Process Context

Ask the customer for:
- equipment list by line or area
- line names and asset identifiers
- critical process steps
- common failure modes
- maintenance ownership structure
- safety-critical assets and procedures
- vendor ecosystem by machine family

### C. Document Inventory

Ask the customer for:
- current SOPs
- maintenance manuals
- troubleshooting guides
- safety procedures
- quality standards
- incident logs
- RCAs
- approved vendor documentation or excerpts

### D. Governance and Access

Ask the customer for:
- approval status for each document
- document owner or approver
- version history
- confidentiality classification
- retention requirements
- redaction constraints
- whether the corpus must be air-gapped

### E. Technical Environment

Ask the customer for:
- deployment preference
- identity and access requirements
- browser access limitations
- container or VM policy
- network segmentation rules
- API access restrictions
- logging or audit requirements

### F. Success Criteria

Ask the customer for:
- top questions they want answered faster
- acceptable response quality threshold
- search latency expectations
- languages required at launch
- who will validate the corpus
- what counts as a successful pilot

## Document Processing Requirements by Customer Phase

### Phase 1: Discovery

Objective:
- identify the minimal useful corpus

Deliverables:
- document inventory
- site and equipment map
- use-case shortlist

### Phase 2: Corpus Preparation

Objective:
- prepare documents for indexing

Deliverables:
- normalized text extracts
- metadata spreadsheet or manifest
- approval and revision flags
- document naming convention

### Phase 3: Index Build

Objective:
- create searchable vector index

Deliverables:
- indexed chunks
- retrieval validation set
- baseline query results

### Phase 4: Operational Validation

Objective:
- prove the assistant is useful in realistic scenarios

Deliverables:
- test questions
- retrieval screenshots or logs
- gap analysis
- go-live recommendations

## Recommended Metadata Contract

The minimum customer-side contract should require the following for every document:

```json
{
  "document_id": "unique id",
  "title": "human readable title",
  "document_type": "SOP | RCA | Safety Procedure | Quality Standard | Vendor Documentation | Incident Report",
  "department": "owner department",
  "equipment": "equipment or line association",
  "process": "process name",
  "site": "site name",
  "language": "en | de | ...",
  "revision": "version label",
  "criticality": "High | Medium | Low",
  "author": "owner or source",
  "created_date": "YYYY-MM-DD"
}
```

Recommended extension fields:
- approval_status
- source_system
- file_path
- confidentiality_level
- checksum
- validity_end

## Customer Onboarding Questions

These are the exact questions to ask during onboarding.

### Operational Use

- What questions do engineers ask most often today?
- Which topics generate the most interruption to experts?
- What are the most common safety, maintenance, and troubleshooting scenarios?
- Which lines or assets should be supported first?

### Corpus Scope

- Which documents are approved for the first release?
- Which documents are too sensitive or incomplete to include?
- Do you want vendor excerpts, full manuals, or only customer-authored content?
- Are there known gaps that should be left intentionally visible?

### Language and Access

- Which languages should the assistant support at launch?
- Do you need cross-language retrieval, or only language-specific search?
- Can the corpus be accessed via browser, internal VPN, or only on-site networks?

### Governance

- Who owns approval for each document class?
- What is the change-control process for updates?
- What is the retention and audit requirement?
- How should the system signal that a document is out of date?

## Deployment Options

The product should support multiple deployment models.

### Option 1: Streamlit App on Customer VM or Server

Best for:
- fast pilot deployment
- internal demo environments
- small teams

Pros:
- simple to launch
- low infrastructure overhead
- good for controlled pilots

Cons:
- less suitable for large-scale enterprise usage
- basic UI compared to a bespoke portal

### Option 2: Docker Container on Customer Infrastructure

Best for:
- standardization
- repeatable deployments
- operations teams that already use containers

Pros:
- portable
- consistent runtime
- easy to automate in CI/CD

Cons:
- requires container orchestration discipline
- may still need customer support for persistent storage and secrets

### Option 3: Cloud-Hosted Managed Service

Best for:
- customer organizations comfortable with cloud deployment
- rapid iteration and centralized operations

Pros:
- easiest to manage centrally
- simplifies updates and monitoring
- supports faster feature rollout

Cons:
- may not fit strict data residency or air-gap requirements
- requires security review and access control design

### Option 4: On-Prem Air-Gapped Deployment

Best for:
- sensitive manufacturing environments
- regulated environments
- strict network isolation requirements

Pros:
- strongest control over data locality
- aligns with many factory security policies

Cons:
- more operational responsibility for the customer
- external API usage may be restricted or impossible

### Option 5: Hybrid Deployment

Best for:
- customers who want local document control with optional external AI services

Pros:
- flexible
- can keep sensitive documents local while using optional backends for non-sensitive tasks

Cons:
- more complex policy design
- requires clear separation between local and external processing

## Recommended Defaults

For most first deployments, recommend:
- Docker container deployment
- local or customer-controlled vector store
- controlled document corpus only
- Streamlit UI for the initial interface
- optional OpenAI or local fallback depending on customer policy

If the customer is highly security-sensitive, move to on-prem or air-gapped deployment and use local fallback behavior where required.

## Security and Governance Considerations

The product should be implemented with the following controls:

- role-based access if the customer needs it
- separation between customer corpora
- document approval and revision tracking
- logs for question and retrieval activity
- clear handling of knowledge gaps
- no uncontrolled web search by default

## Implementation Phases for a Customer

### Phase A: Discovery and Scoping

- identify use cases
- gather document inventory
- define deployment constraints
- agree on success criteria

### Phase B: Corpus Build

- ingest documents
- normalize metadata
- create initial index
- validate retrieval behavior

### Phase C: Pilot

- run a small audience demo
- gather feedback on top questions
- tune chunking and retrieval settings
- refine gap handling and citations

### Phase D: Production Rollout

- expand corpus
- finalize deployment method
- add monitoring and operational ownership
- define update process for new documents

## Acceptance Criteria for Customer Go-Live

The system should not go live until the following are true:

- key use cases have working answers
- citations are present and accurate
- the corpus owner approves the document set
- gap detection works on intentionally missing topics
- deployment model matches customer security requirements
- operational support ownership is assigned

## Optional Enhancements

The base product can be extended with:
- API access for integrations
- SSO / identity provider integration
- document approval workflows
- audit dashboards
- analytics and topic trends
- role-aware question routing
- richer multilingual support

## Non-Goals for the Base Version

The base implementation is not intended to be:
- a general internet chatbot
- a replacement for engineering approval
- a CMMS or document management system
- an autonomous decision-making system

It is a governed retrieval and knowledge access layer.

## Summary

For customers, the product should be positioned as a standardized knowledge layer that turns approved engineering documents into an answer system with traceability, governance, and deployment flexibility.

The important implementation rule is simple:

- the quality of the assistant depends on the quality, scope, and governance of the underlying corpus.

## Appendix A: Customer Intake Checklist

Use this checklist during discovery and kickoff. Mark each item as Complete, Partial, or Missing.

### A1. Customer Profile and Scope

| Item | Status | Notes |
|------|--------|-------|
| Customer legal name and business unit captured |  |  |
| Primary site(s) identified |  |  |
| Initial rollout scope defined (line, area, or plant) |  |  |
| Primary users identified (engineers, operators, quality, safety) |  |  |
| Languages required at launch confirmed |  |  |
| Named executive sponsor and technical owner identified |  |  |

### A2. Business Objectives and Success Criteria

| Item | Status | Notes |
|------|--------|-------|
| Top 5 high-value questions documented |  |  |
| Current pain points quantified (search time, escalations, rework) |  |  |
| Pilot KPIs defined (quality, speed, adoption) |  |  |
| Target response quality threshold agreed |  |  |
| Go-live acceptance criteria agreed |  |  |

### A3. Equipment and Process Context

| Item | Status | Notes |
|------|--------|-------|
| Equipment inventory by line/area provided |  |  |
| Critical process steps documented |  |  |
| Common failure modes listed |  |  |
| Safety-critical assets and procedures identified |  |  |
| Vendor landscape by equipment family captured |  |  |

### A4. Document Inventory and Content Readiness

| Item | Status | Notes |
|------|--------|-------|
| SOP corpus provided |  |  |
| Maintenance procedures provided |  |  |
| Safety procedures provided |  |  |
| RCA and incident reports provided |  |  |
| Quality standards provided |  |  |
| Vendor manuals or approved excerpts provided |  |  |
| Initial corpus size meets recommended baseline |  |  |

Recommended baseline:
- 25 to 30 vendor or equipment-related documents/excerpts
- 10 to 12 customer-specific operating documents

### A5. Metadata and Governance Readiness

| Item | Status | Notes |
|------|--------|-------|
| Required metadata fields available for each document |  |  |
| Document approval status available |  |  |
| Revision/version tracking available |  |  |
| Document ownership assigned per document class |  |  |
| Retention and audit requirements documented |  |  |
| Confidentiality classification available |  |  |

Required fields check:
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

### A6. Security and Compliance Constraints

| Item | Status | Notes |
|------|--------|-------|
| Data residency requirements confirmed |  |  |
| Air-gap requirement confirmed (yes/no) |  |  |
| External API usage policy confirmed |  |  |
| Redaction requirements captured |  |  |
| Logging and audit expectations defined |  |  |
| Access control model identified (if required) |  |  |

### A7. Technical Environment and Deployment

| Item | Status | Notes |
|------|--------|-------|
| Deployment model selected |  |  |
| Infrastructure owner identified |  |  |
| Network constraints documented |  |  |
| Browser/client constraints documented |  |  |
| Container/VM policy confirmed |  |  |
| Integration requirements captured (API, SSO, portal) |  |  |

Deployment model selected:
- Streamlit on customer VM/server
- Docker on customer infrastructure
- Cloud-hosted managed service
- On-prem air-gapped
- Hybrid

### A8. Pilot Plan and Handover Readiness

| Item | Status | Notes |
|------|--------|-------|
| Pilot timeline agreed |  |  |
| Pilot user group selected |  |  |
| Evaluation question set drafted |  |  |
| Feedback collection process defined |  |  |
| Support and escalation owner assigned |  |  |
| Document update cadence agreed |  |  |

### A9. Intake Decision Gate

Use this gate before implementation starts.

| Decision Gate | Pass/Fail | Notes |
|---------------|-----------|-------|
| Business use cases are clear and prioritized |  |  |
| Corpus is sufficient for pilot |  |  |
| Metadata quality is acceptable |  |  |
| Deployment/security path is approved |  |  |
| Named customer owners are in place |  |  |

If one or more gates fail, run a remediation cycle before build/index work.

### A10. Intake Meeting Template (Quick Capture)

Use this section to capture the kickoff call quickly.

- Customer:
- Site(s):
- Sponsor:
- Technical owner:
- Primary users:
- Languages:
- Deployment preference:
- Top 5 questions to solve:
- Documents already available:
- Known documentation gaps:
- Security constraints:
- Target pilot date:
- Go-live success criteria:
