#!/usr/bin/env python3
"""
SAP-015 Dependency Blocker Resolution Time Tracker

Tracks time blocked work stays blocked before being resolved.

Usage:
    # Log when task becomes blocked
    python scripts/sap015-dependency-tracker.py blocked --project my-project --task-id abc-123 --blocker-id xyz-456

    # Log when blocker is resolved
    python scripts/sap015-dependency-tracker.py unblocked --project my-project --task-id abc-123 --blocked-hours 48

    # Show metrics
    python scripts/sap015-dependency-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List


def load_events(events_path: Path) -> List[dict]:
    """Load dependency blocker events from JSONL file"""
    if not events_path.exists():
        return []

    events = []
    with open(events_path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def log_dependency_event(
    action: str,
    project: str,
    task_id: str,
    blocker_id: str,
    blocked_hours: float,
    events_path: Path
) -> dict:
    """Log dependency blocker event"""
    event = {
        "event_type": "sap015_dependency_blocker",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,  # "blocked" or "unblocked"
        "project": project,
        "task_id": task_id,
        "blocker_id": blocker_id,
        "blocked_hours": blocked_hours if action == "unblocked" else 0.0,
        "tags": ["sap-015", "dependency", "roi-tracking", "beads"]
    }

    # Append to events log
    with open(events_path, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_metrics(events_path: Path) -> dict:
    """Calculate dependency blocker metrics"""
    events = load_events(events_path)

    if not events:
        return {
            "total_blocks": 0,
            "total_unblocks": 0,
            "avg_blocked_hours": 0.0,
            "median_blocked_hours": 0.0,
            "currently_blocked": 0
        }

    blocked_events = [e for e in events if e.get("action") == "blocked"]
    unblocked_events = [e for e in events if e.get("action") == "unblocked"]

    blocked_times = [e.get("blocked_hours", 0) for e in unblocked_events if e.get("blocked_hours", 0) > 0]

    avg_blocked = (
        sum(blocked_times) / len(blocked_times)
        if blocked_times else 0.0
    )

    median_blocked = 0.0
    if blocked_times:
        sorted_times = sorted(blocked_times)
        mid = len(sorted_times) // 2
        median_blocked = sorted_times[mid] if len(sorted_times) % 2 == 1 else (sorted_times[mid-1] + sorted_times[mid]) / 2

    currently_blocked = len(blocked_events) - len(unblocked_events)

    return {
        "total_blocks": len(blocked_events),
        "total_unblocks": len(unblocked_events),
        "avg_blocked_hours": avg_blocked,
        "median_blocked_hours": median_blocked,
        "currently_blocked": max(0, currently_blocked)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Track SAP-015 dependency blocker resolution time"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["blocked", "unblocked"],
        help="Log blocked or unblocked event"
    )
    parser.add_argument(
        "--project",
        help="Project name"
    )
    parser.add_argument(
        "--task-id",
        help="Blocked task ID"
    )
    parser.add_argument(
        "--blocker-id",
        help="Blocker task ID"
    )
    parser.add_argument(
        "--blocked-hours",
        type=float,
        help="Hours task was blocked (for unblocked action)"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show dependency blocker metrics"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory"
    )

    args = parser.parse_args()

    events_dir = Path(args.events_dir)
    events_dir.mkdir(parents=True, exist_ok=True)
    events_path = events_dir / "sap015-dependency.jsonl"

    if args.metrics:
        metrics = calculate_metrics(events_path)
        print(f"SAP-015 Dependency Blocker Metrics")
        print(f"===================================")
        print(f"Total blocked events: {metrics['total_blocks']}")
        print(f"Total unblocked events: {metrics['total_unblocks']}")
        print(f"Currently blocked: {metrics['currently_blocked']} tasks")
        print(f"")
        print(f"Blocked work resolution time:")
        print(f"  Average: {metrics['avg_blocked_hours']:.1f} hours")
        print(f"  Median: {metrics['median_blocked_hours']:.1f} hours")
        return 0

    if not args.action or not args.project or not args.task_id or not args.blocker_id:
        parser.error("action, --project, --task-id, and --blocker-id required (or use --metrics)")

    if args.action == "unblocked" and args.blocked_hours is None:
        parser.error("--blocked-hours required for unblocked action")

    event = log_dependency_event(
        action=args.action,
        project=args.project,
        task_id=args.task_id,
        blocker_id=args.blocker_id,
        blocked_hours=args.blocked_hours if args.action == "unblocked" else 0.0,
        events_path=events_path
    )

    if args.action == "blocked":
        print(f"🔒 Task blocked: '{args.task_id}' blocked by '{args.blocker_id}'")
        print(f"   Project: {args.project}")
    else:
        print(f"🔓 Task unblocked: '{args.task_id}'")
        print(f"   Blocker: {args.blocker_id}")
        print(f"   Blocked for: {args.blocked_hours:.1f} hours")

    return 0


if __name__ == "__main__":
    sys.exit(main())
