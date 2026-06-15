# Engineering Knowledge Assistant Kundenspezifikation

Language: [EN](customer-product-spec.md) | [DE](customer-product-spec-de.md)


## Dokumentset

Dies ist die technische Hauptspezifikation (DE).

Begleitdokumente:

- [Executive Summary (DE)](customer-product-spec-executive-summary-de.md)
- [Sales Overview (DE)](customer-product-spec-sales-de.md)
- [Master Spec (EN)](customer-product-spec.md)

## Zweck

Dieses Dokument beschreibt das standardisierte Produktmuster fuer die Bereitstellung des Engineering Knowledge Assistant in Kundenumgebungen.

Es ist fuer Prospects, Implementierungsteams und technische Stakeholder gedacht und umfasst:

- Referenzarchitektur
- Dokumentverarbeitungspipeline
- erforderliche Kundeneingaben
- Deployment-Modelle und Trade-offs
- empfohlene Defaults vs. optionale Varianten

## Produktzusammenfassung

Der Engineering Knowledge Assistant ist ein governter Retrieval-Service fuer Engineering-Dokumentation.

Er unterstuetzt die Wiederverwendung von Wissen aus:

- SOPs
- Wartungsanleitungen
- Incident-Reports
- Root-Cause-Analysen
- Safety Procedures
- Qualitaetsstandards
- Vendor Manuals

Antworten sind nachvollziehbar, zitierbar und mit Gap-Signal versehen, wenn die Wissensbasis nicht ausreicht.

## Standardarchitektur

```text
Kundendokumente
   -> Metadaten-Validierung
   -> Text-Extraktion / Normalisierung
   -> Chunking
   -> Embedding-Generierung
   -> Vector Store
   -> Retrieval Engine
   -> Answer Generation
   -> Citations / Confidence / Gap Signal
   -> Web UI oder API
```

## Kernprinzipien

1. Nur kontrollierte Quellen.
2. Nachvollziehbarkeit ist Pflicht.
3. Knowledge-Gap-Erkennung ist Pflicht.
4. Mehrsprachigkeit bei Bedarf.
5. Deployment gemaess Security-Vorgaben.
6. Dokumentverarbeitung ist Produktkern, kein Nebenthema.

## Kundeneingaben

### Business Context

- Site/Plant Scope
- Zielrollen
- Use Cases
- Sprachanforderungen
- Erfolgskriterien

### Equipment/Process Context

- Linien und Asset-Hierarchie
- kritische Prozesse
- haeufige Fehlerbilder
- Maintenance Ownership

### Dokumentinventar

- SOPs
- Wartungs- und Troubleshooting-Guides
- Safety Procedures
- Incident/RCAs
- Qualitaetsstandards
- freigegebene Vendor-Inhalte

### Governance

- Dokumentowner
- Freigabestatus und Version
- Vertraulichkeitsklassen
- Retention/Redaction Regeln

### Technical Environment

- VM/Container/Cloud/on-prem Vorgaben
- Identity/Access Anforderungen
- Netzwerk-/API-Restriktionen
- Logging/Audit Anforderungen

## Verarbeitungsphasen

### Phase 1: Discovery

- minimal nutzbares Corpus definieren
- Dokumentinventar und Scope festlegen

### Phase 2: Corpus Preparation

- Extraktion, Normalisierung, Metadaten
- Freigabe- und Revisionsflags

### Phase 3: Index Build

- Chunking, Embeddings, Retrieval-Baseline
- Validierungsfragen und Ergebnisse

### Phase 4: Operational Validation

- realistische Nutzerfragen
- Antwortqualitaet und Gap-Rate bewerten
- Verbesserungsbacklog aufbauen

## Deployment-Optionen

1. Streamlit auf Kundensystem
2. Docker auf Kundensystem
3. Cloud-hosted
4. On-prem air-gapped
5. Hybrid

## Go-Live-Kriterien

- freigegebenes Corpus vorhanden
- Zitierbarkeit in Antworten aktiviert
- Gap-Signal verifiziert
- Antwortqualitaet durch Fachbereich validiert
- Verantwortlichkeiten fuer Pflege und Freigaben geklaert
