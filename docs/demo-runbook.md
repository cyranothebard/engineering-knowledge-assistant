# Engineering Knowledge Assistant Demo Runbook

## Purpose

This runbook is intended to let another person run the demo without prior context.

It covers:
- how to start the demo
- what to say during the demo
- how to explain the product to technical and business audiences
- what questions to expect
- how to recover if something breaks mid-demo

Product name used in this runbook: Engineering Knowledge Assistant.

## Demo Goal

The demo should show three things clearly:

1. The assistant finds relevant engineering knowledge from approved documents.
2. The answer is traceable, with citations and confidence/gap signals.
3. The system behaves like an operational knowledge tool, not a general chatbot.

The best demo outcome is when the audience understands both the business value and the technical mechanics.

## Audience

This runbook is optimized for a mixed audience:
- business stakeholders who care about operational risk, speed, and onboarding
- technical stakeholders who care about retrieval, data quality, and deployment

## Demo Length

Recommended live demo length: 12 to 18 minutes.

Suggested timing:
- 2 minutes: context and business problem
- 4 to 6 minutes: live interaction
- 2 to 3 minutes: knowledge gap and traceability examples
- 2 to 4 minutes: technical architecture and deployment discussion
- 2 to 3 minutes: questions

## Pre-Demo Checklist

Use this checklist before every demo.

- Confirm the app is running.
  - Preferred launch command from the project root:
    - `streamlit run frontend/streamlit_app.py --server.port 8501`
  - If port 8501 is busy, use another free port such as 8510 or 8511.
- Open the browser page and verify the title is Engineering Knowledge Assistant - BridgeOps.
- Confirm the demo corpus has been indexed.
- Confirm you can answer at least one English question and one German question.
- Confirm citations appear under the answer.
- Confirm the sidebar metrics render.
- Confirm there are no browser popups, login prompts, or stale error messages.

## Environment Notes

The demo was built to run locally on a laptop or workstation.

Current compatibility notes:
- The Streamlit version in this environment is older than current releases.
- The app includes compatibility fallbacks for older Streamlit APIs.
- Package warnings from pandas dependencies are non-blocking and do not stop the demo.

If you need to restart the app during a handoff, use the exact project path to avoid import or working-directory issues:

```bash
streamlit run /Users/brandonlewis/Desktop/pyprojects/engineering-knowledge-assistant/frontend/streamlit_app.py --server.port 8501
```

## Demo Storyline

Tell the story in this order:

1. Manufacturing teams have critical knowledge in SOPs, RCAs, safety procedures, and vendor manuals.
2. The problem is not only document storage; it is governed retrieval and reuse.
3. This assistant turns that corpus into an operational knowledge layer.
4. Users ask questions in English or German.
5. The system retrieves relevant source material, composes an answer, and shows citations.
6. If the corpus does not cover the question well, it flags a potential knowledge gap instead of pretending certainty.

## Suggested Opening Script

Use this as the opening if you are presenting to a mixed audience.

"This demo shows a manufacturing knowledge assistant built for controlled engineering content. Instead of searching through folders or asking a person who happens to know the answer, the system retrieves approved documents, composes a grounded response, and shows where the answer came from. The goal is not just faster search. The goal is traceable operational knowledge that reduces downtime, improves onboarding, and makes knowledge gaps visible."

## Suggested Technical Framing

If the audience includes engineers, describe the system this way:

- Documents are validated with metadata before ingestion.
- Text is chunked and embedded into a vector store.
- Queries are expanded for multilingual retrieval.
- Answers are generated from the most relevant retrieved chunks.
- Citations and gap detection are attached to the answer package.
- Usage metrics record questions, feedback, and equipment interest.

## Suggested Business Framing

If the audience is non-technical or partially technical, emphasize the outcome:

- Faster answers for maintenance and operations.
- Better onboarding for new engineers and operators.
- More consistent troubleshooting across shifts.
- Lower dependence on tribal knowledge.
- Better visibility into what the documentation does not yet cover.

## Live Demo Flow

### 1. Show the landing page

Talk track:
- This is the front end for the BridgeOps Knowledge Layer.
- It is designed for controlled engineering documentation.
- The side panel shows usage metrics so teams can see adoption and common topics.

What to point out:
- title and branding
- usage metrics in the sidebar
- example questions
- language selector

### 2. Ask a routine maintenance question

Example question:
- How do I start Packaging Line 4?

What to say:
- This is the simplest happy path.
- The assistant should retrieve the startup SOP and related source material.
- Notice that the answer is not only text; it also includes citations.

What to highlight:
- the answer itself
- source citations
- retrieved document details
- confidence or gap signal

### 3. Ask a question that crosses vendor and operational docs

Example question:
- What is the proper SEW coupling alignment tolerance and how do I check it?

What to say:
- This shows why the corpus was designed around a coherent automation stack.
- The assistant should surface both the vendor maintenance guide and the plant RCA or SOP.
- This is the difference between generic search and operational retrieval.

What to highlight:
- vendor and internal documents appearing together
- explicit tolerance values or inspection steps
- traceability back to source reference filenames

### 4. Ask a multilingual question

Example question in German:
- Welche Ursachen wurden fuer Vibrationsalarme dokumentiert?

What to say:
- The assistant supports English and German because manufacturing teams do not always search in the same language they read or write documents in.
- The retrieval layer expands the query so it can match across languages.

What to highlight:
- answer language selection
- retrieval of relevant German or English documents
- the corpus is multilingual, but the assistant is still grounded in approved content

### 5. Ask a knowledge-gap question

Example question:
- What is our approved machine learning validation process?

What to say:
- This is an intentional test of governance.
- The system should not invent a procedure.
- Instead, it should flag that the corpus does not contain sufficient approved material.

What to highlight:
- knowledge gap message
- why gap detection matters in regulated or operational environments
- this is a feature, not a failure

### 6. Show feedback and metrics

What to say:
- The assistant can collect lightweight feedback.
- Usage metrics help identify which topics people ask about most often.
- Over time, that makes content gaps visible to operations and engineering leads.

What to highlight:
- Helpful / Not Helpful feedback
- question counts
- top searched equipment

## Recommended Demo Questions

Use these questions in this order if you want a consistent, low-risk demo.

1. How do I start Packaging Line 4?
2. What LED state confirms normal S7-1500 operation?
3. How do I verify SICK laser sensor accuracy?
4. What is the SEW coupling alignment tolerance?
5. Welche Ursachen wurden fuer Vibrationsalarme dokumentiert?
6. How do I safely enter the robot cell for maintenance work?
7. What caused the vision false-reject spike on 2026-03-15?
8. What is our approved machine learning validation process?

## Suggested Script by Role

### If speaking to business leaders

Use language like this:

"The value here is speed, consistency, and risk reduction. People no longer have to hunt for the right version of a procedure or wait for one person who knows the answer. They get a traceable answer grounded in approved documents, and if the documentation is incomplete, the system says so. That is how you turn fragmented knowledge into an operational asset."

### If speaking to engineers

Use language like this:

"The assistant is not reading the internet. It retrieves from a controlled corpus, validates document metadata, chunks the sources, embeds them into a vector store, and answers from retrieved context. The design intentionally surfaces vendor documentation alongside internal RCAs and SOPs so the retrieval pattern matches real troubleshooting behavior."

### If speaking to both

Use language like this:

"The business outcome is faster, safer knowledge reuse. The technical mechanism is governed retrieval over a structured engineering corpus. The important part is that the two are aligned: the interface is simple, but the answers are traceable and the corpus design is intentional."

## Common Questions and Suggested Answers

### Is this just a chatbot?

Suggested answer:
"No. It is a controlled retrieval system. The answer comes from approved documents in the corpus, and the output includes citations and a knowledge-gap signal."

### What happens if the answer is not in the documents?

Suggested answer:
"The system flags a potential knowledge gap. That prevents it from pretending to know something that is not supported by the corpus."

### Why does multilingual retrieval matter?

Suggested answer:
"In real plants, people work in more than one language. A technician may search in German while the original vendor manual is in English. The retrieval layer bridges that gap."

### How is this different from a keyword search?

Suggested answer:
"Keyword search returns documents. This system returns an answer package: the answer, the citations, the confidence/gap signal, and the retrieved context."

### Can this be deployed inside a customer environment?

Suggested answer:
"Yes. The product spec supports customer VM, Docker, cloud, on-prem, and hybrid deployment options depending on the customer’s security and infrastructure constraints."

### Can we use our own documents?

Suggested answer:
"Yes. The document set is customer-specific. The ingestion pipeline expects customer SOPs, maintenance instructions, incident reports, standards, and optionally vendor manuals."

### Does it require OpenAI?

Suggested answer:
"No. It can use OpenAI embeddings and LLM synthesis when keys are available, but it also supports deterministic local fallback behavior so the demo and baseline system can run without external API access."

## Handoff Notes for a Substitute Presenter

If someone else has to run the demo, tell them to do the following:

1. Start the app from the project root or use the absolute app path.
2. Check that the browser page is already open on the right port.
3. Run one simple question first to prove the app is live.
4. Run one vendor-plus-SOP question to show retrieval quality.
5. Run one German question to show multilingual support.
6. Run one knowledge-gap question to show governance.
7. Do not over-explain the internals until after the audience sees the result.
8. If something looks off, return to the simplest question and recover the demo flow.

## Recovery Plan If the Demo Breaks

### If the app does not load

Check:
- correct port
- correct working directory
- browser page refresh
- whether the Streamlit process is still running

Fallback:
- restart Streamlit using the absolute path to the app file

### If a question returns a poor answer

Check:
- whether the question is too broad
- whether the corpus contains a relevant document
- whether the question should be asked in English or German

Fallback:
- switch to one of the recommended demo questions

### If the audience asks about something not covered

Use this response:
"That is not in the current demo corpus, which is actually useful because it shows the knowledge-gap behavior. For production use, that would be handled by adding the missing customer documents and re-indexing."

## What Not To Do

- Do not claim the corpus represents real customer production content.
- Do not improvise on the technical details of a question if the answer is not returned by the system.
- Do not overuse jargon for the business audience.
- Do not hide the knowledge-gap response; it is part of the value proposition.

## Demo Close

Close with a statement like this:

"The point of this product is not to replace engineers. It is to make approved engineering knowledge easier to find, easier to trust, and easier to scale across teams, sites, and languages."
