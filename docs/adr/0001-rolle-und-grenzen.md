# ADR-0001: Rolle und Grenzen von tender-ingest

- Status: Entwurf (Freigabe durch Christian offen)
- Datum: 2026-11-24
- Entscheider: Christian

## Kontext

Tender-Copilot hilft einem KMU, passende EU-Ausschreibungen zu finden, die Anforderungen zu
verstehen und schnell über Bid/No-Bid zu entscheiden. Datenquelle ist TED (Tenders Electronic Daily).
Das System besteht aus mehreren Repos (`tender-<aufgabe>`), die nur über REST oder MCP
miteinander sprechen. Jemand muss die Bekanntmachungen von TED abholen und für die
nachgelagerten Repos bereitstellen.

## Optionen

1. **Reiner Ingest:** tender-ingest holt Bekanntmachungen und legt sie unverändert als Rohdaten ab.
   Auswertung, Extraktion und Bewertung passieren in anderen Repos.
2. **Ingest mit Aufbereitung:** tender-ingest normalisiert und filtert die Daten bereits.
   Weniger Repos, aber Fachlogik und Abruf sind gekoppelt; Rohdaten gehen verloren oder
   müssen zusätzlich gespeichert werden.

## Entscheidung

Option 1 (laut Projektvorgabe in `CLAUDE.md`).

tender-ingest ist zuständig für:
- Abruf von der TED Search API (`POST https://api.ted.europa.eu/v3/notices/search`).
- Unveränderte Ablage der Rohantworten.
- Fair Usage der API (Timeouts, Retries mit Backoff, Rate-Limit).

tender-ingest ist **nicht** zuständig für:
- Interpretation, Normalisierung oder Bewertung der Bekanntmachungen.
- Download oder Analyse der Vergabeunterlagen (spätere Erweiterung, abhängig von AP3).
- Zeitsteuerung: Den täglichen Aufruf übernimmt später n8n.

Abhängigkeiten: tender-ingest hängt von keinem anderen Repo ab. Gemeinsame Schemas kommen
später aus `tender-contracts`.

## Folgen

- Nachgelagerte Repos (z. B. `tender-doc-extractor`) können jederzeit neu aus den Rohdaten
  rechnen, ohne TED erneut abzufragen.
- Das Ablageformat der Rohdaten wird zur Schnittstelle und muss stabil bleiben.
- Speicherbedarf wächst, weil nichts weggefiltert wird.
