# Spike TED – Ergebnisse

## AP2 – Zugang und Mengen (Lauf vom 2026-11-26)

### Filter (Entscheidung Christian, siehe ADR-0002)

- Nur Ausschreibungen: `notice-type IN (cn-standard)`
- Alle EU-27-Länder: `buyer-country IN (AUT BEL … SWE)`
- Alle CPV-Bereiche (KI hat keinen eigenen CPV-Code)
- Letzte 7 Tage: `publication-date>=… AND publication-date<=…` (bis einschließlich gestern)
- Volltext: „künstliche Intelligenz“ in allen 24 EU-Amtssprachen + „machine learning“ + „maschinelles Lernen“,
  verknüpft als `(FT~("…") OR FT~("…") OR …)`

Vollständige Abfrage: wird bei jedem Lauf unter `data/runs/<zeitstempel>/query.txt` gespeichert.
Skript: `spike/fetch_ai_tenders.py`.

### Messwerte

| Messgröße | Wert |
|---|---|
| Zeitraum | 2026-11-19 bis 2026-11-25 (7 Kalendertage, 5 Veröffentlichungstage) |
| Treffer (Ausschreibungen, EU-27) | **36** |
| Treffer pro Veröffentlichungstag | 4 / 9 / 13 / 5 / 5 (Montag 23.11. sammelt das Wochenende) |
| Ø pro Veröffentlichungstag | 7,2 |
| Seiten im Seitenmodus (250/Seite) | 1 |
| XML geladen | 36 von 36, alle wohlgeformt |
| Fehlerquote | 0 % (0 Fehler, 0 Wiederholungen) |
| Anfragen | 37 (1 Suche + 36 XML) |
| Laufzeit | 37,1 s (begrenzt durch 1 Anfrage/s) |
| Zweiter Lauf (bereits vorhanden) | 1 Anfrage, 0,7 s, 0 neue XML |
| Speicherbedarf Rohdaten | 3,8 MB für 36 XML (≈ 105 KB je Bekanntmachung) |
| Länder | PL 7, DE 6, ES 5, RO 5, FR 4, GR 3, BE/BG/CZ/IT/LT/PT je 1 |
| Ohne Länderfilter | 39 (zusätzlich 3 × Schweiz) |

### Frage A – Funktioniert eine Expert Query aus der TED-Webseite unverändert in der API?

_Offen – Prüfung durch Christian: Abfrage aus `query.txt` in https://ted.europa.eu/en/expert-search
einfügen und Trefferzahl mit 36 vergleichen._

### Frage B – Wie viele neue Bekanntmachungen pro Tag? Reicht der Seitenmodus?

Rund 7 Ausschreibungen pro Veröffentlichungstag, 36 pro Woche. Eine Seite (max. 250) reicht für eine
ganze Woche mit großem Abstand. Auch die Grenze von 15.000 abrufbaren Treffern ist weit entfernt.
**Der Seitenmodus reicht; der Iterationsmodus ist für diesen Filter nicht nötig.**

### Weitere Befunde

- **Stemming:** Gebeugte Formen liefern dieselben Trefferzahlen wie die Grundform
  (gemessen: de „künstliche/künstlicher Intelligenz“ 9/9, pl „sztuczna inteligencja/sztucznej inteligencji“ 8/8,
  ro mit/ohne diakritische Zeichen 8/8). Je Sprache reicht die Grundform.
- **Kurzbegriffe unbrauchbar:** `FT~("KI")` traf 11.088 von 20.765 Bekanntmachungen einer Woche,
  `FT~("AI")` 9.531 von 9.812 Ausschreibungen.
- **12 Sprachen ohne Treffer** in der Stichprobe (da, et, fi, ga, hr, hu, lv, mt, nl, sk, sl, sv).
  Ob das an fehlenden Ausschreibungen oder an anderen Begriffen liegt (z. B. Komposita), ist offen.
- **Rauschen:** Unter den Treffern sind Bekanntmachungen ohne KI-Bezug im Gegenstand
  (z. B. Umbau einer Werkhalle, Laptops), weil der Begriff irgendwo im Text vorkommt.
  Gewollt (Recall vor Precision); Filterung erfolgt nachgelagert.
- **Suchantwort ≠ Bekanntmachung:** Die Search API liefert nur angeforderte Felder.
  Vollständige Inhalte (Beschreibungen, Eignungs- und Zuschlagskriterien, Lose) stehen nur im XML
  (Beispiel 807412-2026: Suchantwort 8,7 KB, XML 36,8 KB mit 12 Beschreibungstexten).
- **TED ist nicht weltweit:** Nur EU/EWR und einige weitere Länder (z. B. CH).
