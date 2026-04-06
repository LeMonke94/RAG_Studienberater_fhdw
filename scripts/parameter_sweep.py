"""
Parameter-Sweep

Testet alle Kombinationen aus Chunk-Konfiguration und Top-K.
Pro Chunk-Konfiguration wird nur einmal ingested — Top-K-Varianten
nutzen denselben Vector Store.

Ablauf pro Chunk-Config:
    Qdrant leeren → Ingest → Evaluate(top_k=5) → Evaluate(top_k=10)

Ergebnisse:
    data/evaluation/top_k_5/sweep_<chunk>.json
    data/evaluation/top_k_10/sweep_<chunk>.json

HINWEIS: Ein Durchlauf dauert ~10-20 Minuten (Ingest + 2 × 42 Fragen).
         Bei 3 Chunk-Configs = ~30-60 Minuten Gesamtlaufzeit.

Verwendung:
    py scripts/parameter_sweep.py
    py scripts/parameter_sweep.py --testset data/evaluation/testset.json
"""

# Imports
import json
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

# Reuse evaluation logic from evaluate.py
sys.path.insert(0, str(Path(__file__).parent))
from evaluate import (
    EvaluationReport,
    QuestionResult,
    calculate_report_metrics,
    print_summary,
    load_testset,
    score_result,
    get_symbol,
)


# Chunk configurations — top_k is varied separately
@dataclass
class ChunkConfig:
    name: str
    chunk_size: int
    chunk_overlap: int


@dataclass
class SweepResult:
    chunk_config: ChunkConfig
    top_k: int
    report_path: str
    report: EvaluationReport


CHUNK_CONFIGS = [
    ChunkConfig(name='small',  chunk_size=256,  chunk_overlap=30),
    ChunkConfig(name='medium', chunk_size=512,  chunk_overlap=50),
    ChunkConfig(name='large',  chunk_size=1024, chunk_overlap=100),
]

TOP_K_VALUES = [5, 10]


# Sweep logic
def run_sweep(testset_path: str, pdf_folder: str, url_json: str, output_base_dir: str) -> None:
    total_runs = len(CHUNK_CONFIGS) * len(TOP_K_VALUES)
    print(f"\n{'═' * 80}")
    print('  PARAMETER-SWEEP — RAG-STUDIENBERATER')
    print(f"{'═' * 80}")
    print(f'  {len(CHUNK_CONFIGS)} Chunk-Configs × {len(TOP_K_VALUES)} Top-K-Werte = {total_runs} Evaluationen')
    print(f'  Ingest: {len(CHUNK_CONFIGS)}× (Top-K-Varianten teilen denselben Vector Store)')
    print(f'  Geschätzte Laufzeit: {len(CHUNK_CONFIGS) * 15}–{len(CHUNK_CONFIGS) * 20} Minuten\n')

    all_results: list[SweepResult] = []

    for i, chunk_config in enumerate(CHUNK_CONFIGS, start=1):
        print(f"\n{'─' * 80}")
        print(f'  [{i}/{len(CHUNK_CONFIGS)}] Chunk-Config: {chunk_config.name}  '
              f'(size={chunk_config.chunk_size}, overlap={chunk_config.chunk_overlap})')
        print(f"{'─' * 80}\n")

        ingest_start = time.perf_counter()

        # Initialise container for ingest (top_k irrelevant here)
        try:
            container = _create_container(chunk_config, top_k=TOP_K_VALUES[0])
        except Exception as e:
            print(f'  FEHLER beim Initialisieren: {e}')
            print('  Stelle sicher, dass Ollama und Qdrant laufen.\n')
            sys.exit(1)

        # Clear vector store
        print('  Leere Vector Store...')
        try:
            container.retrieval_use_case.retrieval_service.vector_store.clear()
            print('  Vector Store geleert.')
        except Exception as e:
            print(f'  WARNUNG: Leeren fehlgeschlagen: {e}')

        # Ingest once for this chunk config
        print(f"\n  Ingest PDFs aus '{pdf_folder}'...")
        try:
            container.ingest_use_case.execute_folder(pdf_folder)
        except Exception as e:
            print(f'  WARNUNG: PDF-Ingest fehlgeschlagen: {e}')

        print(f"  Ingest URLs aus '{url_json}'...")
        try:
            container.ingest_use_case.execute_urls_from_file(url_json)
        except Exception as e:
            print(f'  WARNUNG: URL-Ingest fehlgeschlagen: {e}')

        ingest_duration = time.perf_counter() - ingest_start
        print(f'  Ingest abgeschlossen in {ingest_duration/60:.1f} Minuten.\n')

        # Evaluate for each top_k — no re-ingest needed
        for top_k in TOP_K_VALUES:
            print(f"  {'─' * 40}")
            print(f'  Evaluation mit top_k={top_k}...')
            print(f"  {'─' * 40}\n")

            eval_container = _create_container(chunk_config, top_k=top_k)
            output_dir = str(Path(output_base_dir) / f'top_k_{top_k}')

            path, report = _run_evaluation(
                container=eval_container,
                testset_path=testset_path,
                output_dir=output_dir,
                config_name=chunk_config.name,
            )
            all_results.append(SweepResult(chunk_config, top_k, path, report))
            print(f'  Ergebnis gespeichert: {path}\n')

    _print_comparison(all_results)


def _create_container(chunk_config: ChunkConfig, top_k: int):
    """Creates a container with the given chunk config and top_k."""
    import os
    os.environ['CHUNKING__CHUNK_SIZE']    = str(chunk_config.chunk_size)
    os.environ['CHUNKING__CHUNK_OVERLAP'] = str(chunk_config.chunk_overlap)
    os.environ['CHUNKING__TOP_K']         = str(top_k)

    from rag_studienberater.config.settings import get_settings
    get_settings.cache_clear()

    from rag_studienberater.bootstrap.container import create_container
    return create_container()


def _run_evaluation(
    container, testset_path: str, output_dir: str, config_name: str
) -> tuple[str, EvaluationReport]:
    """Runs evaluation for one container configuration and returns (file_path, report)."""
    questions = load_testset(testset_path)
    report = EvaluationReport(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        testset_path=testset_path,
    )

    for i, question_data in enumerate(questions, start=1):
        question_text = question_data['frage']
        result = QuestionResult(
            id=question_data.get('id', f'Q{i:02d}'),
            category=question_data.get('kategorie', 'unbekannt'),
            question=question_text,
            expected_answer=question_data.get('erwartet_antwort', True),
        )

        print(f'  [{i:02d}/{len(questions)}] {question_text[:70]}', end='', flush=True)

        try:
            t0 = time.perf_counter()
            answer = container.answer_use_case.execute(question_text)
            result.runtime_sec = time.perf_counter() - t0
            result.has_answer   = answer.has_evidence
            result.answer_text  = answer.text
            result.sources      = list({
                f'{chunk.source} S.{chunk.page}' if chunk.page else chunk.source
                for chunk in answer.sources
            })
        except Exception as exc:
            result.answer_text = f'[FEHLER: {exc}]'

        score_result(result, question_data)
        print(f'  {get_symbol(result.guardrail_correct)}  ({result.runtime_sec:.1f}s)')
        report.results.append(result)

    calculate_report_metrics(report)
    print_summary(report)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = str(Path(output_dir) / f'sweep_{config_name}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(asdict(report), f, ensure_ascii=False, indent=2)

    return path, report


def _print_comparison(results: list[SweepResult]) -> None:
    """Prints a grouped comparison table: chunk configs as rows, top_k as column groups."""
    print(f"\n\n{'═' * 80}")
    print('  VERGLEICH ALLER KONFIGURATIONEN')
    print(f"{'═' * 80}\n")

    # Header
    col = 10
    tk_w = 50  # width per top_k group
    print(f"  {'':>{col}}  ", end='')
    for top_k in TOP_K_VALUES:
        label = f'top_k={top_k}'
        print(f"  {label:^{tk_w}}", end='')
    print()

    print(f"  {'Chunk':<{col}}  ", end='')
    for _ in TOP_K_VALUES:
        print(f"  {'Guardrail':>9} {'Quellen':>7} {'Keywords':>8} {'TopScore':>9} {'ØScore':>7} {'Ø Zeit':>6}  ", end='')
    print()

    print(f"  {'─'*col}  ", end='')
    for _ in TOP_K_VALUES:
        print(f"  {'─'*9} {'─'*7} {'─'*8} {'─'*9} {'─'*7} {'─'*6}  ", end='')
    print()

    # Rows grouped by chunk config
    for chunk_config in CHUNK_CONFIGS:
        print(f"  {chunk_config.name:<{col}}  ", end='')
        for top_k in TOP_K_VALUES:
            match = next((r for r in results if r.chunk_config.name == chunk_config.name and r.top_k == top_k), None)
            if match:
                r = match.report
                print(
                    f"  {r.guardrail_accuracy:>8.0%} "
                    f"{r.source_citation_rate:>7.0%} "
                    f"{r.average_keyword_recall:>8.0%} "
                    f"{r.average_top_score:>9.3f} "
                    f"{r.average_avg_score:>7.3f} "
                    f"{r.average_runtime_sec:>5.1f}s  ",
                    end=''
                )
            else:
                print(f"  {'–':>8} {'–':>7} {'–':>8} {'–':>9} {'–':>7} {'–':>6}  ", end='')
        print()

    # File list
    print(f'\n  Ergebnisdateien:')
    for res in results:
        print(f'    top_k={res.top_k}  {res.chunk_config.name:<8}  {res.report_path}')
    print(f"\n{'═' * 80}\n")


# Entry point
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parameter-Sweep für den RAG-Studienberater')
    parser.add_argument('--testset',    default='data/evaluation/testset.json')
    parser.add_argument('--pdf-folder', default='data/raw/pdf')
    parser.add_argument('--url-json',   default='data/raw/web/url.json')
    parser.add_argument('--output',     default='data/evaluation')
    args = parser.parse_args()

    run_sweep(
        testset_path=args.testset,
        pdf_folder=args.pdf_folder,
        url_json=args.url_json,
        output_base_dir=args.output,
    )
