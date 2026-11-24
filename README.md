# tender-ingest

Teil von **Tender-Copilot**. Holt Bekanntmachungen von der TED Search API
(Tenders Electronic Daily) und legt sie unverändert als Rohdaten ab.

> Status: Grundgerüst (AP1). Noch keine Fachlogik.

## Problem

_TODO: Welches Problem löst das Repo für das KMU? (AP2–AP4)_

## Architektur

_TODO: Architekturbild mit Archify (AP5), interaktive Version unter `docs/architecture/`._

## Start mit einem Befehl

```bash
uv sync
uv run pytest
```

_TODO: `uv run tender-ingest fetch --since <datum>` (AP4), `docker run ... fetch` (AP5)._

## Entwicklung

| Aufgabe | Befehl |
|---|---|
| Abhängigkeiten installieren | `uv sync` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Tests | `uv run pytest` |

Änderungen laufen über Branch → Pull Request → grüne CI → Merge.
Die CI prüft ruff, pytest und gitleaks.

## Entscheidungen

ADRs unter [`docs/adr/`](docs/adr/).

## Messwerte

_TODO: Mengen, Füllquoten, Laufzeit, Fehlerquote (AP2–AP4)._

| Messgröße | Wert | Quelle |
|---|---|---|
| | | |

## Was nicht funktioniert hat

_TODO_

## Betrieb im Unternehmen

- **Konfiguration:** _TODO (Umgebungsvariablen)_
- **Fair Usage der TED API:** _TODO (Timeouts, Retries mit Backoff, Rate-Limit)_
- **Logging ohne personenbezogene Daten:** _TODO_
- **Wiederanlauf nach Fehlern:** _TODO_
