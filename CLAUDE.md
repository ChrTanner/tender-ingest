# CLAUDE.md – tender-ingest

## Kontext
Dieses Repo ist Teil des Portfolio-Systems **Tender-Copilot** (GitHub-Topic: `tender-copilot`).
Das System hilft einem KMU, passende EU-Ausschreibungen zu finden, die Anforderungen zu verstehen
und schnell über Bid/No-Bid zu entscheiden. Datenquelle: TED (Tenders Electronic Daily).

Alle Repos folgen der Namenskonvention `tender-<aufgabe>`. Sie sprechen nur über REST oder MCP miteinander.
Gemeinsame Schemas kommen später aus `tender-contracts`. Dieses Repo hängt am Anfang von keinem anderen Repo ab.

**Aufgabe von tender-ingest:** Bekanntmachungen von der TED Search API abholen und unverändert als Rohdaten
ablegen. Später ruft n8n dieses Repo täglich auf. Nachgelagerte Repos (z. B. `tender-doc-extractor`)
lesen die Rohdaten.

Das Repo startet mit einem **Spike**. Der Spike beantwortet offene Fragen zur Datenlage.
Danach wird aus dem Spike-Code ein sauberer Client.

## Arbeitsweise (verbindlich)
- Christian entscheidet Ansatz, Architektur und Design. Du schlägst Optionen mit Trade-offs vor.
  Du triffst keine Entscheidung für ihn.
- VibeWise-Ablauf: Christian beschreibt seinen Ansatz → du bewertest ihn (Schwächen, Alternativen,
  aktueller Stand der Technik) → Christian bestätigt das Design → Christian gibt jede Code-Änderung frei.
- Schreib keinen Code, bevor das Design bestätigt ist.
- Schlage bei Werkzeugen und Mustern den aktuellen Stand der Technik vor. Begründe kurz.
- Erfinde keine Fakten. Prüfe Feldnamen, Parameter und Limits gegen die TED-Doku oder echte API-Antworten.
  Wenn du etwas nicht weißt, sag es.
- Antworte auf Deutsch, kurz und direkt.
- Eine Sitzung dauert 1–2 h. Schneide Arbeit so, dass jede Sitzung mit einem lauffähigen Stand endet.

## Regeln
- Python mit `uv`. Lint und Format mit `ruff`. Tests mit `pytest`.
- `.vibe-wise/` steht in `.gitignore`. Rohdaten (`data/`) stehen in `.gitignore`, außer kleine Test-Fixtures.
- Nur öffentliche Daten. Keine Secrets im Code. Konfiguration über Umgebungsvariablen.
- Fair Usage der TED API: Timeouts, Retries mit Backoff, Rate-Limit, kleine Mengen im Spike.
- Keine personenbezogenen Daten in Logs.
- Jede wichtige Entscheidung bekommt ein ADR unter `docs/adr/` (Format: Kontext, Optionen, Entscheidung, Folgen).
- Messwerte statt Behauptungen: Mengen, Füllquoten, Laufzeit, Fehlerquote.
- Commit-Nachrichten nach Conventional Commits.

## TED Search API (geprüfte Fakten, Stand 11/2026)
- Endpunkt: `POST https://api.ted.europa.eu/v3/notices/search`. Ohne Anmeldung nutzbar.
- Swagger: https://api.ted.europa.eu/swagger-ui/index.html
- Doku: https://docs.ted.europa.eu/api/latest/search.html
- Parameter u. a.: `query` (Expert Query), `fields`, `limit`, `page`, `scope`, `checkQuerySyntax`,
  `paginationMode` (`PAGE_NUMBER` oder `ITERATION`).
- Limits Seitenmodus: max. 250 Bekanntmachungen pro Seite, max. 15.000 abrufbar, max. 10.000 Felder pro Seite.
- Iterationsmodus: Erste Seite liefert ein Token. Das Token geht in die nächste Abfrage.
- Feldnamen: Liste auf der Expert-Search-Seite von TED (https://ted.europa.eu/en/expert-search).
  Swagger nennt die Felder nur, erklärt sie aber nicht.
- Die API liefert eForms-Bekanntmachungen und Bekanntmachungen im alten TED-Schema.
- Relevante eForms-Business-Terms: BT-15 (Documents URL), BT-707 (Begründung für eingeschränkten Zugang).

## Arbeitspakete

### AP1 – Repo-Grundgerüst (1 Sitzung)
- `uv init`, Paketstruktur `src/tender_ingest/`, `ruff`, `pytest`, `.gitignore`.
- GitHub Action: Lint und Tests bei jedem Push und PR. Optional: `gitleaks` gegen Secrets.
- README-Gerüst mit den Abschnitten aus der Definition of Done (siehe unten).
- ADR-Vorlage und ADR-0001 „Rolle und Grenzen von tender-ingest“.
- Fertig, wenn: `uv run pytest` läuft und CI grün ist.

### AP2 – Spike: Zugang und Mengen (1 Sitzung)
- Minimaler Abruf mit einer Expert Query. Christian legt den Filter fest (z. B. CPV-Bereich, Länder, Zeitraum).
- Rohantworten unverändert speichern (z. B. `data/raw/<datum>/<seite>.json`).
- Fragen:
  - A. Funktioniert eine Expert Query aus der TED-Webseite unverändert in der API?
  - B. Wie viele neue Bekanntmachungen pro Tag gibt es für den Filter? Reicht der Seitenmodus,
    oder ist der Iterationsmodus nötig?
- Fertig, wenn: Rohdaten für mindestens 7 Tage liegen vor und die Zahlen zu A und B stehen in `docs/spike-ted.md`.

### AP3 – Spike: Struktur und Vergabeunterlagen (1–2 Sitzungen)
- Analyse direkt auf den Rohdaten (Werkzeug wählt Christian, z. B. DuckDB oder Polars).
- Fragen:
  - C. Anteil eForms vs. altes TED-Schema. Füllquote der Felder Auftraggeber, CPV, Frist,
    geschätzter Wert, Zuschlag. Wie gut sind Lose abbildbar?
  - D. Füllquote von BT-15 und BT-707. Kategorien der Links: direktes PDF, Plattform mit Login,
    toter Link. 20 Zufallslinks für eine manuelle Prüfung ausgeben.
- Fertig, wenn: Zahlen zu C und D stehen in `docs/spike-ted.md`, plus ADR-Entwurf
  „Primäre Datenquelle für Phase 1“ (Optionen: XML, PDF, synthetisch). Die Entscheidung trifft Christian.

### AP4 – Vom Spike zum Client (1–2 Sitzungen)
- Sauberer, getesteter TED-Client: Timeouts, Retries mit Backoff, Paginierung, idempotente Ablage
  (gleiche Bekanntmachung wird nicht doppelt gespeichert).
- CLI mit einem Befehl, z. B. `uv run tender-ingest fetch --since <datum>`.
- Tests mit aufgezeichneten API-Antworten (keine echten API-Calls in CI).
- Fertig, wenn: CLI läuft, Tests grün, Messwerte (Laufzeit, Anzahl, Fehlerquote) im README.

### AP5 – Docker und Abschluss (1 Sitzung)
- Dockerfile, Image auf GHCR über GitHub Action, Version 0.1.0 nach SemVer.
- Architekturbild mit Archify erzeugen (siehe Abschnitt „Architekturbild mit Archify“).
- README vollständig nach Definition of Done.
- Fertig, wenn: `docker run ... fetch` funktioniert, das Image auf GHCR liegt und das Architekturbild im README ist.

Spätere Erweiterungen (nicht jetzt): REST-Endpunkt für n8n, Ablage in Postgres oder Object Storage,
Download der Vergabeunterlagen (abhängig vom Ergebnis aus AP3).

## Architekturbild mit Archify
- Werkzeug: Skill Archify (https://github.com/tt-a1i/archify). Installation einmalig: `npx skills add tt-a1i/archify -g`
- Zeitpunkt: am Ende des Repos (AP5) und nach jeder Änderung an der Architektur.
- Prompt: „Use archify to map this repository's runtime architecture. 8–12 Knoten, ein Hauptpfad,
  externe Abhängigkeiten (TED API, Dateiablage) und Vertrauensgrenzen. Nur Komponenten, die im Repo existieren.“
- Ablage: `docs/architecture/` mit HTML und JSON-Quelle von Archify, plus Export als SVG oder PNG.
- README: SVG/PNG einbinden und auf die interaktive HTML-Version verlinken.

## Definition of Done für das Repo
- README: Problem, Architekturbild (mit Archify erzeugt), Start mit einem Befehl
- ADR für jede wichtige Entscheidung
- Messtabelle (Mengen, Füllquoten, Laufzeit, Fehlerquote)
- Tests und CI grün
- Abschnitt „Was nicht funktioniert hat“
- Abschnitt „Betrieb im Unternehmen“ (Konfiguration, Fair Usage, Logging ohne personenbezogene Daten,
  Wiederanlauf nach Fehlern)

## Übergabe an das Planungsprojekt
Am Ende jedes Arbeitspakets: Aktualisiere `docs/fortschritt.md` mit Datum, Ergebnis, offenen Punkten
und getroffenen Entscheidungen. Christian bringt diese Datei zurück in das Planungsprojekt.
