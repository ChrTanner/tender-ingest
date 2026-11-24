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
- GitHub Actions per Commit-SHA gepinnt (Schutz gegen umgehängte Tags), Updates per Dependabot (wöchentlich).

**Was nicht funktioniert hat**
- Erster CI-Lauf rot: `astral-sh/setup-uv@v10` existiert nicht, setup-uv veröffentlicht nur exakte Tags.
  Behoben durch SHA-Pinning.

**Offene Punkte**
- Branch Protection (Ruleset für `main`): Wirksamkeit mit dem PR zu ADR-0001 prüfen.

**Stand bei Abschluss**
- `uv run pytest` läuft, CI grün (PR #1).
- ADR-0001 „Rolle und Grenzen“ akzeptiert.
