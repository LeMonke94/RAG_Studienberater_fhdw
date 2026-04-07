# RAG-Studienberater

RAG-basiertes Frage-Antwort-System für FHDW-Studienberatung.

---

## Inhaltsverzeichnis

1. [Technologieauswahl](#technologieauswahl)
2. [Projektstruktur](#projektstruktur)
3. [Architekturbeschreibung](#architekturbeschreibung)
4. [Prozessablauf und Kommunikation zwischen den Komponenten](#prozessablauf-und-kommunikation-zwischen-den-komponenten)
5. [Evaluationsmethodik und Ergebnisse](#evaluationsmethodik-und-ergebnisse)
6. [Diskussion und Lessons Learned](#diskussion-und-lessons-learned)
7. [Installationsanleitung](#installationsanleitung)

---

## Technologieauswahl

| Technologie       | Paket                      | Zweck                                          |
|-------------------|----------------------------|------------------------------------------------|
| Laufzeitumgebung  | Python 3.11+               | Basis des Gesamtprojekts                       |
| LLM (lokal)       | qwen2.5:7b via Ollama      | Generiert die Antworten                        |
| Embedding         | bge-m3 via Ollama          | Wandelt Text in Vektoren um                    |
| Text-Splitting    | langchain-text-splitters   | Teilt Dokumente in Chunks auf                  |
| LLM-Integration   | langchain-ollama           | Verbindet die Pipeline mit Ollama              |
| Vektordatenbank   | Qdrant                     | Speichert Chunks und Vektoren                  |
| PDF-Extraktion    | pdfplumber                 | Extrahiert Text aus PDFs                       |
| Web-Scraping      | BeautifulSoup4 + requests  | Extrahiert Text aus FHDW-Webseiten             |
| User Interface    | Streamlit                  | Chat-Interface                                 |
| Konfiguration     | pydantic-settings          | Typsichere Verwaltung von Einstellungen        |
| Testing           | pytest                     | Automatisierte Unit-Tests                      |
| Code-Qualität     | ruff                       | Linting und automatische Formatierung          |
| Typ-Prüfung       | mypy                       | Statische Typprüfung                           |
| Projektdefinition | pyproject.toml             | Metadaten, Abhängigkeiten, Tool-Konfiguration  |

Begründung der zentralen Entscheidungen:
- **Ollama (lokal)** statt Cloud-API: Volle Datenkontrolle, keine laufenden API-Kosten, reproduzierbare Ergebnisse ohne Netzabhängigkeit.
- **Qdrant** als Vektordatenbank: Unterstützt Cosine-Similarity, bietet Cloud- und lokalen Betrieb, stabile Python-Bibliothek.
- **bge-m3** als Embedding-Modell: Mehrsprachiges Modell mit 1024-dimensionalen Vektoren, gut geeignet für deutschen Fachtext.
- **qwen2.5:7b** als LLM: Gutes Verhältnis aus Antwortqualität und lokaler Laufzeit auf Consumer-Hardware.
- **Streamlit** als UI: Schnelle Prototypen-Entwicklung ohne separates Frontend-Framework.

---

## Projektstruktur

RAG_STUDIENBERATER/
|
├──data/
│   ├──evaluation/
|   |   ├──top_k_5/
|   |   |   ├──sweep_large.json
|   |   |   ├──sweep_medium.json
|   |   |   └──sweep_small.json
|   |   ├──top_k_10/
|   |   |   ├──sweep_large.json
|   |   |   ├──sweep_medium.json
|   |   |   └──sweep_small.json
|   |   └──testset.json
│   └──raw/
|       ├──pdf/
|       |   ├──Modulhandbuecher/
|       |   |   └──...
|       |   ├──Studienprogramme
|       |   |   └──...
|       |   └──Regelungen zur Nutzung von KI-Tools 2025 03 31.pdf
|       └──web/
|           └──url.json
|
├──scripts/
│   ├──evaluate.py
│   ├──parameter_swep.py
│   └──smoke_test.py
|
├──src/
│   ├──rag_studienberater/
|   |   |
|   |   ├──application/
|   |   |   ├──services/
|   |   |   |   ├──__init__.py
|   |   |   |   ├──chunking_service.py
|   |   |   |   ├──grounding_service.py
|   |   |   |   ├──guardrail_service.py
|   |   |   |   ├──retrieval_service.py
|   |   |   |   └──text_cleaner_service.py
|   |   |   ├──use_cases/
|   |   |   |   ├──__init__.py
|   |   |   |   ├──answer_use_case.py
|   |   |   |   ├──ingest_use_case.py
|   |   |   |   └──retrieval_use_case.py
|   |   |   └──__init__.py
|   |   |
|   |   ├──bootstrap/
|   |   |   ├──__init__.py
|   |   |   └──container.py
|   |   |
|   |   ├──config/
|   |   |   ├──__init__.py
|   |   |   ├──logging_config.py
|   |   |   └──settings.py
|   |   |
|   |   ├──domain/
|   |   |   ├──models/
|   |   |   |   ├──__init__.py
|   |   |   |   ├──answer.py
|   |   |   |   ├──chunk.py
|   |   |   |   ├──document.py
|   |   |   |   ├──page.py
|   |   |   |   ├──query.py
|   |   |   |   ├──retrieval_result.py
|   |   |   |   └──scored_chunk.py
|   |   |   ├──ports/
|   |   |   |   ├──__init__.py
|   |   |   |   ├──document_loader_port.py
|   |   |   |   ├──embedding_port.py
|   |   |   |   ├──language_model_port.py
|   |   |   |   ├──text_splitter_port.py
|   |   |   |   └──vector_store_port.py
|   |   |   └──__init__.py
|   |   |
|   |   ├──infrastructure/
|   |   |   ├──document_loaders/
|   |   |   |   ├──__init__.py
|   |   |   |   ├──pdf_loader.py
|   |   |   |   ├──routing_document_loader.py
|   |   |   |   └──web_loader.py
|   |   |   ├──embedding_models/
|   |   |   |   ├──__init__.py
|   |   |   |   └──ollama_embedding_model.py
|   |   |   ├──language_models/
|   |   |   |   ├──__init__.py
|   |   |   |   └──ollama_language_model.py
|   |   |   ├──text_splitters/
|   |   |   |   ├──__init__.py
|   |   |   |   └──langchain_text_splitter.py
|   |   |   ├──vectore_stores/
|   |   |   |   ├──__init__.py
|   |   |   |   └──qdrant_vector_store.py
|   |   |   └──__init__.py
|   |   |
|   |   ├──presentation/
|   |   |   ├──components/
|   |   |   |   ├──__init__.py
|   |   |   |   ├──chat.py
|   |   |   |   └──sidebar.py
|   |   |   ├──__init__.py
|   |   |   ├──app.py
|   |   |   └──state.py
|   |   |
|   |   └──__init__.py
|   |
|   └──rag_studienberater.egg-info/
|       └──...
|
├──tests/
|   ├──unit/
|   |   ├──services/
|   |   |   ├──__init__.py
|   |   |   ├──test_chunking_service.py
|   |   |   ├──test_grounding_service.py
|   |   |   ├──test_guardrail_service.py
|   |   |   ├──test_retrieval_service.py
|   |   |   └──test_text_cleaner_service.py
|   |   ├──use_cases/
|   |   |   ├──__init__.py
|   |   |   ├──test_answer_use_case.py
|   |   |   ├──test_ingest_use_case.py
|   |   |   └──test_retrieval_use_case.py
|   |   └──__init__.py
|   ├──__init__.py
|   └──conftest.py
|
├──.env
├──.env.example
├──.gitignore
├──pyproject.toml
└──README.md

---

## Architekturbeschreibung

Die Anwendung ist nach den Prinzipien der **Clean Architecture** strukturiert und folgt einem schichtenbasierten Aufbau 
mit klarer Trennung von Präsentation, Anwendung, Domäne und Infrastruktur. Die Kernlogik ist über **Hexagonal Architecture**
entkoppelt, indem Schnittstellen (Ports) in der Domäne definiert und durch Infrastrukturkomponenten (Adapter) implementiert werden.
Fachliche Konzepte werden nach **DDD** (Domain-Driven Design) modelliert und durch Use Cases orchestriert. Funktional bildet das 
System eine RAG-Pipeline zur Verarbeitung, Retrieval und Generierung von Antworten auf Basis gegebener Wissensquellen.

┌─────────────────────────────────────────────────────┐
│                   Presentation                      │
│              Streamlit Chat-Interface               │
└────────────────────────┬────────────────────────────┘
                         │
┌───────────────────────────────────────────────────────────────────┐
│                   Application                                     │
│ Use Cases: AnswerUseCase, IngestUseCase, RetrievalUseCase         │
│ Services:  Chunking, Grounding, Guardrail, Retrieval, TextCleaner │
└────────┬──────────────────────────────────┬───────────────────────┘
         │                                  │
┌───────────────────┐        ┌─────────────────────────────┐
│      Domain       │        │       Infrastructure        │
│  Models & Ports   │        │  Qdrant, Ollama, Langchain  │
│  (keine Deps)     │        │  pdfplumber, BS4            │
└───────────────────┘        └─────────────────────────────┘

---

### Gesamtübersicht
| Schicht                | Beschreibung                                                       |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Application-Schicht    | Orchestriert die Ablauflogik der Anwendung und kommuniziert ausschließlich über definierte Schnittstellen mit externen Komponenten |
| Bootstrap              | Das Bootstrap-Modul initialisiert die Anwendung und sorgt für die zentrale Bereitstellung aller Komponenten                        |
| Config                 | Die Config-Schicht kapselt alle konfigurierbaren Parameter und trennt diese von der Geschäftslogik                                 |
| Domain                 | Die Domain-Schicht ist vollständig unabhängig von technischen Details und bildet die fachliche Grundlage des Systems               |
| Infrastructure-Schicht | Die Infrastructure-Schicht implementiert die in der Domain definierten Schnittstellen und kapselt alle externen Technologien       |
| Presentation-Schicht   | Die Presentation-Schicht übernimmt die Interaktion mit dem Benutzer und delegiert die Verarbeitung an die Application-Schicht      |

---

### Application-Schicht
| Bestandteil | Beschreibung                                                                                                                                  |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Services    | Kapseln wiederverwendbare Verarbeitungslogik und stellen diese den Use Cases als Bausteine zur Verfügung                                      |
| Use Cases   | Orchestrieren den Ablauf der Anwendungsfälle, indem sie Services koordinieren und über definierte Ports mit externen Komponenten interagieren |

---

### Bootstrap
| Bestandteil | Beschreibung                                                       |
|-------------|--------------------------------------------------------------------|
| Container   | Erstellt und verdrahtet alle Abhängigkeiten (Dependency Injection) |

---

### Config
| Bestandteil | Beschreibung                                                       |
|-------------|--------------------------------------------------------------------|
| Settings    | Verwaltet Umgebungsvariablen und Konfigurationen                   |
| Logging     | Konfiguriert das Logging der Anwendung                             |

---

### Domain-Schicht
| Bestandteil | Beschreibung                                                   |
|-------------|----------------------------------------------------------------|
| Modelle     | Repräsentieren die fachlichen Kernobjekte                      |
| Ports       | Definieren abstrakte Schnittstellen für externe Abhängigkeiten |

---

### Infrastructure-Schicht
| Bestandteil       | Beschreibung                                                       |
|-------------------|--------------------------------------------------------------------|
| Document Loader   | Laden und extrahieren Inhalte aus verschiedenen Quellen (PDF, Web) |
| Embedding-Modelle | Erzeugen Vektorrepräsentationen von Texten                         |
| Language-Modelle  | Generieren Antworten basierend auf den bereitgestellten Kontexten  |
| Vector Store      | Speichern und durchsuchen Vektoren für das Retrieval (Qdrant)      |
| Text Splitter     | Zerlegen Dokumente in kleinere Einheiten (Chunks)                  |

---

### Presentation-Schicht
| Bestandteil | Beschreibung                                                        |
|-------------|---------------------------------------------------------------------|
| Components  | Stellen interaktive Elemente wie Chat und Sidebar bereit            |
| App         | Einstiegspunkt der Anwendung und Verbindung zur Application-Schicht |
| State       | Verwaltet den Zustand der Benutzerinteraktion                       |

---

## Prozessablauf und Kommunikation zwischen den Komponenten

### Ingest-Pipeline
Dokumente werden einmalig verarbeitet und im Vektorspeicher abgelegt:

```
Datei / URL
    │
    ▼
IngestUseCase
    ├──loader.load(source)                          - lädt die Quelle als Document
    |       -> Document (Pages)
    |
    ├──text_cleaner_service.clean(page.text)        - bereinigt den Text jeder Seite
    |       -> bereinigte Pages
    |
    ├──chunking_service.chunk_document(document)    - zerlegt das Dokument in Chunks
    |       -> list[Chunk]
    |
    ├──[len(c.text.strip()) >= 20]                  - filtert Chunks mit zu wenig Inhalt
    |       -> list[Chunk]
    |
    ├──embedder.embed_documents([chunk.text])       - erzeugt Vektoren für einzelne Chunks
    |       -> list[list[float]]
    |
    ├──[math.isfinite(v) für alle v im Vektor]      - verwirft Vektoren mit NaN/Inf-Werten
    |       -> Chunks + Vectors
    |
    └──vector_store.add_chunks(chunks, vectors)     - speichert Chunks und Vektoren im Vektorspeicher
```

---

### Retrieval-Pipeline
```
Query/Frage
    |
    ▼
RetrievalUseCase
    |
    └──retrieval_service.retrieve(query, top_k)      - Retrieval Service wird aufgerufen
        ├──embedder.embed_query(query.text)          - erzeugt eine Vektorrepräsentation der Anfrage
        |       -> list[float]
        |
        ├──vector_store.search(vector, top_k)      - sucht die ähnlichsten Chunks im Vektorspeicher
        |       -> list[ScoredChunk]
        |
        └──RetrievalResult                         - bündelt die gefundenen Chunks mit Scores
```

---

### Answer-Pipeline
Nutzerfrage (str)
    |
    ▼
AnswerUseCase
    ├── guardrail_service.is_question_valid(question)     - prüft, ob die Frage ausreichend konkret ist
    |       -> wenn ungültig: Hinweisantwort
    |
    ├──Query(question)                                    - wandelt die Eingabe in ein Domänenobjekt um
    |       -> Query
    |
    ├──retrieval_use_case.execute(query)                  - führt die Retrieval-Pipeline aus
    |       -> RetrievalResult
    |
    ├──guardrail_service.has_sufficient_evidence(result)  - prüft, ob ausreichend Evidenz vorhanden ist
    |       -> wenn keine Evidenz: Hinweisantwort
    |
    ├──guardrail_service.filter_chunks(result)            - entfernt Chunks unterhalb des Mindestschwellwerts
    |       -> gefiltertes RetrievalResult
    |
    ├──grounding_service.build_prompt(query, filtered)    - erstellt einen kontextbasierten Prompt
    |       -> Prompt
    |
    ├──language_model.generate(prompt)                    - generiert die finale Antwort
    |       -> Antworttext
    |
    ├──Answer(text, sources, has_evidence)
    |       -> Erzeugt das Rückgabeobjekt
    |
    ▼
Presentation-Schicht                                      - zeigt Antwort und Quellen in der UI

---

## Guardrail-Logik 

Die Guardrail-Logik stellt sicher, dass nur valide Nutzeranfragen verarbeitet werden und dass generierte Antworten
auf ausreichender inhaltlicher Grundlage basieren. Damit werden fehlerhafte ungenaue und unbegründete Antworten
vermieden.

GuardrailService erfüllt drei Aufgaben:
1. **Eingabevalidierung** - Fragen unter 10 Zeichen werden direkt abgelehnt.
2. **Evidenzprüfung** - Mindestens ein Chunk muss den **min_score**-Schwellenwert erreichen, sonst wird keine Antwort generiert.
3. **Kontextfilterung** - Alle Chunks unter **min_score** werden vor der Prompt-Erstellung entfernt, damit das LLM nur hochrelevante Informationen bekommt.

---

## Grounding-Prompt:
```
Du bist ein hilfreicher Studienberater der FHDW.
Beantworte die Frage ausschließlich auf Basis der folgenden Informationen
aus den FHDW-Unterlagen. Wenn die Informationen nicht ausreichen, sage
das ehrlich. Gib am Ende immer die Quellen an.

INFORMATIONEN AUS DEN UNTERLAGEN:
[Quelle 1: <Dateiname>, Seite <n>]
<Chunk-Text>
...

FRAGE:
<Nutzerfrage>

ANTWORT:
```

---

## Evaluationsmethodik und Ergebnisse

### Testset
Das Testset umfasst **42 Fragen** in fünf Kategorien, die auf den tatsächlichen Quelldokumenten basieren:

| Kategorie          | Anzahl | Erwartet Antwort | Beschreibung                                     |
|--------------------|--------|------------------|--------------------------------------------------|
| `ki_regelungen`    | 8      | ja               | Fragen zur FHDW KI-Nutzungsregelung              |
| `studienprogramme` | 13     | ja               | Studiengangs-, Bewerbungs- und Kostenfragen      |
| `modulhandbuecher` | 10     | ja               | Fragen zu Modulinhalten, ECTS, Prüfungsformen    |
| `grenzfall`        | 3      | nein             | FHDW-nah, aber nicht in den Dokumenten enthalten |
| `off_topic`        | 8      | nein             | Vollständig themenfremde Fragen                  |

### Metriken
Automatisch gemessen:
- **Guardrail-Korrektheit** — Hat das System geantwortet, wenn eine Antwort erwartet wurde, und geschwiegen, wenn nicht?
- **Keyword-Recall** — Anteil der erwarteten Schlüsselwörter, die in der Antwort vorkommen.
- **Top-Score / Avg-Score** — Cosine-Ähnlichkeit des besten bzw. durchschnitt aller verwendeten Chunks.
- **Laufzeit** — Antwortzeit pro Frage.

Manuell bewertet (Skala: 0 = falsch · 1 = teilweise · 2 = korrekt):
- **Korrektheit** — Ist der Inhalt der Antwort sachlich richtig?
- **Vollständigkeit** — Werden alle relevanten Aspekte der Frage abgedeckt?

---

### Evaluationsergebnisse

#### top_k = 5:

**Small Chunks (chunk_size=256, overlap=30)**
Ingest:
    10727/10930 PDF-Chunks · 203 übersprungen
    340/341 URL-Chunks · 1 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | ja      |   17.3s  | 0.64     | 0.62    | richtig   | 1.00     | 2           | 2               |
| Q02 | ki_regelungen        | nein    |    2.2s  | -        | -       | falsch    | 0.00     | 1           | 1               |
| Q03 | ki_regelungen        | ja      |    6.6s  | 0.66     | 0.65    | richtig   | 0.33     | 2           | 1               |
| Q04 | ki_regelungen        | nein    |    2.2s  | -        | -       | falsch    | 0.00     | 0           | 0               |
| Q05 | ki_regelungen        | nein    |    0.2s  | -        | -       | falsch    | 0.00     | 0           | 0               |
| Q06 | ki_regelungen        | nein    |    0.2s  | -        | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |    0.2s  | -        | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |    3.1s  | 0.65     | 0.63    | richtig   | 0.75     | 2           | 1               |
| Q09 | studienprogramme     | ja      |   10.1s  | 0.68     | 0.63    | richtig   | 0.83     | 1           | 1               |
| Q10 | studienprogramme     | ja      |    7.5s  | 0.68     | 0.63    | richtig   | 0.67     | 2           | 1               |
| Q11 | studienprogramme     | ja      |   15.8s  | 0.66     | 0.63    | richtig   | 0.75     | 2           | 0               |
| Q12 | studienprogramme     | nein    |    2.2s  | -        | -       | falsch    | 0.00     | 2           | 2               |
| Q13 | studienprogramme     | ja      |   11.9s  | 0.64     | 0.64    | richtig   | 0.67     | 0           | 0               |
| Q14 | studienprogramme     | ja      |   15.5s  | 0.65     | 0.64    | richtig   | 1.00     | 1           | 0               |
| Q15 | studienprogramme     | ja      |   11.7s  | 0.64     | 0.63    | richtig   | 0.50     | 0           | 0               |
| Q16 | studienprogramme     | ja      |   10.0s  | 0.65     | 0.63    | richtig   | 0.75     | 1           | 0               |
| Q17 | studienprogramme     | nein    |    2.3s  | -        | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |    8.8s  | 0.62     | 0.62    | richtig   | 1.00     | 0           | 0               |
| Q19 | modulhandbuecher     | ja      |    6.2s  | 0.60     | 0.60    | richtig   | 0.50     | 1           | 0               |
| Q20 | modulhandbuecher     | nein    |    0.1s  | -        | -       | falsch    | 0.00     | 0           | 0               |
| Q21 | modulhandbuecher     | ja      |   11.6s  | 0.70     | 0.66    | richtig   | 0.75     | 1           | 0               |
| Q22 | modulhandbuecher     | ja      |    9.9s  | 0.62     | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q23 | modulhandbuecher     | ja      |   15.7s  | 0.63     | 0.62    | richtig   | 1.00     | 1           | 0               |
| Q24 | modulhandbuecher     | ja      |    9.3s  | 0.62     | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q25 | modulhandbuecher     | ja      |    6.0s  | 0.60     | 0.60    | richtig   | 0.25     | 0           | 0               |
| Q26 | modulhandbuecher     | nein    |    0.2s  | -        | -       | falsch    | 0.00     | 0           | 0               |
| Q27 | modulhandbuecher     | ja      |   10.1s  | 0.63     | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q28 | modulhandbuecher     | ja      |   10.4s  | 0.63     | 0.62    | richtig   | 0.75     | 1           | 0               |
| Q29 | studienprogramme     | ja      |   11.6s  | 0.67     | 0.66    | richtig   | 0.67     | 0           | 0               |
| Q30 | studienprogramme     | ja      |   13.0s  | 0.66     | 0.65    | richtig   | 0.67     | 0           | 0               |
| Q31 | studienprogramme     | ja      |    5.4s  | 0.71     | 0.68    | richtig   | 0.33     | 2           | 1               |
| Q32 | grenzfall            | nein    |    0.2s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | ja      |    2.5s  | 0.64     | 0.64    | falsch    | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |    2.7s  | 0.64     | 0.62    | falsch    | 1.00     | 2           | 2               |
| Q35 | off_topic            | nein    |    0.1s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |    0.1s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |    0.1s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |    0.2s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |    0.2s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |    0.1s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |    0.1s  | -        | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |    0.1s  | -        | -       | richtig   | 1.00     | 2           | 2               |

**Zusammenfassung nach Kategorie**
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|--------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.26 |        0.65 |            1.5 / 2 |                1.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.60 |        0.66 |              1 / 2 |                  0 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.50 |        0.63 |            1.0 / 2 |                0.0 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.64 |              2 / 2 |                  2 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                2.0 / 2 |

---

**Medium Chunks (chunk_size=512, overlap=50)**
Ingest:
    5680/5720 PDF-Chunks · 40 übersprungen
    216/216 URL-Chunks · 0 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | nein    |    2.2s | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q02 | ki_regelungen        | nein    |    0.2s | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q03 | ki_regelungen        | ja      |   14.2s | 0.65      | 0.65    | richtig   | 0.33     | 2           | 1               |
| Q04 | ki_regelungen        | nein    |    2.2s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q05 | ki_regelungen        | ja      |   11.6s | 0.60      | 0.60    | richtig   | 1.00     | 2           | 2               |
| Q06 | ki_regelungen        | nein    |    2.2s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |    0.2s | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |    6.2s | 0.64      | 0.63    | richtig   | 0.75     | 2           | 2               |
| Q09 | studienprogramme     | ja      |    4.2s | 0.67      | 0.62    | richtig   | 0.50     | 2           | 0               |
| Q10 | studienprogramme     | ja      |    3.4s | 0.67      | 0.62    | richtig   | 0.67     | 1           | 0               |
| Q11 | studienprogramme     | ja      |   14.0s | 0.72      | 0.66    | richtig   | 0.50     | 2           | 1               |
| Q12 | studienprogramme     | nein    |    2.2s | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q13 | studienprogramme     | ja      |   15.5s | 0.64      | 0.62    | richtig   | 0.67     | 2           | 1               |
| Q14 | studienprogramme     | ja      |    6.5s | 0.71      | 0.67    | richtig   | 1.00     | 2           | 1               |
| Q15 | studienprogramme     | ja      |    9.5s | 0.63      | 0.62    | richtig   | 0.50     | 1           | 1               |
| Q16 | studienprogramme     | ja      |    9.5s | 0.63      | 0.61    | richtig   | 0.75     | 1           | 1               |
| Q17 | studienprogramme     | nein    |    2.2s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |    8.2s | 0.61      | 0.61    | richtig   | 1.00     | 0           | 0               |
| Q19 | modulhandbuecher     | ja      |    6.9s | 0.65      | 0.62    | richtig   | 0.50     | 1           | 0               |
| Q20 | modulhandbuecher     | ja      |    5.9s | 0.60      | 0.60    | richtig   | 1.00     | 2           | 1               |
| Q21 | modulhandbuecher     | ja      |   17.8s | 0.66      | 0.65    | richtig   | 0.75     | 0           | 0               |
| Q22 | modulhandbuecher     | ja      |    5.6s | 0.62      | 0.62    | richtig   | 0.50     | 1           | 1               |
| Q23 | modulhandbuecher     | ja      |   16.3s | 0.64      | 0.63    | richtig   | 1.00     | 1           | 0               |
| Q24 | modulhandbuecher     | ja      |   13.6s | 0.62      | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q25 | modulhandbuecher     | ja      |   10.2s | 0.61      | 0.61    | richtig   | 1.00     | 2           | 1               |
| Q26 | modulhandbuecher     | nein    |    2.2s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q27 | modulhandbuecher     | ja      |   14.0s | 0.60      | 0.60    | richtig   | 0.75     | 2           | 1               |
| Q28 | modulhandbuecher     | nein    |    2.3s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q29 | studienprogramme     | ja      |    4.9s | 0.67      | 0.64    | richtig   | 0.67     | 2           | 2               |
| Q30 | studienprogramme     | nein    |    0.2s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q31 | studienprogramme     | ja      |    9.1s | 0.64      | 0.64    | richtig   | 1.00     | 1           | 1               |
| Q32 | grenzfall            | nein    |    2.2s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | ja      |    3.0s | 0.62      | 0.62    | falsch    | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |    1.9s | 0.62      | 0.62    | falsch    | 1.00     | 0           | 0               |
| Q35 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |    0.2s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |    0.2s | -         | -       | richtig   | 1.00     | 2           | 2               |

**Zusammenfassung nach Kategorie**
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|--------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.26 |        0.63 |            2.0 / 2 |                1.5 / 2 |
| studienprogramme     |     13 |      0.77 |     0.56 |        0.66 |              1 / 2 |                  1 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.60 |        0.63 |            1.0 / 2 |                0.5 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.62 |              2 / 2 |                  2 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                2.0 / 2 |

---

**Large Chunks (chunk_size=1024, overlap=100)**
Ingest:
    2859/2865 PDF-Chunks · 6 übersprungen
    92/92 URL-Chunks · 0 übersprungen

| ID  | Kategorie            | Antwort | Runtime | Top-Score | Ø-Score | Guardrail | Keywords | Korrektheit | Vollständigkeit |
|-----|----------------------|---------|---------|-----------|---------|-----------|----------|-------------|-----------------|
| Q01 | ki_regelungen        | nein    |    2.2s | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q02 | ki_regelungen        | nein    |    0.2s | -         | -       | falsch    | 0.00     | 1           | 1               |
| Q03 | ki_regelungen        | ja      |   11.7s | 0.66      | 0.62    | richtig   | 0.67     | 2           | 2               |
| Q04 | ki_regelungen        | ja      |    7.7s | 0.60      | 0.60    | richtig   | 0.67     | 2           | 1               |
| Q05 | ki_regelungen        | ja      |    3.7s | 0.62      | 0.62    | richtig   | 1.00     | 2           | 2               |
| Q06 | ki_regelungen        | nein    |    0.1s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q07 | ki_regelungen        | nein    |    0.1s | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q08 | ki_regelungen        | ja      |    3.2s | 0.62      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q09 | studienprogramme     | ja      |    1.4s | 0.66      | 0.62    | richtig   | 0.67     | 2           | 1               |
| Q10 | studienprogramme     | ja      |    2.4s | 0.66      | 0.63    | richtig   | 0.67     | 2           | 1               |
| Q11 | studienprogramme     | ja      |    4.3s | 0.73      | 0.69    | richtig   | 0.25     | 2           | 1               |
| Q12 | studienprogramme     | nein    |    0.2s | -         | -       | falsch    | 0.00     | 2           | 2               |
| Q13 | studienprogramme     | ja      |    4.7s | 0.64      | 0.63    | richtig   | 0.67     | 2           | 2               |
| Q14 | studienprogramme     | ja      |    1.7s | 0.71      | 0.69    | richtig   | 1.00     | 2           | 1               |
| Q15 | studienprogramme     | ja      |    1.5s | 0.63      | 0.63    | richtig   | 0.50     | 2           | 2               |
| Q16 | studienprogramme     | ja      |    4.9s | 0.62      | 0.61    | richtig   | 0.75     | 2           | 2               |
| Q17 | studienprogramme     | nein    |    0.1s | -         | -       | falsch    | 0.00     | 0           | 0               |
| Q18 | studienprogramme     | ja      |    2.9s | 0.62      | 0.61    | richtig   | 1.00     | 2           | 2               |
| Q19 | modulhandbuecher     | ja      |    3.8s | 0.68      | 0.65    | richtig   | 0.75     | 1           | 0               |
| Q20 | modulhandbuecher     | ja      |    3.6s | 0.61      | 0.61    | richtig   | 1.00     | 2           | 1               |
| Q21 | modulhandbuecher     | ja      |    2.6s | 0.67      | 0.66    | richtig   | 0.75     | 2           | 1               |
| Q22 | modulhandbuecher     | ja      |    1.7s | 0.62      | 0.62    | richtig   | 0.50     | 1           | 1               |
| Q23 | modulhandbuecher     | ja      |    4.7s | 0.65      | 0.64    | richtig   | 1.00     | 1           | 0               |
| Q24 | modulhandbuecher     | ja      |    3.0s | 0.63      | 0.61    | richtig   | 0.50     | 1           | 1               |
| Q25 | modulhandbuecher     | ja      |    3.0s | 0.64      | 0.62    | richtig   | 0.75     | 0           | 0               |
| Q26 | modulhandbuecher     | ja      |    4.7s | 0.63      | 0.62    | richtig   | 0.75     | 1           | 0               |
| Q27 | modulhandbuecher     | ja      |    3.1s | 0.60      | 0.60    | richtig   | 1.00     | 2           | 2               |
| Q28 | modulhandbuecher     | ja      |    3.0s | 0.64      | 0.61    | richtig   | 0.75     | 1           | 1               |
| Q29 | studienprogramme     | ja      |    3.7s | 0.65      | 0.65    | richtig   | 1.00     | 2           | 2               |
| Q30 | studienprogramme     | ja      |    3.4s | 0.64      | 0.62    | richtig   | 0.67     | 2           | 2               |
| Q31 | studienprogramme     | ja      |    2.7s | 0.64      | 0.64    | richtig   | 0.67     | 2           | 2               |
| Q32 | grenzfall            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q33 | grenzfall            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q34 | grenzfall            | ja      |    0.9s | 0.61      | 0.61    | falsch    | 1.00     | 2           | 2               |
| Q35 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |    0.1s | -         | -       | richtig   | 1.00     | 2           | 2               |

**Zusammenfassung nach Kategorie**
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|--------------------|------------------------|
| ki_regelungen        |      8 |      0.50 |     0.39 |        0.62 |            2.0 / 2 |                2.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.60 |        0.66 |              2 / 2 |                  2 / 2 |
| modulhandbuecher     |     10 |      1.00 |     0.78 |        0.64 |            1.0 / 2 |                1.0 / 2 |
| grenzfall            |      3 |      0.67 |     1.00 |        0.61 |              2 / 2 |                  2 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                2.0 / 2 |

---

#### top_k = 10:

**Small Chunks (chunk_size=256, overlap=30)**
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
| Q35 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |   0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |   0.2s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

**Zusammenfassung nach Kategorie**
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|-------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.26 |        0.65 |           1.5 / 2 |                1.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.60 |        0.66 |           1.0 / 2 |                1.0 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.53 |        0.63 |           0.0 / 2 |                0.0 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.64 |           2.0 / 2 |                2.0 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |           2.0 / 2 |                2.0 / 2 |

---

**Medium Chunks (chunk_size=512, overlap=50)**
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
| Q35 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

**Zusammenfassung nach Kategorie**
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|--------------------|------------------------|
| ki_regelungen        |      8 |      0.38 |     0.18 |        0.63 |            1.5 / 2 |                1.0 / 2 |
| studienprogramme     |     13 |      0.77 |     0.60 |        0.66 |            1.0 / 2 |                1.0 / 2 |
| modulhandbuecher     |     10 |      0.80 |     0.57 |        0.63 |            0.0 / 2 |                0.0 / 2 |
| grenzfall            |      3 |      0.33 |     1.00 |        0.62 |            2.0 / 2 |                2.0 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                2.0 / 2 |

---

**Large Chunks (chunk_size=1024, overlap=100)**
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
| Q35 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q36 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q37 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q38 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q39 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q40 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q41 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |
| Q42 | off_topic            | nein    |   0.1s  | -         | -       | richtig   | 1.00     | 2           | 2               |

**Zusammenfassung nach Kategorie**
| Kategorie            | Fragen | Guardrail | Keywords | Top-Score Ø | Korrektheit Median | Vollständigkeit Median |
|----------------------|--------|-----------|----------|-------------|--------------------|------------------------|
| ki_regelungen        |      8 |      0.50 |     0.34 |        0.62 |            2.0 / 2 |                2.0 / 2 |
| studienprogramme     |     13 |      0.85 |     0.62 |        0.66 |            2.0 / 2 |                1.0 / 2 |
| modulhandbuecher     |     10 |      1.00 |     0.70 |        0.64 |            1.0 / 2 |                0.5 / 2 |
| grenzfall            |      3 |      0.67 |     1.00 |        0.61 |            2.0 / 2 |                2.0 / 2 |
| off_topic            |      8 |      1.00 |     1.00 |           - |            2.0 / 2 |                2.0 / 2 |

---

### Lessons Learned

Modulbeschreibungen, Studienprogramme und KI-Regelungen sind inhaltlich dichte Texte, bei denen zusammengehörige Informationen 
oft über mehrere Sätze verteilt sind. Kleine Chunks (256 Token) zerschneiden diese Zusammenhänge - ein Chunk enthält dann 
z.B. die Lernziele eines Moduls, aber nicht die Prüfungsform. Das LLM kann die Frage nur teilweise beantworten, weil der relevante Kontext 
auf mehrere, möglicherweise nicht alle abgerufene Chunks verteilt ist.

Large Chunks (1024 Token) halten solche Passagen zusammen. Das erklärt den deutlichen Sprung bei modulhandbuecher von 0,50 auf 1,00 in der Korrektheit.

Ein weiterer Effekt: Small Chunks erzeugen fast viermal so viele Vektoren (10.930 vs. 2.865), was die Retrieval-Latenz erhöht und zu mehr Embedding-Fehlern 
führt (2 % übersprungen vs. < 1 % bei Large).

---

## Installationsanleitung

### Voraussetzungen

- Python 3.11+
- [Ollama](https://ollama.com) installiert und gestartet
- [Qdrant Cloud](https://cloud.qdrant.io) Account (oder lokale Qdrant-Instanz)

### Installation

**1. Repository klonen**
```bash
git clone <repo-url>
cd RAG_Studienberater
```

**2. Virtuelle Umgebung erstellen und aktivieren**
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/macOS:
source .venv/bin/activate
```

**3. Pakete installieren**
```bash
# Nur Laufzeit-Abhängigkeiten:
pip install -e .

# Mit Dev-Tools (pytest, ruff, mypy):
pip install -e .[dev]
```

**4. Ollama-Modelle herunterladen**
```bash
ollama pull qwen2.5:7b
ollama pull bge-m3
```

**5. Umgebungsvariablen konfigurieren**

Kopiere `.env.example` zu `.env` und trage deine Zugangsdaten ein:

```bash
cp .env.example .env
```

`.env` befüllen:
```env
QDRANT__ENDPOINT=https://deine-url.qdrant.io
QDRANT__API_KEY=dein_api_key
QDRANT__COLLECTION_NAME=studienberater
QDRANT__VECTOR_DIMENSIONS=1024

OLLAMA__BASE_URL=http://localhost:11434
OLLAMA__LANGUAGE_MODEL=qwen2.5:7b
OLLAMA__EMBEDDING_MODEL=bge-m3

CHUNKING__CHUNK_SIZE=1024
CHUNKING__CHUNK_OVERLAP=100
CHUNKING__TOP_K=10

GUARDRAIL__MIN_SCORE=0.65

LOGGING__LEVEL=INFO
```

> **Wichtig:** Die verschachtelten Einstellungen verwenden doppelte Unterstriche (`__`) als Trennzeichen.

---

### Verwendung

**Schritt 1 — Dokumente und Links vorbereiten**

PDFs in `data/raw/pdf/` ablegen (Unterordner sind erlaubt):
```
data/raw/pdf/
├── dokument1.pdf
├── dokument2.pdf
└── unterordner/
    └── dokument3.pdf
```

Webseiten-URLs in `data/raw/web/url.json` eintragen:
```json
{
  "urls": [
    "https://beispiel.de/seite1",
    "https://beispiel.de/seite2"
  ]
}
```

**Schritt 2 — App starten**
```bash
streamlit run src/rag_studienberater/presentation/app.py
```
In der Sidebar auf **Wissensbasis aufbauen** klicken, um PDFs und Webseiten einzulesen.

**Schritt 3 — Tests ausführen**
```bash
py -m pytest tests/ -v
```

**Schritt 4 — Evaluation durchführen**
```bash
# Ingest + alle 42 Testfragen auswerten:
py scripts/evaluate.py

# Dokumente bereits geladen — Ingest überspringen:
py scripts/evaluate.py --skip-ingest
```

**Schritt 5 — Parameter-Sweep**
```bash
py scripts/parameter_sweep.py
```

Ergebnisse werden in `data/evaluation/top_k_5/` und `data/evaluation/top_k_10/` gespeichert.