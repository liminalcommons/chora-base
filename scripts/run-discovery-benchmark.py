#!/usr/bin/env python3
"""
run-discovery-benchmark.py - Execute discovery benchmark on test queries

Runs all queries from fixtures/feat-002-validation/queries.csv through
unified-discovery.py and records routing decisions, token estimates, and timing.

Usage:
    python scripts/run-discovery-benchmark.py

Outputs:
    scripts/fixtures/feat-002-validation/benchmark-results.csv
"""

import csv
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any
import sys

# Windows UTF-8 console support (chora-base cross-platform requirement)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Constants
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "feat-002-validation"
QUERIES_FILE = FIXTURES_DIR / "queries.csv"
RESULTS_FILE = FIXTURES_DIR / "benchmark-results.csv"
DISCOVERY_SCRIPT = Path(__file__).parent / "unified-discovery.py"


def load_queries() -> List[Dict[str, str]]:
    """Load test queries from CSV file."""
    queries = []
    with open(QUERIES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            queries.append(row)
    return queries


def run_discovery(query_text: str) -> Dict[str, Any]:
    """
    Run unified-discovery.py with given query and parse result.

    Returns:
        dict: {
            'routing': str (e.g., 'CODE_FEATURE'),
            'method': str (e.g., 'feature_manifest'),
            'token_estimate': int,
            'time_seconds': float,
            'suggestions': list,
            'error': str or None
        }
    """
    start_time = time.time()

    try:
        # Run discovery with JSON output
        result = subprocess.run(
            ['python', str(DISCOVERY_SCRIPT), query_text, '--format', 'json'],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=DISCOVERY_SCRIPT.parent.parent  # Run from repo root
        )

        elapsed = time.time() - start_time

        if result.returncode != 0:
            return {
                'routing': 'ERROR',
                'method': 'none',
                'token_estimate': 0,
                'time_seconds': elapsed,
                'suggestions': [],
                'error': result.stderr or result.stdout
            }

        # Parse JSON output
        output_json = json.loads(result.stdout)

        # Map query_type to uppercase routing format
        query_type = output_json.get('query_type', 'unknown')
        routing = query_type.upper() if query_type != 'unknown' else 'UNKNOWN'

        return {
            'routing': routing,
            'method': output_json.get('method_used', 'unknown'),
            'token_estimate': output_json.get('token_estimate', 0),
            'time_seconds': elapsed,
            'suggestions': output_json.get('results', []),
            'error': None
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        return {
            'routing': 'TIMEOUT',
            'method': 'none',
            'token_estimate': 0,
            'time_seconds': elapsed,
            'suggestions': [],
            'error': 'Query timed out after 30 seconds'
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'routing': 'ERROR',
            'method': 'none',
            'token_estimate': 0,
            'time_seconds': elapsed,
            'suggestions': [],
            'error': str(e)
        }


def run_benchmark() -> List[Dict[str, Any]]:
    """Run benchmark on all test queries."""
    queries = load_queries()
    results = []

    print(f"Running benchmark on {len(queries)} queries...")
    print(f"Discovery script: {DISCOVERY_SCRIPT}")
    print(f"Results will be saved to: {RESULTS_FILE}")
    print()

    for i, query in enumerate(queries, 1):
        query_id = query['query_id']
        query_text = query['query_text']
        expected_type = query['expected_type']

        print(f"[{i}/{len(queries)}] {query_id}: {query_text[:50]}...")

        # Run discovery
        discovery_result = run_discovery(query_text)

        # Check if routing matches expected
        actual_routing = discovery_result['routing']
        match = actual_routing == expected_type

        # Record result
        result = {
            'query_id': query_id,
            'query_text': query_text,
            'expected_type': expected_type,
            'actual_routing': actual_routing,
            'match': 'yes' if match else 'no',
            'discovery_method': discovery_result['method'],
            'token_estimate': discovery_result['token_estimate'],
            'time_seconds': round(discovery_result['time_seconds'], 3),
            'suggestions_count': len(discovery_result['suggestions']),
            'error': discovery_result['error'] or ''
        }
        results.append(result)

        # Print status
        status = "✓" if match else "✗"
        print(f"  {status} Expected: {expected_type}, Got: {actual_routing} ({result['time_seconds']}s)")

        if discovery_result['error']:
            print(f"  ERROR: {discovery_result['error']}")

        print()

    return results


def save_results(results: List[Dict[str, Any]]):
    """Save benchmark results to CSV file."""
    if not results:
        print("No results to save.")
        return

    # Write results
    with open(RESULTS_FILE, 'w', encoding='utf-8', newline='') as f:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to: {RESULTS_FILE}")


def print_summary(results: List[Dict[str, Any]]):
    """Print summary statistics."""
    if not results:
        print("No results to summarize.")
        return

    total = len(results)
    matches = sum(1 for r in results if r['match'] == 'yes')
    errors = sum(1 for r in results if r['actual_routing'] in ['ERROR', 'TIMEOUT'])

    accuracy = (matches / total) * 100 if total > 0 else 0

    avg_time = sum(r['time_seconds'] for r in results) / total if total > 0 else 0
    avg_tokens = sum(r['token_estimate'] for r in results if r['token_estimate'] > 0)
    avg_tokens = avg_tokens / (total - errors) if (total - errors) > 0 else 0

    print()
    print("=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"Total queries: {total}")
    print(f"Matched routing: {matches} ({accuracy:.1f}%)")
    print(f"Mismatched routing: {total - matches - errors}")
    print(f"Errors/Timeouts: {errors}")
    print()
    print(f"Average time: {avg_time:.3f} seconds")
    print(f"Average token estimate: {int(avg_tokens)} tokens")
    print()

    # Breakdown by expected type
    type_breakdown = {}
    for result in results:
        expected = result['expected_type']
        if expected not in type_breakdown:
            type_breakdown[expected] = {'total': 0, 'matches': 0}
        type_breakdown[expected]['total'] += 1
        if result['match'] == 'yes':
            type_breakdown[expected]['matches'] += 1

    print("Accuracy by Query Type:")
    for query_type, stats in sorted(type_breakdown.items()):
        type_accuracy = (stats['matches'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"  {query_type}: {stats['matches']}/{stats['total']} ({type_accuracy:.1f}%)")

    print("=" * 60)


def main():
    """Main execution."""
    print("FEAT-002 Discovery Benchmark")
    print("=" * 60)
    print()

    # Ensure fixtures directory exists
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

    # Check if queries file exists
    if not QUERIES_FILE.exists():
        print(f"ERROR: Queries file not found: {QUERIES_FILE}")
        return 1

    # Check if discovery script exists
    if not DISCOVERY_SCRIPT.exists():
        print(f"ERROR: Discovery script not found: {DISCOVERY_SCRIPT}")
        return 1

    # Run benchmark
    results = run_benchmark()

    # Save results
    save_results(results)

    # Print summary
    print_summary(results)

    return 0


if __name__ == '__main__':
    exit(main())
