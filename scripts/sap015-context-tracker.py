#!/usr/bin/env python3
"""
SAP-015 Context Re-establishment Time Tracker

Tracks time saved when resuming work with beads vs. without.

Usage:
    # Log session WITHOUT beads (baseline)
    python scripts/sap015-context-tracker.py log --project my-project --session-type baseline --context-time 15

    # Log session WITH beads (optimized)
    python scripts/sap015-context-tracker.py log --project my-project --session-type beads --context-time 3

    # Show metrics
    python scripts/sap015-context-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List



# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def load_events(events_path: Path) -> List[dict]:
    """Load context re-establishment events from JSONL file"""
    if not events_path.exists():
        return []

    events = []
    with open(events_path, "r", encoding='utf-8') as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def log_context_event(
    project: str,
    session_type: str,
    context_time_minutes: float,
    task_id: str,
    events_path: Path
) -> dict:
    """Log context re-establishment event"""
    event = {
        "event_type": "sap015_context_reestablishment",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": project,
        "session_type": session_type,  # "baseline" (no beads) or "beads"
        "context_time_minutes": context_time_minutes,
        "task_id": task_id if task_id else None,
        "tags": ["sap-015", "context", "roi-tracking", "beads"]
    }

    # Append to events log
    with open(events_path, "a", encoding='utf-8') as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_metrics(events_path: Path) -> dict:
    """Calculate context re-establishment metrics"""
    events = load_events(events_path)

    if not events:
        return {
            "total_sessions": 0,
            "baseline_avg_minutes": 0.0,
            "beads_avg_minutes": 0.0,
            "time_saved_minutes": 0.0,
            "percent_saved": 0.0,
            "target_percent": 20.0,
            "meets_target": False
        }

    baseline_events = [e for e in events if e.get("session_type") == "baseline"]
    beads_events = [e for e in events if e.get("session_type") == "beads"]

    baseline_avg = (
        sum(e.get("context_time_minutes", 0) for e in baseline_events) / len(baseline_events)
        if baseline_events else 0.0
    )

    beads_avg = (
        sum(e.get("context_time_minutes", 0) for e in beads_events) / len(beads_events)
        if beads_events else 0.0
    )

    time_saved = baseline_avg - beads_avg if baseline_avg > 0 else 0.0
    percent_saved = (time_saved / baseline_avg * 100) if baseline_avg > 0 else 0.0

    return {
        "total_sessions": len(events),
        "baseline_sessions": len(baseline_events),
        "beads_sessions": len(beads_events),
        "baseline_avg_minutes": baseline_avg,
        "beads_avg_minutes": beads_avg,
        "time_saved_minutes": time_saved,
        "percent_saved": percent_saved,
        "target_percent": 20.0,
        "meets_target": percent_saved >= 20.0
    }


def main():
    parser = argparse.ArgumentParser(
        description="Track SAP-015 context re-establishment time savings"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["log"],
        help="Log context re-establishment event"
    )
    parser.add_argument(
        "--project",
        help="Project name"
    )
    parser.add_argument(
        "--session-type",
        choices=["baseline", "beads"],
        help="Session type: baseline (no beads) or beads (with beads)"
    )
    parser.add_argument(
        "--context-time",
        type=float,
        help="Time spent re-establishing context (minutes)"
    )
    parser.add_argument(
        "--task-id",
        help="Beads task ID (if session-type=beads)"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show context re-establishment metrics"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory"
    )

    args = parser.parse_args()

    events_dir = Path(args.events_dir)
    events_dir.mkdir(parents=True, exist_ok=True)
    events_path = events_dir / "sap015-context.jsonl"

    if args.metrics:
        metrics = calculate_metrics(events_path)
        print(f"SAP-015 Context Re-establishment Metrics")
        print(f"=========================================")
        print(f"Total sessions: {metrics['total_sessions']}")
        print(f"  Baseline (no beads): {metrics['baseline_sessions']} sessions")
        print(f"  With beads: {metrics['beads_sessions']} sessions")
        print(f"")
        print(f"Average context time:")
        print(f"  Baseline: {metrics['baseline_avg_minutes']:.1f} minutes")
        print(f"  With beads: {metrics['beads_avg_minutes']:.1f} minutes")
        print(f"  Time saved: {metrics['time_saved_minutes']:.1f} minutes per session")
        print(f"")
        print(f"Percent saved: {metrics['percent_saved']:.1f}%")
        print(f"Target: ≥{metrics['target_percent']:.0f}%")
        print(f"Status: {'✅ Met' if metrics['meets_target'] else '❌ Not met'}")
        return 0

    if not args.action or not args.project or not args.session_type or args.context_time is None:
        parser.error("action, --project, --session-type, and --context-time required (or use --metrics)")

    event = log_context_event(
        project=args.project,
        session_type=args.session_type,
        context_time_minutes=args.context_time,
        task_id=args.task_id,
        events_path=events_path
    )

    session_label = "WITHOUT beads (baseline)" if args.session_type == "baseline" else "WITH beads"
    print(f"📝 Context re-establishment logged for '{args.project}': {session_label}")
    print(f"   Time to re-establish context: {args.context_time:.1f} minutes")
    if args.task_id:
        print(f"   Task ID: {args.task_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
