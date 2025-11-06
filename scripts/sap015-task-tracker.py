#!/usr/bin/env python3
"""
SAP-015 Task Completion Velocity Tracker

Tracks task completion velocity to measure productivity with beads.

Usage:
    # Log completed task
    python scripts/sap015-task-tracker.py log --project my-project --task-id abc-123 --completion-time 2.5

    # Show metrics
    python scripts/sap015-task-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List


def load_events(events_path: Path) -> List[dict]:
    """Load task completion events from JSONL file"""
    if not events_path.exists():
        return []

    events = []
    with open(events_path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def log_task_event(
    project: str,
    task_id: str,
    completion_time_hours: float,
    had_blockers: bool,
    events_path: Path
) -> dict:
    """Log task completion event"""
    event = {
        "event_type": "sap015_task_completion",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": project,
        "task_id": task_id,
        "completion_time_hours": completion_time_hours,
        "had_blockers": had_blockers,
        "tags": ["sap-015", "task-velocity", "roi-tracking", "beads"]
    }

    # Append to events log
    with open(events_path, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_metrics(events_path: Path) -> dict:
    """Calculate task completion velocity metrics"""
    events = load_events(events_path)

    if not events:
        return {
            "total_tasks": 0,
            "avg_completion_time_hours": 0.0,
            "tasks_with_blockers": 0,
            "tasks_without_blockers": 0,
            "velocity_tasks_per_week": 0.0
        }

    total_tasks = len(events)
    tasks_with_blockers = sum(1 for e in events if e.get("had_blockers"))
    tasks_without_blockers = total_tasks - tasks_with_blockers

    avg_time = (
        sum(e.get("completion_time_hours", 0) for e in events) / len(events)
        if events else 0.0
    )

    # Estimate tasks per week based on avg completion time
    # Assume 40 work hours per week
    velocity = (40.0 / avg_time) if avg_time > 0 else 0.0

    return {
        "total_tasks": total_tasks,
        "avg_completion_time_hours": avg_time,
        "tasks_with_blockers": tasks_with_blockers,
        "tasks_without_blockers": tasks_without_blockers,
        "velocity_tasks_per_week": velocity
    }


def main():
    parser = argparse.ArgumentParser(
        description="Track SAP-015 task completion velocity"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["log"],
        help="Log task completion event"
    )
    parser.add_argument(
        "--project",
        help="Project name"
    )
    parser.add_argument(
        "--task-id",
        help="Beads task ID"
    )
    parser.add_argument(
        "--completion-time",
        type=float,
        help="Task completion time (hours)"
    )
    parser.add_argument(
        "--had-blockers",
        action="store_true",
        help="Task had dependency blockers"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show task completion velocity metrics"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory"
    )

    args = parser.parse_args()

    events_dir = Path(args.events_dir)
    events_dir.mkdir(parents=True, exist_ok=True)
    events_path = events_dir / "sap015-task.jsonl"

    if args.metrics:
        metrics = calculate_metrics(events_path)
        print(f"SAP-015 Task Completion Velocity Metrics")
        print(f"==========================================")
        print(f"Total tasks completed: {metrics['total_tasks']}")
        print(f"  With blockers: {metrics['tasks_with_blockers']}")
        print(f"  Without blockers: {metrics['tasks_without_blockers']}")
        print(f"")
        print(f"Avg completion time: {metrics['avg_completion_time_hours']:.1f} hours")
        print(f"Velocity: {metrics['velocity_tasks_per_week']:.1f} tasks/week")
        print(f"")
        print(f"(Based on 40-hour work week)")
        return 0

    if not args.action or not args.project or not args.task_id or args.completion_time is None:
        parser.error("action, --project, --task-id, and --completion-time required (or use --metrics)")

    event = log_task_event(
        project=args.project,
        task_id=args.task_id,
        completion_time_hours=args.completion_time,
        had_blockers=args.had_blockers,
        events_path=events_path
    )

    blocker_status = "WITH blockers" if args.had_blockers else "NO blockers"
    print(f"✅ Task completion logged for '{args.project}': {blocker_status}")
    print(f"   Task ID: {args.task_id}")
    print(f"   Completion time: {args.completion_time:.1f} hours")

    return 0


if __name__ == "__main__":
    sys.exit(main())
