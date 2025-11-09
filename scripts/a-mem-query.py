#!/usr/bin/env python3
"""
A-MEM Knowledge Query Tracker

Logs knowledge queries to track SAP-010 ROI metric: "Knowledge queries per session ≥3"

Usage:
    python scripts/a-mem-query.py "how to fix jinja2 undefined variables"
    python scripts/a-mem-query.py "SAP-010 adoption patterns" --session-id abc123
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional



# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def get_session_id() -> str:
    """Generate or retrieve current session ID"""
    # Simple: use current date + hour
    return datetime.utcnow().strftime("%Y-%m-%d-%H")


def search_knowledge_notes(query: str, knowledge_dir: Path) -> List[str]:
    """
    Search knowledge notes for query string.

    Returns list of matching note filenames.
    """
    if not knowledge_dir.exists():
        return []

    matches = []
    for note in knowledge_dir.glob("*.md"):
        content = note.read_text().lower()
        if query.lower() in content:
            matches.append(note.name)

    return matches


def log_query_event(
    query: str,
    results: List[str],
    session_id: str,
    events_dir: Path
) -> None:
    """Log knowledge query to events/knowledge-queries.jsonl"""
    events_dir.mkdir(parents=True, exist_ok=True)

    event = {
        "event_type": "knowledge_query",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query,
        "results_count": len(results),
        "results": results,
        "session_id": session_id,
        "tags": ["sap-010", "a-mem", "query", "roi-tracking"]
    }

    queries_log = events_dir / "knowledge-queries.jsonl"
    with open(queries_log, "a", encoding='utf-8') as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_session_metrics(session_id: str, events_dir: Path) -> dict:
    """Calculate queries per session metric"""
    queries_log = events_dir / "knowledge-queries.jsonl"

    if not queries_log.exists():
        return {"session_id": session_id, "queries": 0, "target": 3}

    session_queries = 0
    with open(queries_log, "r", encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("session_id") == session_id:
                session_queries += 1

    return {
        "session_id": session_id,
        "queries": session_queries,
        "target": 3,
        "meets_target": session_queries >= 3
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM knowledge query tracker for ROI validation"
    )
    parser.add_argument("query", help="Search query for knowledge notes")
    parser.add_argument(
        "--session-id",
        help="Session ID (default: auto-generated from timestamp)"
    )
    parser.add_argument(
        "--memory-dir",
        default=".chora/memory",
        help="A-MEM directory (default: .chora/memory)"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show session metrics after query"
    )

    args = parser.parse_args()

    # Resolve paths
    memory_dir = Path(args.memory_dir)
    knowledge_dir = memory_dir / "knowledge"
    events_dir = memory_dir / "events"

    # Get session ID
    session_id = args.session_id or get_session_id()

    # Search knowledge notes
    results = search_knowledge_notes(args.query, knowledge_dir)

    # Log query event
    event = log_query_event(args.query, results, session_id, events_dir)

    # Display results
    print(f"🔍 Query: {args.query}")
    print(f"📁 Session: {session_id}")
    print(f"✅ Results: {len(results)} notes found")

    if results:
        print("\nMatching notes:")
        for note in results:
            print(f"  - {note}")
    else:
        print("\n⚠️  No matching notes found")

    # Show metrics if requested
    if args.metrics:
        metrics = calculate_session_metrics(session_id, events_dir)
        print(f"\n📊 Session Metrics:")
        print(f"  Queries this session: {metrics['queries']}")
        print(f"  Target: ≥{metrics['target']} queries/session")

        if metrics['meets_target']:
            print(f"  ✅ Target met!")
        else:
            print(f"  ⏳ Need {metrics['target'] - metrics['queries']} more queries")

    return 0


if __name__ == "__main__":
    sys.exit(main())
