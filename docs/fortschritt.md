# Fortschritt tender-ingest

## AP1 – Repo-Grundgerüst (2026-11-24)

**Ergebnis**
- uv-Paket `src/tender_ingest/`, Python 3.14, Build-Backend `uv_build`.
- Tests in `tests/` neben `src/` (Smoke-Test). ruff (Lint + Format) und pytest als Dev-Abhängigkeiten.
- CI (GitHub Actions): ruff check, ruff format --check, pytest, gitleaks.
- README-Gerüst nach Definition of Done, ADR-Vorlage, ADR-0001 (Entwurf).

**Entscheidungen (Christian)**
- Tests außerhalb des Pakets, damit Paket und Image nur Betriebscode enthalten.
- Fehlgeschlagene Checks blockieren den Merge in `main` (Branch Protection); Arbeit über Branch → PR.
- gitleaks von Anfang an, damit Secrets nicht unbemerkt ins Repo gelangen.

**Offene Punkte**
- Branch Protection für `main` in GitHub einrichten (nach dem ersten CI-Lauf).
- ADR-0001 freigeben.
- CI grün bestätigen.
