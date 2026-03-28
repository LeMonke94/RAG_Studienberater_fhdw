# Architektur Konzepte

domain/
├── models/    → Definition der Datenstrukturen
│               werden überall durchgereicht
├── ports/     → Interfaces für externe Tools
│               werden in infrastructure implementiert
└── services/  → Fachlogik in reinem Python
                werden in application aufgerufen

infrastructure/
└── implementiert die Ports mit echten Tools
    VectorStorePort → QdrantStore (Qdrant)
    LLMPort         → OllamaClient (Ollama)

application/
└── koordiniert services + infrastructure
    "hole Chunks (infrastructure) dann prüfe Guardrail (service)"

ui/
└── zeigt Ergebnis an, ruft application auf

| Technologie       | Paket                  | Zweck                                         |
|-------------------|------------------------|-----------------------------------------------|
| Laufzeitumgebung  | Python 3.11+           | Basis des Gesammtprojekts                     |
| LLM  (lokal)      | qwen2.5:7b             | Generiert die Antworten                       |
| LLM Framework     | langchain-ollama       | Verbindet LangChain mit Ollama                |
| Text Embedding    | bge-m3                 | Wandelt Text in Vektoren um                   |
| RAG Framework     | LangChain              | Fertige Bausteine für Pipeline                |
| Vektordatenbank   | Qdrant                 | Speichert Chunks + Vektoren                   |
| PDF-Extraktion    | pypdf + pdfplumber     | Extrahiert Text aus PDFs                      |
| Web-Scraping      | BeautifulSoup4         | Extrahiert Text aus FHDW-Webseiten            |
| User Interface    | Streamlit              | Chat-Interface ohne Frontend-Kenntnisse       |
| Konfiguration     | pydantic-settings      | Typsichere Verwaltung von Einstellungen       |
| Konfiguration     | python-dotenv          | Lädt .env-Datei in Umgebungsvariablen         |
| Testing           | pytest + pytest-mock   | Automatisierte Tests                          |
| Code-Qualität     | ruff                   | Linting und automatische Formatierung         |
| Typ-Prüfung       | mypy                   | Statische Typprüfung vor der Ausführung       |
| Versionskontrolle | Git                    | Code-Versionierung und Zusammenarbeit         |
| Projektdefinition | pyproject.toml         | Metadaten, Abhängigkeiten, Tool-Konfiguration |


app/                                # Enthält den gesamten Python-Code
    shared/                         # Alles was alle drei Pipelines (Ingestion, Retrieval, Generation) gemeinsam nutzen
        domain/                         # Abstrakte Interfaces (Ports) und Datenmodelle die in allen Pipelines verwendet werden
            models/                         # Datenstrukturen
            ports/                          # Abstrakte Interfaces
        infrastructure/                 # Gemeinsame Adapter
            vectorstores/
            llm/
            embeddings/

    pipelines/                      # Die drei Verarbeitungsstränge
        ingestion/                      # Dokumente einlesen
            domain/                         #  Ingestion-Logik
                services/
            infrastructure/                 # Ingestion-Adapter
            application/