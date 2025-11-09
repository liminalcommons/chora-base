#!/usr/bin/env python3
"""
A-MEM + Beads Correlation Script

Demonstrates bidirectional traceability between A-MEM events and beads tasks.

Usage:
    # Find A-MEM events for a beads task
    python scripts/a-mem-beads-correlation.py events-for-task --task-id chora-base-o4b

    # Find beads tasks for a trace ID
    python scripts/a-mem-beads-correlation.py tasks-for-trace --trace-id sap-015-phase1-multi-adopter

    # Show correlation summary
    python scripts/a-mem-beads-correlation.py --summary
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict



# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def load_events(events_dir: Path) -> List[dict]:
    """Load all A-MEM events from development.jsonl"""
    events_path = events_dir / "development.jsonl"

    if not events_path.exists():
        return []

    events = []
    with open(events_path, "r", encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return events


def find_events_for_task(events: List[dict], task_id: str) -> List[dict]:
    """Find all A-MEM events referencing a beads task ID"""
    return [e for e in events if e.get("beads_task_id") == task_id]


def find_events_for_trace(events: List[dict], trace_id: str) -> List[dict]:
    """Find all A-MEM events for a trace ID"""
    return [e for e in events if e.get("trace_id") == trace_id]


def get_beads_task(task_id: str) -> Dict:
    """Get beads task details via bd CLI"""
    try:
        result = subprocess.run(
            ["bd", "show", task_id, "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        return None


def extract_trace_id(task_description: str) -> str:
    """Extract trace ID from beads task description"""
    for line in task_description.split("\n"):
        if line.strip().startswith("Trace:"):
            return line.strip().replace("Trace:", "").strip()
    return None


def find_tasks_for_trace(trace_id: str) -> List[Dict]:
    """Find all beads tasks with a given trace ID"""
    try:
        result = subprocess.run(
            ["bd", "list", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        tasks = json.loads(result.stdout)

        matching_tasks = []
        for task in tasks:
            task_trace = extract_trace_id(task.get("description", ""))
            if task_trace == trace_id:
                matching_tasks.append(task)

        return matching_tasks
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        return []


def calculate_correlation_stats(events: List[dict]) -> Dict:
    """Calculate correlation statistics"""
    total_events = len(events)
    events_with_task_id = sum(1 for e in events if e.get("beads_task_id"))
    events_with_trace_id = sum(1 for e in events if e.get("trace_id"))
    events_with_both = sum(1 for e in events if e.get("beads_task_id") and e.get("trace_id"))

    unique_task_ids = set(e.get("beads_task_id") for e in events if e.get("beads_task_id"))
    unique_trace_ids = set(e.get("trace_id") for e in events if e.get("trace_id"))

    return {
        "total_events": total_events,
        "events_with_task_id": events_with_task_id,
        "events_with_trace_id": events_with_trace_id,
        "events_with_both": events_with_both,
        "unique_task_ids": len(unique_task_ids),
        "unique_trace_ids": len(unique_trace_ids),
        "correlation_rate": (events_with_task_id / total_events * 100) if total_events > 0 else 0.0
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM + Beads correlation and traceability"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["events-for-task", "tasks-for-trace"],
        help="Query action"
    )
    parser.add_argument(
        "--task-id",
        help="Beads task ID"
    )
    parser.add_argument(
        "--trace-id",
        help="A-MEM trace ID"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show correlation summary statistics"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    events_dir = Path(args.events_dir)
    events = load_events(events_dir)

    if args.summary:
        stats = calculate_correlation_stats(events)

        if args.json:
            print(json.dumps(stats, indent=2))
            return 0

        print("A-MEM + Beads Correlation Summary")
        print("==================================")
        print(f"Total A-MEM events: {stats['total_events']}")
        print(f"Events with beads_task_id: {stats['events_with_task_id']} ({stats['correlation_rate']:.1f}%)")
        print(f"Events with trace_id: {stats['events_with_trace_id']}")
        print(f"Events with both: {stats['events_with_both']}")
        print(f"")
        print(f"Unique beads tasks referenced: {stats['unique_task_ids']}")
        print(f"Unique trace IDs: {stats['unique_trace_ids']}")
        print(f"")
        print("Integration Quality:")
        if stats['correlation_rate'] >= 80:
            print(f"  ✅ Excellent ({stats['correlation_rate']:.1f}% correlation)")
        elif stats['correlation_rate'] >= 50:
            print(f"  ⚠️  Good ({stats['correlation_rate']:.1f}% correlation)")
        else:
            print(f"  ❌ Needs improvement ({stats['correlation_rate']:.1f}% correlation)")

        return 0

    if args.action == "events-for-task":
        if not args.task_id:
            parser.error("--task-id required for events-for-task action")

        matching_events = find_events_for_task(events, args.task_id)

        if args.json:
            print(json.dumps(matching_events, indent=2))
            return 0

        print(f"A-MEM Events for Beads Task: {args.task_id}")
        print("=" * 80)
        print(f"Found {len(matching_events)} event(s)")
        print()

        for event in matching_events:
            print(f"Event Type: {event.get('event_type')}")
            print(f"Timestamp: {event.get('timestamp')}")
            print(f"Trace ID: {event.get('trace_id', 'N/A')}")
            if event.get('notes'):
                print(f"Notes: {event.get('notes')}")
            print("-" * 80)

        return 0

    if args.action == "tasks-for-trace":
        if not args.trace_id:
            parser.error("--trace-id required for tasks-for-trace action")

        matching_tasks = find_tasks_for_trace(args.trace_id)
        matching_events = find_events_for_trace(events, args.trace_id)

        if args.json:
            print(json.dumps({
                "tasks": matching_tasks,
                "events": matching_events
            }, indent=2))
            return 0

        print(f"Beads Tasks + A-MEM Events for Trace: {args.trace_id}")
        print("=" * 80)
        print()

        print(f"📋 Beads Tasks ({len(matching_tasks)}):")
        print("-" * 80)
        for task in matching_tasks:
            print(f"  {task['id']}: {task['title']}")
            print(f"  Status: {task['status']}")
            print(f"  Created: {task.get('created_at', 'N/A')}")
            print()

        print(f"📝 A-MEM Events ({len(matching_events)}):")
        print("-" * 80)
        for event in matching_events:
            print(f"  {event.get('event_type')} - {event.get('timestamp')}")
            if event.get('beads_task_id'):
                print(f"  Beads Task: {event.get('beads_task_id')}")
            if event.get('notes'):
                print(f"  Notes: {event.get('notes')}")
            print()

        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
