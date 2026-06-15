# Engineering Knowledge Assistant Demo Runbook (DE)

Language: [EN](demo-runbook.md) | [DE](demo-runbook-de.md)


## Zweck

Dieses Runbook erlaubt die Demo-Durchfuehrung ohne Vorwissen.

Es umfasst:

- Start- und Preflight-Schritte
- Sprechleitfaden fuer Business + Technik
- erwartbare Fragen und Antworten
- Recovery-Massnahmen bei Live-Problemen

## Demo-Ziel

Die Demo soll drei Punkte klar zeigen:

1. Relevantes Engineering-Wissen wird aus freigegebenen Quellen gefunden.
2. Antworten sind zitierbar und nachvollziehbar.
3. Das System arbeitet als operatives Wissenswerkzeug, nicht als allgemeiner Chatbot.

## Pre-Demo-Checkliste

- App starten:
  - `streamlit run frontend/streamlit_app.py --server.port 8501`
- Index/Corpus verfuegbar
- je eine EN- und DE-Frage pruefen
- Zitate unter Antworten sichtbar
- Sidebar-Metriken sichtbar

## Empfohlene Storyline

1. Problem: Wissen ist verteilt und schwer auffindbar.
2. Loesung: governte Retrieval-Pipeline ueber freigegebenes Corpus.
3. Live-Fragen in EN/DE mit Zitaten zeigen.
4. Gap-Signal bei nicht abgedeckten Fragen demonstrieren.
5. Mit Business-Nutzen und Deployment-Optionen schliessen.

## Demo-Ablauf

### Schritt 1: Landing Page

- Branding, Sidebar-Metriken, Beispiel-Fragen zeigen

### Schritt 2: Routinefrage

Beispiel: "How do I start Packaging Line 4?"

### Schritt 3: Cross-Source Frage

Beispiel: "What is the proper SEW coupling alignment tolerance?"

### Schritt 4: Mehrsprachige Frage

Beispiel: "Welche Ursachen wurden fuer Vibrationsalarme dokumentiert?"

### Schritt 5: Gap-Frage

Beispiel: "What is our approved machine learning validation process?"

## Typische Fragen

### Ist das ein Chatbot?

Nein. Es ist governte Retrieval-Antwortgenerierung auf freigegebenen Quellen.

### Was passiert bei fehlender Dokumentabdeckung?

Das System signalisiert eine Wissensluecke statt unsicher zu raten.

### Warum mehrsprachig?

Reale Teams arbeiten in mehreren Sprachen; Retrieval muss dies abdecken.

## Recovery

### App startet nicht

- alternativer Port: `--server.port 8510`
- Projektroot pruefen

### Antworten ohne Zitate

- Indexstatus pruefen
- Corpus-Rebuild ausfuehren

### UI-Fehler

- Streamlit neu starten
- Browser neu laden

## Demo-Close

"Dieses System macht aus Dokumentablage eine operative Wissensschicht: schnell, nachvollziehbar und governbar."
