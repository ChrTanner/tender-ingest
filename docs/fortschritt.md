# Fortschritt tender-ingest

## AP1 – Repo-Grundgerüst (2026-11-24) – abgeschlossen

**Ergebnis**
- uv-Paket `src/tender_ingest/`, Python 3.14, Build-Backend `uv_build`.
- Tests in `tests/` neben `src/` (Smoke-Test). ruff (Lint + Format) und pytest als Dev-Abhängigkeiten.
- CI (GitHub Actions): ruff check, ruff format --check, pytest, gitleaks.
- README-Gerüst nach Definition of Done, ADR-Vorlage, ADR-0001 (Entwurf).

**Entscheidungen (Christian)**
- Tests außerhalb des Pakets, damit Paket und Image nur Betriebscode enthalten.
- Fehlgeschlagene Checks blockieren den Merge in `main` (Branch Protection); Arbeit über Branch → PR.
- gitleaks von Anfang an, damit Secrets nicht unbemerkt ins Repo gelangen.

**Entscheidungen (Claude, auf Wunsch von Christian)**
- GitHub Actions per Commit-SHA gepinnt (Schutz gegen umgehängte Tags).

**Was nicht funktioniert hat**
- Erster CI-Lauf rot: `astral-sh/setup-uv@v10` existiert nicht, setup-uv veröffentlicht nur exakte Tags.
  Behoben durch SHA-Pinning.

**Offene Punkte**
- keine

**Stand bei Abschluss**
- `uv run pytest` läuft, CI grün (PR #1).
- ADR-0001 „Rolle und Grenzen“ akzeptiert.

## Arbeitsweise angepasst (2026-11-25)

**Entscheidung (Christian)**
- Kein PR-Ablauf mehr: Ruleset für `main` entfernt, Änderungen gehen direkt auf `main`.
  Grund: Fokus auf technisches Verständnis der KI-Use-Cases, nicht auf Entwickler-Workflow.
- CI (ruff, pytest, gitleaks) läuft weiter nach jedem Push auf `main`.
- Dependabot entfernt (würde wöchentlich PRs öffnen). Folge: Action-Versionen werden nicht automatisch aktualisiert.
- Routine-Tooling entscheidet Claude mit kurzer Begründung; Daten-, Architektur- und KI-Fragen entscheidet Christian.

## AP2 – Spike: Zugang und Mengen (2026-11-26) – fast abgeschlossen

**Ergebnis**
- Spike-Skript `spike/fetch_ai_tenders.py`: Suche (Seitenmodus) + XML je Bekanntmachung nach
  `data/raw/<datum>/<nummer>.xml`, Protokoll und Messwerte unter `data/runs/<zeitstempel>/`.
- 36 KI-Ausschreibungen (EU-27, 19.–25.11.2026), 0 % Fehler, 37 s Laufzeit. Details in `docs/spike-ted.md`.
- Frage B beantwortet: ca. 7 pro Veröffentlichungstag, Seitenmodus reicht.

**Entscheidungen (Christian)**
- Use Case gewechselt: KI-Ausschreibungen statt Tiefbau Oberbayern (ADR-0002, Entwurf).
- Filter: nur Ausschreibungen, alle EU-Länder, alle CPV, letzte 7 Tage, „KI“ in 24 Sprachen; Recall vor Precision.
- Rohdaten = vollständiges XML (nicht die Suchantwort), damit später neu gerechnet werden kann.

**Offene Punkte**
- Frage A: Abfrage in der TED-Expertensuche prüfen (Christian).
- ADR-0002 freigeben.
- Zielprofil des KMU für KI-Ausschreibungen festlegen (Planungsprojekt).
- 12 Sprachen ohne Treffer: andere Begriffe nötig? (AP3)
