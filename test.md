# Evaluationsergebnisse — top_k = 10

Bewertungsskala Korrektheit / Vollständigkeit: `0` = falsch · `1` = teilweise · `2` = korrekt/vollständig · `-` = nicht bewertet

---

## Small Chunks (chunk_size=256, overlap=30)
Ingest:
    10727/10930 PDF-Chunks · 203 übersprungen
    340/341 URL-Chunks · 1 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | ja      |  13.1s  | 0.64      | 0.62    | richtig   | 1.00     | 1           | 2               |
| Q02 | ki_regelungen        | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q03 | ki_regelungen        | ja      |   8.7s  | 0.66      | 0.65    | richtig   | 0.33     | 2           | 1               |
| Q04 | ki_regelungen        | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q05 | ki_regelungen        | nein    |   0.2s  | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q06 | ki_regelungen        | nein    |   0.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |   0.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |   4.8s  | 0.65      | 0.63    | richtig   | 0.75     | 2           | 1               |
| Q09 | studienprogramme     | ja      |   9.1s  | 0.68      | 0.63    | richtig   | 1.00     | 1           | 1               |
| Q10 | studienprogramme     | ja      |   7.6s  | 0.68      | 0.62    | richtig   | 0.67     | 1           | 1               |
| Q11 | studienprogramme     | ja      |  17.4s  | 0.66      | 0.62    | richtig   | 0.25     | 1           | 1               |
| Q12 | studienprogramme     | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q13 | studienprogramme     | ja      |  16.4s  | 0.64      | 0.63    | richtig   | 1.00     | 0           | 1               |
| Q14 | studienprogramme     | ja      |  13.3s  | 0.65      | 0.63    | richtig   | 1.00     | 2           | 1               |
| Q15 | studienprogramme     | ja      |   5.9s  | 0.64      | 0.63    | richtig   | 0.50     | 1           | 0               |
| Q16 | studienprogramme     | ja      |   8.8s  | 0.65      | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q17 | studienprogramme     | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |  13.4s  | 0.62      | 0.62    | richtig   | 1.00     | 0           | 0               |
| Q19 | modulhandbuecher     | ja      |   6.0s  | 0.60      | 0.60    | richtig   | 0.50     | 0           | 2               |
| Q20 | modulhandbuecher     | nein    |   0.1s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q21 | modulhandbuecher     | ja      |   6.6s  | 0.70      | 0.65    | richtig   | 0.50     | 0           | 0               |
| Q22 | modulhandbuecher     | ja      |   8.8s  | 0.62      | 0.61    | richtig   | 0.50     | 1           | 0               |
| Q23 | modulhandbuecher     | ja      |  21.1s  | 0.63      | 0.61    | richtig   | 1.00     | 0           | 0               |
| Q24 | modulhandbuecher     | ja      |  10.4s  | 0.62      | 0.61    | richtig   | 0.75     | 0           | 0               |
| Q25 | modulhandbuecher     | ja      |   5.9s  | 0.60      | 0.60    | richtig   | 0.50     | 1           | 1               |
| Q26 | modulhandbuecher     | nein    |   0.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q27 | modulhandbuecher     | ja      |  10.5s  | 0.63      | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q28 | modulhandbuecher     | ja      |  10.1s  | 0.63      | 0.62    | richtig   | 0.75     | 0           | 0               |
| Q29 | studienprogramme     | ja      |  15.1s  | 0.67      | 0.65    | richtig   | 0.67     | 2           | 2               |
| Q30 | studienprogramme     | ja      |  10.9s  | 0.66      | 0.65    | richtig   | 0.67     | 1           | 1               |
| Q31 | studienprogramme     | ja      |  11.4s  | 0.71      | 0.65    | richtig   | 0.33     | 2           | 1               |
| Q32 | grenzfall            | nein    |   2.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | ja      |   3.2s  | 0.64      | 0.64    | falsch    | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |   3.2s  | 0.64      | 0.61    | falsch    | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |   0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |   0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q43 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

### Zusammenfassung nach Kategorie
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|-------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.26 |        0.65 |           1.5 / 2 |                1.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.60 |        0.66 |           1.0 / 2 |                1.0 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.53 |        0.63 |           0.0 / 2 |                0.0 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.64 |           2.0 / 2 |                2.0 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |           2.0 / 2 |                2.0 / 2 |

---

## Medium Chunks (chunk_size=512, overlap=50)
Ingest:
    5680/5720 PDF-Chunks · 40 übersprungen
    216/216 URL-Chunks · 0 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q02 | ki_regelungen        | nein    |   0.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q03 | ki_regelungen        | ja      |   6.1s  | 0.65      | 0.65    | richtig   | 0.00     | 2           | 1               |
| Q04 | ki_regelungen        | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q05 | ki_regelungen        | ja      |  10.5s  | 0.60      | 0.60    | richtig   | 0.67     | 0           | 0               |
| Q06 | ki_regelungen        | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |   0.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |   6.2s  | 0.64      | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q09 | studienprogramme     | ja      |   4.2s  | 0.67      | 0.62    | richtig   | 0.67     | 1           | 1               |
| Q10 | studienprogramme     | ja      |   4.3s  | 0.67      | 0.62    | richtig   | 0.67     | 2           | 1               |
| Q11 | studienprogramme     | ja      |  12.2s  | 0.72      | 0.64    | richtig   | 0.50     | 1           | 1               |
| Q12 | studienprogramme     | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q13 | studienprogramme     | ja      |  13.8s  | 0.64      | 0.61    | richtig   | 1.00     | 1           | 1               |
| Q14 | studienprogramme     | ja      |  16.7s  | 0.71      | 0.66    | richtig   | 1.00     | 2           | 1               |
| Q15 | studienprogramme     | ja      |   9.5s  | 0.63      | 0.62    | richtig   | 0.50     | 1           | 0               |
| Q16 | studienprogramme     | ja      |   8.4s  | 0.63      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q17 | studienprogramme     | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q18 | studienprogramme     | ja      |   9.9s  | 0.61      | 0.61    | richtig   | 1.00     | 0           | 0               |
| Q19 | modulhandbuecher     | ja      |   5.0s  | 0.65      | 0.62    | richtig   | 0.50     | 0           | 2               |
| Q20 | modulhandbuecher     | ja      |   5.0s  | 0.60      | 0.60    | richtig   | 1.00     | 0           | 0               |
| Q21 | modulhandbuecher     | ja      |   7.7s  | 0.66      | 0.65    | richtig   | 0.75     | 0           | 0               |
| Q22 | modulhandbuecher     | ja      |   5.2s  | 0.62      | 0.62    | richtig   | 0.50     | 1           | 0               |
| Q23 | modulhandbuecher     | ja      |  18.8s  | 0.64      | 0.62    | richtig   | 1.00     | 0           | 0               |
| Q24 | modulhandbuecher     | ja      |  11.0s  | 0.62      | 0.61    | richtig   | 0.50     | 0           | 0               |
| Q25 | modulhandbuecher     | ja      |  10.9s  | 0.61      | 0.61    | richtig   | 0.75     | 0           | 1               |
| Q26 | modulhandbuecher     | nein    |   2.4s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q27 | modulhandbuecher     | ja      |   4.9s  | 0.60      | 0.60    | richtig   | 0.75     | 2           | 2               |
| Q28 | modulhandbuecher     | nein    |   0.5s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q29 | studienprogramme     | ja      |   3.5s  | 0.67      | 0.63    | richtig   | 0.67     | 2           | 2               |
| Q30 | studienprogramme     | nein    |   0.1s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q31 | studienprogramme     | ja      |   4.0s  | 0.64      | 0.64    | richtig   | 1.00     | 1           | 1               |
| Q32 | grenzfall            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | ja      |   1.3s  | 0.62      | 0.62    | falsch    | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |   0.8s  | 0.62      | 0.62    | falsch    | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q43 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

### Zusammenfassung nach Kategorie
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|--------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.18 |        0.63 |            1.5 / 2 |                1.0 / 2 |
| studienprogramme     |     13 |      0.77 |     0.60 |        0.66 |            1.0 / 2 |                1.0 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.57 |        0.63 |            0.0 / 2 |                0.0 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.62 |            2.0 / 2 |                2.0 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                2.0 / 2 |

---

## Large Chunks (chunk_size=1024, overlap=100)
Ingest:
    2859/2865 PDF-Chunks · 6 übersprungen
    92/92 URL-Chunks · 0 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | nein    |   2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q02 | ki_regelungen        | nein    |   0.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q03 | ki_regelungen        | ja      |   8.1s  | 0.66      | 0.62    | richtig   | 0.33     | 2           | 2               |
| Q04 | ki_regelungen        | ja      |   5.4s  | 0.60      | 0.60    | richtig   | 0.67     | 2           | 2               |
| Q05 | ki_regelungen        | ja      |   3.6s  | 0.62      | 0.62    | richtig   | 1.00     | 2           | 2               |
| Q06 | ki_regelungen        | nein    |   0.1s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |   0.1s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |   2.6s  | 0.62      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q09 | studienprogramme     | ja      |   1.2s  | 0.66      | 0.62    | richtig   | 0.67     | 1           | 1               |
| Q10 | studienprogramme     | ja      |   1.5s  | 0.66      | 0.63    | richtig   | 0.67     | 1           | 1               |
| Q11 | studienprogramme     | ja      |   4.4s  | 0.73      | 0.68    | richtig   | 0.75     | 2           | 1               |
| Q12 | studienprogramme     | nein    |   0.1s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q13 | studienprogramme     | ja      |   4.4s  | 0.64      | 0.63    | richtig   | 0.67     | 2           | 1               |
| Q14 | studienprogramme     | ja      |   1.4s  | 0.71      | 0.65    | richtig   | 1.00     | 2           | 1               |
| Q15 | studienprogramme     | ja      |   1.7s  | 0.63      | 0.63    | richtig   | 0.50     | 0           | 0               |
| Q16 | studienprogramme     | ja      |   4.0s  | 0.62      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q17 | studienprogramme     | nein    |   0.1s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |   2.7s  | 0.62      | 0.61    | richtig   | 1.00     | 2           | 1               |
| Q19 | modulhandbuecher     | ja      |   3.7s  | 0.68      | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q20 | modulhandbuecher     | ja      |   3.3s  | 0.61      | 0.61    | richtig   | 1.00     | 0           | 0               |
| Q21 | modulhandbuecher     | ja      |   2.9s  | 0.67      | 0.66    | richtig   | 0.75     | 0           | 0               |
| Q22 | modulhandbuecher     | ja      |   1.9s  | 0.62      | 0.62    | richtig   | 0.50     | 1           | 0               |
| Q23 | modulhandbuecher     | ja      |   7.0s  | 0.65      | 0.64    | richtig   | 1.00     | 1           | 1               |
| Q24 | modulhandbuecher     | ja      |   3.5s  | 0.63      | 0.61    | richtig   | 0.25     | 0           | 0               |
| Q25 | modulhandbuecher     | ja      |   3.6s  | 0.64      | 0.62    | richtig   | 0.75     | 1           | 0               |
| Q26 | modulhandbuecher     | ja      |   5.9s  | 0.63      | 0.62    | richtig   | 0.75     | 1           | 1               |
| Q27 | modulhandbuecher     | ja      |   4.3s  | 0.60      | 0.60    | richtig   | 0.50     | 2           | 2               |
| Q28 | modulhandbuecher     | ja      |   4.7s  | 0.64      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q29 | studienprogramme     | ja      |   4.4s  | 0.65      | 0.64    | richtig   | 1.00     | 2           | 2               |
| Q30 | studienprogramme     | ja      |   3.8s  | 0.64      | 0.62    | richtig   | 0.67     | 1           | 1               |
| Q31 | studienprogramme     | ja      |   4.4s  | 0.64      | 0.62    | richtig   | 0.33     | 2           | 2               |
| Q32 | grenzfall            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |   0.8s  | 0.61      | 0.61    | falsch    | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q43 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

### Zusammenfassung nach Kategorie
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|--------------------|------------------------|
| ki_regelungen        |      8 |      0.50 |     0.34 |        0.62 |            2.0 / 2 |                2.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.62 |        0.66 |            2.0 / 2 |                1.0 / 2 |
| modulhandbuecher     |     10 |      1.00 |     0.70 |        0.64 |            1.0 / 2 |                0.5 / 2 |
| grenzfall            |      3 |      0.67 |     1.00 |        0.61 |            2.0 / 2 |                2.0 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                2.0 / 2 |









---


# Evaluationsergebnisse — top_k = 5

Bewertungsskala Korrektheit / Vollständigkeit: `0` = falsch · `1` = teilweise · `2` = korrekt/vollständig · `-` = nicht bewertet

---

## Small Chunks (chunk_size=256, overlap=30)
Ingest:
    10727/10930 PDF-Chunks · 203 übersprungen
    340/341 URL-Chunks · 1 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | ja      |   17.3s  | 0.64      | 0.62    | richtig   | 1.00     | 2           | 2               |
| Q02 | ki_regelungen        | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q03 | ki_regelungen        | ja      |    6.6s  | 0.66      | 0.65    | richtig   | 0.33     | 2           | 1               |
| Q04 | ki_regelungen        | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q05 | ki_regelungen        | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q06 | ki_regelungen        | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |    3.1s  | 0.65      | 0.63    | richtig   | 0.75     | 2           | 1               |
| Q09 | studienprogramme     | ja      |   10.1s  | 0.68      | 0.63    | richtig   | 0.83     | 1           | 1               |
| Q10 | studienprogramme     | ja      |    7.5s  | 0.68      | 0.63    | richtig   | 0.67     | 2           | 1               |
| Q11 | studienprogramme     | ja      |   15.8s  | 0.66      | 0.63    | richtig   | 0.75     | 2           | 0               |
| Q12 | studienprogramme     | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q13 | studienprogramme     | ja      |   11.9s  | 0.64      | 0.64    | richtig   | 0.67     | 0           | 0               |
| Q14 | studienprogramme     | ja      |   15.5s  | 0.65      | 0.64    | richtig   | 1.00     | 1           | 0               |
| Q15 | studienprogramme     | ja      |   11.7s  | 0.64      | 0.63    | richtig   | 0.50     | 0           | 0               |
| Q16 | studienprogramme     | ja      |   10.0s  | 0.65      | 0.63    | richtig   | 0.75     | 1           | 0               |
| Q17 | studienprogramme     | nein    |    2.3s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |    8.8s  | 0.62      | 0.62    | richtig   | 1.00     | 0           | 0               |
| Q19 | modulhandbuecher     | ja      |    6.2s  | 0.60      | 0.60    | richtig   | 0.50     | 1           | 0               |
| Q20 | modulhandbuecher     | nein    |    0.1s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q21 | modulhandbuecher     | ja      |   11.6s  | 0.70      | 0.66    | richtig   | 0.75     | 1           | 0               |
| Q22 | modulhandbuecher     | ja      |    9.9s  | 0.62      | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q23 | modulhandbuecher     | ja      |   15.7s  | 0.63      | 0.62    | richtig   | 1.00     | 1           | 0               |
| Q24 | modulhandbuecher     | ja      |    9.3s  | 0.62      | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q25 | modulhandbuecher     | ja      |    6.0s  | 0.60      | 0.60    | richtig   | 0.25     | 0           | 0               |
| Q26 | modulhandbuecher     | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q27 | modulhandbuecher     | ja      |   10.1s  | 0.63      | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q28 | modulhandbuecher     | ja      |   10.4s  | 0.63      | 0.62    | richtig   | 0.75     | 1           | 0               |
| Q29 | studienprogramme     | ja      |   11.6s  | 0.67      | 0.66    | richtig   | 0.67     | 0           | 0               |
| Q30 | studienprogramme     | ja      |   13.0s  | 0.66      | 0.65    | richtig   | 0.67     | 0           | 0               |
| Q31 | studienprogramme     | ja      |    5.4s  | 0.71      | 0.68    | richtig   | 0.33     | 2           | 1               |
| Q32 | grenzfall            | nein    |    0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | ja      |    2.5s  | 0.64      | 0.64    | falsch    | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |    2.7s  | 0.64      | 0.62    | falsch    | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |    0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |    0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q43 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

### Zusammenfassung nach Kategorie
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|-------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.26 |        0.65 |            1.5 / 2 |                 1.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.60 |        0.66 |              1 / 2 |                   0 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.50 |        0.63 |            1.0 / 2 |                 0.0 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.64 |              2 / 2 |                   2 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                 2.0 / 2 |

---

## Medium Chunks (chunk_size=512, overlap=50)
Ingest:
    5680/5720 PDF-Chunks · 40 übersprungen
    216/216 URL-Chunks · 0 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q02 | ki_regelungen        | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q03 | ki_regelungen        | ja      |   14.2s  | 0.65      | 0.65    | richtig   | 0.33     | 2           | 1               |
| Q04 | ki_regelungen        | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q05 | ki_regelungen        | ja      |   11.6s  | 0.60      | 0.60    | richtig   | 1.00     | 2           | 2               |
| Q06 | ki_regelungen        | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |    6.2s  | 0.64      | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q09 | studienprogramme     | ja      |    4.2s  | 0.67      | 0.62    | richtig   | 0.50     | 2           | 0               |
| Q10 | studienprogramme     | ja      |    3.4s  | 0.67      | 0.62    | richtig   | 0.67     | 1           | 0               |
| Q11 | studienprogramme     | ja      |   14.0s  | 0.72      | 0.66    | richtig   | 0.50     | 2           | 1               |
| Q12 | studienprogramme     | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q13 | studienprogramme     | ja      |   15.5s  | 0.64      | 0.62    | richtig   | 0.67     | 2           | 1               |
| Q14 | studienprogramme     | ja      |    6.5s  | 0.71      | 0.67    | richtig   | 1.00     | 2           | 1               |
| Q15 | studienprogramme     | ja      |    9.5s  | 0.63      | 0.62    | richtig   | 0.50     | 1           | 1               |
| Q16 | studienprogramme     | ja      |    9.5s  | 0.63      | 0.61    | richtig   | 0.75     | 1           | 1               |
| Q17 | studienprogramme     | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |    8.2s  | 0.61      | 0.61    | richtig   | 1.00     | 0           | 0               |
| Q19 | modulhandbuecher     | ja      |    6.9s  | 0.65      | 0.62    | richtig   | 0.50     | 1           | 0               |
| Q20 | modulhandbuecher     | ja      |    5.9s  | 0.60      | 0.60    | richtig   | 1.00     | 2           | 1               |
| Q21 | modulhandbuecher     | ja      |   17.8s  | 0.66      | 0.65    | richtig   | 0.75     | 0           | 0               |
| Q22 | modulhandbuecher     | ja      |    5.6s  | 0.62      | 0.62    | richtig   | 0.50     | 1           | 1               |
| Q23 | modulhandbuecher     | ja      |   16.3s  | 0.64      | 0.63    | richtig   | 1.00     | 1           | 0               |
| Q24 | modulhandbuecher     | ja      |   13.6s  | 0.62      | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q25 | modulhandbuecher     | ja      |   10.2s  | 0.61      | 0.61    | richtig   | 1.00     | 2           | 1               |
| Q26 | modulhandbuecher     | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q27 | modulhandbuecher     | ja      |   14.0s  | 0.60      | 0.60    | richtig   | 0.75     | 2           | 1               |
| Q28 | modulhandbuecher     | nein    |    2.3s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q29 | studienprogramme     | ja      |    4.9s  | 0.67      | 0.64    | richtig   | 0.67     | 2           | 2               |
| Q30 | studienprogramme     | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q31 | studienprogramme     | ja      |    9.1s  | 0.64      | 0.64    | richtig   | 1.00     | 1           | 1               |
| Q32 | grenzfall            | nein    |    2.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | ja      |    3.0s  | 0.62      | 0.62    | falsch    | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |    1.9s  | 0.62      | 0.62    | falsch    | 1.00     | 0           | 0               |
| Q36 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |    0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q43 | off_topic            | nein    |    0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |

### Zusammenfassung nach Kategorie
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|-------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.26 |        0.63 |            2.0 / 2 |                 1.5 / 2 |
| studienprogramme     |     13 |      0.77 |     0.56 |        0.66 |              1 / 2 |                   1 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.60 |        0.63 |            1.0 / 2 |                 0.5 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.62 |              2 / 2 |                   2 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                 2.0 / 2 |

---

## Large Chunks (chunk_size=1024, overlap=100)
Ingest:
    2859/2865 PDF-Chunks · 6 übersprungen
    92/92 URL-Chunks · 0 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | nein    |    2.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q02 | ki_regelungen        | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q03 | ki_regelungen        | ja      |   11.7s  | 0.66      | 0.62    | richtig   | 0.67     | 2           | 2               |
| Q04 | ki_regelungen        | ja      |    7.7s  | 0.60      | 0.60    | richtig   | 0.67     | 2           | 1               |
| Q05 | ki_regelungen        | ja      |    3.7s  | 0.62      | 0.62    | richtig   | 1.00     | 2           | 2               |
| Q06 | ki_regelungen        | nein    |    0.1s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |    0.1s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |    3.2s  | 0.62      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q09 | studienprogramme     | ja      |    1.4s  | 0.66      | 0.62    | richtig   | 0.67     | 2           | 1               |
| Q10 | studienprogramme     | ja      |    2.4s  | 0.66      | 0.63    | richtig   | 0.67     | 2           | 1               |
| Q11 | studienprogramme     | ja      |    4.3s  | 0.73      | 0.69    | richtig   | 0.25     | 2           | 1               |
| Q12 | studienprogramme     | nein    |    0.2s  | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q13 | studienprogramme     | ja      |    4.7s  | 0.64      | 0.63    | richtig   | 0.67     | 2           | 2               |
| Q14 | studienprogramme     | ja      |    1.7s  | 0.71      | 0.69    | richtig   | 1.00     | 2           | 1               |
| Q15 | studienprogramme     | ja      |    1.5s  | 0.63      | 0.63    | richtig   | 0.50     | 2           | 2               |
| Q16 | studienprogramme     | ja      |    4.9s  | 0.62      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q17 | studienprogramme     | nein    |    0.1s  | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |    2.9s  | 0.62      | 0.61    | richtig   | 1.00     | 2           | 2               |
| Q19 | modulhandbuecher     | ja      |    3.8s  | 0.68      | 0.65    | richtig   | 0.75     | 1           | 0               |
| Q20 | modulhandbuecher     | ja      |    3.6s  | 0.61      | 0.61    | richtig   | 1.00     | 2           | 1               |
| Q21 | modulhandbuecher     | ja      |    2.6s  | 0.67      | 0.66    | richtig   | 0.75     | 2           | 1               |
| Q22 | modulhandbuecher     | ja      |    1.7s  | 0.62      | 0.62    | richtig   | 0.50     | 1           | 1               |
| Q23 | modulhandbuecher     | ja      |    4.7s  | 0.65      | 0.64    | richtig   | 1.00     | 1           | 0               |
| Q24 | modulhandbuecher     | ja      |    3.0s  | 0.63      | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q25 | modulhandbuecher     | ja      |    3.0s  | 0.64      | 0.62    | richtig   | 0.75     | 0           | 0               |
| Q26 | modulhandbuecher     | ja      |    4.7s  | 0.63      | 0.62    | richtig   | 0.75     | 1           | 0               |
| Q27 | modulhandbuecher     | ja      |    3.1s  | 0.60      | 0.60    | richtig   | 1.00     | 2           | 2               |
| Q28 | modulhandbuecher     | ja      |    3.0s  | 0.64      | 0.61    | richtig   | 0.75     | 1           | 1               |
| Q29 | studienprogramme     | ja      |    3.7s  | 0.65      | 0.65    | richtig   | 1.00     | 2           | 2               |
| Q30 | studienprogramme     | ja      |    3.4s  | 0.64      | 0.62    | richtig   | 0.67     | 2           | 2               |
| Q31 | studienprogramme     | ja      |    2.7s  | 0.64      | 0.64    | richtig   | 0.67     | 2           | 2               |
| Q32 | grenzfall            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |    0.9s  | 0.61      | 0.61    | falsch    | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q43 | off_topic            | nein    |    0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

### Zusammenfassung nach Kategorie
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|-------------------|------------------------|
| ki_regelungen        |      8 |      0.50 |     0.39 |        0.62 |            2.0 / 2 |                 2.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.60 |        0.66 |              2 / 2 |                   2 / 2 |
| modulhandbuecher     |     10 |      1.00 |     0.78 |        0.64 |            1.0 / 2 |                 1.0 / 2 |
| grenzfall            |      3 |      0.67 |     1.00 |        0.61 |              2 / 2 |                   2 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                 2.0 / 2 |

---
























