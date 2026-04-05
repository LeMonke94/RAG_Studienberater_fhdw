"""
Evaluations-Skript
    Lädt das Testset + schickt jede Frage durch die vollständige Pipeline + bewertet die Antwortqualität anhand messbarer Kriterien.

Verwendung:
    py scripts/evaluate.py
    py scripts/evaluate.py --testset data/evaluation/testset.json
    py scripts/evaluate.py --skip-ingest   # wenn Dokumente bereits geladen sind
"""

# Imports
import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


# Data Models for Results
@dataclass
class QuestionResult:
    id: str
    category: str
    question: str
    expected_answer: bool

    # System-Output
    has_answer: bool = False
    answer_text: str = ""
    sources: list[str] = field(default_factory=list)
    runtime_sec: float = 0.0

    # Automated Metrics
    guardrail_correct: bool = False      # System behaves as expected (Answer / No Answer)
    has_sources: bool = False            # Answer contains source citations
    keyword_recall: float = 0.0          # Ratio of found keywords (0.0-1.0)

    # Manually evaluable (to be filled out after the run)
    correctness: int = -1                # 0=false, 1=partial, 2=correct (-1 = not evaluated)
    completeness: int = -1               # 0=incomplete, 1=partial, 2=complete
    notes: str = ""

@dataclass
class EvaluationReport:
    timestamp: str
    testset_path: str
    total_questions: int = 0
    guardrail_accuracy: float = 0.0
    source_citation_rate: float = 0.0
    average_keyword_recall: float = 0.0
    average_runtime_sec: float = 0.0
    results: list[QuestionResult] = field(default_factory=list)


# Scoring
def calculate_keyword_recall(answer_text: str, keywords: list[str]) -> float:
    """Anteil der Schlüsselwörter, die in der Antwort vorkommen (case-insensitive)."""
    if not keywords:
        return 1.0  # No expectations = full score

    answer_lower = answer_text.lower()
    matches = sum(1 for kw in keywords if kw.lower() in answer_lower)
    return matches / len(keywords)

def score_result(result: QuestionResult, question_data: dict) -> None:
    """Berechnet alle automatischen Metriken und schreibt sie ins Ergebnis."""
    # Guardrail is correct if the system's decision to answer matches our expectation
    result.guardrail_correct = result.has_answer == result.expected_answer
    
    # Check if we got an answer and if it includes at least one source
    result.has_sources = result.has_answer and len(result.sources) > 0
    
    # Calculate how many of the expected keywords were mentioned
    result.keyword_recall = calculate_keyword_recall(
        result.answer_text,
        question_data.get("keywords", [])
    )


# Report-Output
SEPARATOR = '-' * 80

def get_symbol(value: bool) -> str:
    return '✓' if value else '✗'

def render_recall_bar(recall: float, width: int = 10) -> str:
    """Lädt eine Progress-Bar für den Keyword recall"""
    filled = round(recall * width)
    return f"[{'█' * filled}{'░' * (width - filled)}] {recall:.0%}"

def print_results(results: list[QuestionResult]) -> None:
    """Druckt eine Detailierte Ausgabe für jede Antwort auf eine Frage in der Konsole."""
    print(f'\n{SEPARATOR}')
    print('  EINZELERGEBNISSE')
    print(SEPARATOR)

    for r in results:
        guardrail_sym = get_symbol(r.guardrail_correct)
        source_sym    = get_symbol(r.has_sources) if r.has_answer else ' -'
        recall_str    = render_recall_bar(r.keyword_recall) if r.expected_answer else '   (off-topic)'

        print(f'\n  [{r.id}] {r.question[:65]}')
        print(f'       Kategorie  : {r.category}')
        print(f"       Guardrail : {guardrail_sym}  (erwartet={'Antwort' if r.expected_answer else 'Keine Antwort'}, "
              f"erhalten={'Antwort' if r.has_answer else 'Keine Antwort'})")

        if r.has_answer:
            print(f"       Quellen   : {source_sym}  ({len(r.sources)} Quelle(s): {', '.join(r.sources[:2])}{'...' if len(r.sources) > 2 else ''})")
            print(f'       Keywords  : {recall_str}')
            print(f"       Antwort    : {r.answer_text[:120]}{'...' if len(r.answer_text) > 120 else ''}")
        else:
            print(f'       Antwort    : [Guardrail ausgelöst]')

        print(f'       Zeit      : {r.runtime_sec:.2f}s')

def print_summary(report: EvaluationReport) -> None:
    """Zeigt eine aggregierte Zusammenfassung aller Metriken."""
    print(f'\n{SEPARATOR}')
    print('  ZUSAMMENFASSUNG')
    print(SEPARATOR)

    print(f'\n  Gesamt-Fragen         : {report.total_questions}')
    print(f'  Guardrail-Korrektheit : {report.guardrail_accuracy:.0%}  '
          f'({round(report.guardrail_accuracy * report.total_questions)}/{report.total_questions} korrekt)')
    print(f'  Quellenangabe-Quote   : {report.source_citation_rate:.0%}  '
          f'(bei beantworteten Fragen)')
    print(f'  Ø Keyword-Recall      : {report.average_keyword_recall:.0%}')
    print(f'  Ø Laufzeit            : {report.average_runtime_sec:.2f}s pro Frage')

    # Breakdown by category
    categories: dict[str, list[QuestionResult]] = {}
    for r in report.results:
        categories.setdefault(r.category, []).append(r)

    print(f"\n  {'Kategorie':<22} {'Fragen':>6}  {'Guardrail':>10}  {'Quellen':>8}  {'Keywords':>10}")
    print(f"  {'─'*22} {'─'*6}  {'─'*10}  {'─'*8}  {'─'*10}")

    for cat, entries in sorted(categories.items()):
        n = len(entries)
        gc = sum(1 for e in entries if e.guardrail_correct) / n
        qc = sum(1 for e in entries if e.has_sources) / max(1, sum(1 for e in entries if e.has_answer))
        kr = sum(e.keyword_recall for e in entries) / n
        print(f"  {cat:<22} {n:>6}  {gc:>9.0%}  {qc:>7.0%}  {kr:>9.0%}")

    print()

    # Note for manual evaluation
    print("  HINWEIS: Korrektheit und Vollständigkeit müssen manuell bewertet werden.")
    print("  Fülle die Felder 'korrektheit' und 'vollständigkeit' in der Ergebnisdatei aus:")
    print("    0 = falsch/unvollständig  |  1 = teilweise  |  2 = korrekt/vollständig")
    print()


# Main Logic
def load_testset(path: str) -> list[dict]:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    questions = data.get('fragen', data) if isinstance(data, dict) else data
    print(f'  Testset geladen: {len(questions)} Fragen aus \'{path}\'')
    return questions

def save_report(report: EvaluationReport, output_dir: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = report.timestamp.replace(':', '-').replace(' ', '_')
    filename = f'results_{timestamp}.json'
    path = str(Path(output_dir) / filename)

    # dataclass → dict (rekursiv)
    def to_dict(obj):
        if isinstance(obj, list):
            return [to_dict(i) for i in obj]
        if hasattr(obj, '__dataclass_fields__'):
            return {k: to_dict(v) for k, v in asdict(obj).items()}
        return obj
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(to_dict(report), f, ensure_ascii=False, indent=2)

    return path

def calculate_report_metrics(report: EvaluationReport) -> None:
    """Aggregierte Metriken in den Bericht schreiben."""
    n = len(report.results)
    if n == 0:
        return
    
    report.total_questions = n
    report.guardrail_accuracy = sum(
        1 for e in report.results if e.guardrail_correct
    ) / n

    answered = [e for e in report.results if e.has_answer]
    report.source_citation_rate = (
        sum(1 for e in answered if e.has_sources) / len(answered)
        if answered else 0.0
    )

    report.average_keyword_recall = (
        sum(e.keyword_recall for e in report.results) / n
    )
    report.average_runtime_sec = (
        sum(e.runtime_sec for e in report.results) / n
    )

def main() -> None:
    parser = argparse.ArgumentParser(description='RAG-Studienberater Evaluation')
    parser.add_argument(
        '--testset',
        default='data/evaluation/testset.json',
        help='Pfad zur Testset-JSON-Datei',
    )
    parser.add_argument(
        '--output',
        default='data/evaluation',
        help='Ausgabeverzeichnis für den Ergebnisbericht',
    )
    parser.add_argument(
        '--skip-ingest',
        action='store_true',
        help='Dokumente nicht erneut einlesen (Vector Store bereits befüllt)',
    )
    parser.add_argument(
        '--ingest-folder',
        default='data/raw/pdf',
        help='Ordner mit PDFs für den Ingest (Standard: data/raw/pdf)',
    )
    args = parser.parse_args()

    print(f"\n{'═' * 80}")
    print('  RAG-STUDIENBERATER — EVALUATION')
    print(f"{'═' * 80}")

    # Initialize Container
    print('\n  Initialisiere Pipeline...')
    try:
        from rag_studienberater.bootstrap.container import create_container
        container = create_container()
    except Exception as exc:
        print(f'\n  FEHLER beim Initialisieren: {exc}')
        print('  Stelle sicher, dass Ollama läuft und .env korrekt konfiguriert ist.')
        sys.exit(1)

    # Ingest
    if not args.skip_ingest:
        print(f"  Lese Dokumente aus '{args.ingest_folder}' ein...")
        try:
            container.ingest_use_case.execute_folder(args.ingest_folder)
            print('  Ingest abgeschlossen.')
        except Exception as exc:
            print(f'\n  WARNUNG: Ingest fehlgeschlagen: {exc}')
            print('  Fahre fort mit bestehendem Vector-Store-Inhalt.')
    else:
        print('  Ingest übersprungen (--skip-ingest).')

    # Load Testset
    print()
    questions = load_testset(args.testset)

    # Run Evaluation
    report = EvaluationReport(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        testset_path=args.testset,
    )

    print(f'\n  Starte Evaluation ({len(questions)} Fragen)...\n')

    for i, question_data in enumerate(questions, start=1):
        q_id = question_data.get('id', f'Q{i:02d}')

        q_text = question_data['frage']
        category = question_data.get('kategorie', 'unbekannt')
        expected_answer = question_data.get('erwartet_antwort', True)

        print(f'  [{i:02d}/{len(questions)}] {q_text[:70]}', end='', flush=True)

        result = QuestionResult(
            id=q_id,
            category=category,
            question=q_text,
            expected_answer=expected_answer,
        )

        try:
            start = time.perf_counter()
            answer = container.answer_use_case.execute(q_text)
            result.runtime_sec = time.perf_counter() - start

            result.has_answer = answer.has_evidence
            result.answer_text = answer.text
            
            # Using 'p.' instead of 'S.' for pages
            result.sources = list({
                f'{chunk.source} S.{chunk.page}' if chunk.page else chunk.source
                for chunk in answer.sources
            })

        except Exception as exc:
            result.runtime_sec = 0.0
            result.answer_text = f'[FEHLER: {exc}]'

        score_result(result, question_data)

        status = get_symbol(result.guardrail_correct)
        print(f'  {status}  ({result.runtime_sec:.1f}s)')

        report.results.append(result)

    # Calculate metrics and print
    calculate_report_metrics(report)
    print_results(report.results)
    print_summary(report)

    # Save report
    report_path = save_report(report, args.output)
    print(f'  Ergebnisse gespeichert: {report_path}')
    print(f"{'═' * 80}\n")

if __name__ == '__main__':
    main()