# ADR-0002: Filter – KI-Ausschreibungen in der EU

- Status: Entwurf (Freigabe durch Christian offen)
- Datum: 2026-11-26
- Entscheider: Christian

## Kontext

Für den Spike (AP2) braucht tender-ingest einen konkreten Filter. Erster Ansatz war Tiefbau in Oberbayern
bis 2 Mio € (`place-of-performance IN (DE21)`, CPV 45). Eine Stichprobe zeigte: Nur 3 von 51 Ausschreibungen
nennen einen geschätzten Wert, und Bauaufträge unter dem EU-Schwellenwert erscheinen auf TED meist nur als Lose.
Christian hat den Use Case daraufhin auf KI-Ausschreibungen umgestellt.

## Optionen

1. **Tiefbau Oberbayern bis 2 Mio €** – sauber per CPV und NUTS filterbar; Wertgrenze kaum anwendbar,
   kleine Aufträge selten auf TED.
2. **KI-Ausschreibungen, eng** – wenige Sprachen/Begriffe oder IT-CPV (72, 48); weniger Rauschen,
   verpasst Treffer (z. B. KI in Labor- oder Medizintechnik, CPV 38/33).
3. **KI-Ausschreibungen, breit** – alle 24 Sprachen, alle CPV; mehr Rauschen, das nachgelagert gefiltert wird.

## Entscheidung

Option 3. KI-Ausschreibungen ersetzen das Tiefbau-Szenario.

- Nur Ausschreibungen (`cn-standard`), alle EU-27-Länder, alle CPV-Bereiche, letzte 7 Tage.
- Volltextsuche nach „künstliche Intelligenz“ in allen 24 EU-Amtssprachen plus „machine learning“ /
  „maschinelles Lernen“.
- Recall vor Precision: Lieber mehr Treffer mit Rauschen, das später ausgefiltert werden kann,
  als passende Ausschreibungen zu verpassen.
- Rohdaten sind das vollständige XML je Bekanntmachung (die Suchantwort enthält nur ausgewählte Felder).

## Folgen

- Rund 7 Treffer pro Veröffentlichungstag (Messung siehe `docs/spike-ted.md`); Seitenmodus reicht.
- Nachgelagert ist eine Relevanzprüfung nötig (z. B. Klassifikation mit einem LLM), weil die Stichwortsuche
  auch Bekanntmachungen ohne KI-Gegenstand findet. Das gehört nicht in tender-ingest.
- Das ändert den Fokus des Gesamtsystems Tender-Copilot (Zielgruppe: Anbieter von KI-Leistungen statt Tiefbau).
  Zielprofil des KMU ist noch offen.
- „Weltweit“ ist mit TED nicht abgedeckt (nur EU/EWR und einige weitere Länder).
