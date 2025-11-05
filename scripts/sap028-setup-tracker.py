#!/usr/bin/env python3
"""
SAP-028 Setup Time Tracker

Tracks setup time for new projects adopting OIDC trusted publishing.

Usage:
    # Start setup timer
    python scripts/sap028-setup-tracker.py start --project my-package

    # End setup timer
    python scripts/sap028-setup-tracker.py end --project my-package --success

    # Show metrics
    python scripts/sap028-setup-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List


def load_events(events_path: Path) -> List[dict]:
    """Load setup events from JSONL file"""
    if not events_path.exists():
        return []

    events = []
    with open(events_path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def log_setup_event(
    action: str,
    project: str,
    success: bool,
    setup_time_minutes: float,
    events_path: Path,
    session_id: str
) -> dict:
    """Log setup time event"""
    event = {
        "event_type": "sap028_setup",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,  # "start" or "end"
        "project": project,
        "success": success,
        "setup_time_minutes": setup_time_minutes,
        "session_id": session_id,
        "tags": ["sap-028", "setup-time", "roi-tracking"]
    }

    # Append to events log
    with open(events_path, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_metrics(events_path: Path) -> dict:
    """Calculate setup time metrics"""
    events = load_events(events_path)

    if not events:
        return {
            "total_setups": 0,
            "successful_setups": 0,
            "avg_setup_time_minutes": 0.0,
            "target_minutes": 5.0,
            "meets_target": False
        }

    end_events = [e for e in events if e.get("action") == "end"]
    successful = [e for e in end_events if e.get("success")]

    avg_time = (
        sum(e.get("setup_time_minutes", 0) for e in successful) / len(successful)
        if successful else 0.0
    )

    return {
        "total_setups": len(end_events),
        "successful_setups": len(successful),
        "failed_setups": len(end_events) - len(successful),
        "avg_setup_time_minutes": avg_time,
        "target_minutes": 5.0,
        "meets_target": avg_time <= 5.0
    }


def main():
    parser = argparse.ArgumentParser(
        description="Track SAP-028 OIDC setup time"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["start", "end"],
        help="Start or end setup timer"
    )
    parser.add_argument(
        "--project",
        help="Project name"
    )
    parser.add_argument(
        "--success",
        action="store_true",
        help="Setup completed successfully"
    )
    parser.add_argument(
        "--time",
        type=float,
        default=5.0,
        help="Setup time in minutes (default: 5.0)"
    )
    parser.add_argument(
        "--session-id",
        default="default",
        help="Session identifier"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show setup time metrics"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory"
    )

    args = parser.parse_args()

    events_dir = Path(args.events_dir)
    events_dir.mkdir(parents=True, exist_ok=True)
    events_path = events_dir / "sap028-setup.jsonl"

    if args.metrics:
        metrics = calculate_metrics(events_path)
        print(f"SAP-028 Setup Time Metrics")
        print(f"===========================")
        print(f"Total setups: {metrics['total_setups']}")
        print(f"Successful: {metrics['successful_setups']}")
        print(f"Failed: {metrics['failed_setups']}")
        print(f"Avg setup time: {metrics['avg_setup_time_minutes']:.1f} minutes")
        print(f"Target: ≤{metrics['target_minutes']:.0f} minutes")
        print(f"Status: {'✅ Met' if metrics['meets_target'] else '❌ Not met'}")
        return 0

    if not args.action or not args.project:
        parser.error("action and --project required (or use --metrics)")

    event = log_setup_event(
        action=args.action,
        project=args.project,
        success=args.success if args.action == "end" else False,
        setup_time_minutes=args.time if args.action == "end" else 0.0,
        events_path=events_path,
        session_id=args.session_id
    )

    if args.action == "start":
        print(f"⏱️  Setup timer started for '{args.project}'")
        print(f"   Session ID: {args.session_id}")
        print(f"   Run with 'end' when setup complete")
    else:
        status = "✅ Success" if args.success else "❌ Failed"
        print(f"⏱️  Setup complete for '{args.project}': {status}")
        print(f"   Setup time: {args.time:.1f} minutes")
        print(f"   Target: ≤5.0 minutes")
        print(f"   {'✅ Target met!' if args.time <= 5.0 else '⚠️  Exceeded target'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
