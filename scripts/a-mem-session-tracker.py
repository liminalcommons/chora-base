#!/usr/bin/env python3
"""
A-MEM Session & Context Restoration Tracker

Tracks session start times and context restoration to measure SAP-010 ROI metric:
"80% time saved on context restoration"

Usage:
    # Log session start with A-MEM context
    python scripts/a-mem-session-tracker.py start --with-memory --restoration-time 5

    # Log session start without A-MEM (baseline)
    python scripts/a-mem-session-tracker.py start --baseline --restoration-time 180

    # Show metrics
    python scripts/a-mem-session-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def log_session_event(
    action: str,
    with_memory: bool,
    restoration_time_seconds: int,
    baseline_time_seconds: int,
    session_id: str,
    events_dir: Path
) -> dict:
    """Log session event to events/sessions.jsonl"""
    events_dir.mkdir(parents=True, exist_ok=True)

    event = {
        "event_type": "session",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,  # "start" or "end"
        "context_restored_from_memory": with_memory,
        "restoration_time_seconds": restoration_time_seconds,
        "manual_context_baseline_seconds": baseline_time_seconds,
        "time_saved_seconds": baseline_time_seconds - restoration_time_seconds if with_memory else 0,
        "session_id": session_id,
        "tags": ["sap-010", "a-mem", "session-tracking", "roi-tracking"]
    }

    sessions_log = events_dir / "sessions.jsonl"
    with open(sessions_log, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def get_all_sessions(events_dir: Path) -> List[dict]:
    """Get all logged session events"""
    sessions_log = events_dir / "sessions.jsonl"

    if not sessions_log.exists():
        return []

    sessions = []
    with open(sessions_log, "r") as f:
        for line in f:
            if not line.strip():
                continue
            sessions.append(json.loads(line))

    return sessions


def calculate_restoration_metrics(events_dir: Path) -> dict:
    """
    Calculate context restoration time savings.

    Time saved % = (baseline_avg - with_memory_avg) / baseline_avg * 100
    """
    sessions = get_all_sessions(events_dir)

    if not sessions:
        return {
            "total_sessions": 0,
            "with_memory_sessions": 0,
            "baseline_sessions": 0,
            "avg_restoration_with_memory": 0.0,
            "avg_restoration_baseline": 0.0,
            "time_saved_percentage": 0.0,
            "target": 80.0
        }

    # Filter session starts
    starts = [s for s in sessions if s.get("action") == "start"]

    with_memory = [s for s in starts if s.get("context_restored_from_memory")]
    baseline = [s for s in starts if not s.get("context_restored_from_memory")]

    # Calculate averages
    avg_with_memory = (
        sum(s.get("restoration_time_seconds", 0) for s in with_memory) / len(with_memory)
        if with_memory else 0.0
    )

    avg_baseline = (
        sum(s.get("manual_context_baseline_seconds", 0) for s in baseline) / len(baseline)
        if baseline else 180.0  # Default baseline: 3 minutes
    )

    # Use baseline from with_memory sessions if no pure baseline sessions
    if not baseline and with_memory:
        avg_baseline = with_memory[0].get("manual_context_baseline_seconds", 180.0)

    # Calculate time saved percentage
    time_saved_percentage = ((avg_baseline - avg_with_memory) / avg_baseline * 100) if avg_baseline > 0 else 0.0

    return {
        "total_sessions": len(starts),
        "with_memory_sessions": len(with_memory),
        "baseline_sessions": len(baseline),
        "avg_restoration_with_memory": avg_with_memory,
        "avg_restoration_baseline": avg_baseline,
        "time_saved_percentage": time_saved_percentage,
        "total_time_saved_seconds": sum(s.get("time_saved_seconds", 0) for s in with_memory),
        "target": 80.0,
        "meets_target": time_saved_percentage >= 80.0
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM session and context restoration tracker for ROI validation"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["start", "end"],
        help="Session action (start or end)"
    )
    parser.add_argument(
        "--with-memory",
        action="store_true",
        help="Context was restored from A-MEM"
    )
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Baseline session (no A-MEM, manual context restoration)"
    )
    parser.add_argument(
        "--restoration-time",
        type=int,
        help="Time to restore context in seconds"
    )
    parser.add_argument(
        "--baseline-time",
        type=int,
        default=180,
        help="Baseline restoration time in seconds (default: 180s = 3min)"
    )
    parser.add_argument(
        "--session-id",
        help="Session ID (default: auto-generated)"
    )
    parser.add_argument(
        "--memory-dir",
        default=".chora/memory",
        help="A-MEM directory (default: .chora/memory)"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show context restoration metrics"
    )

    args = parser.parse_args()

    # Resolve paths
    memory_dir = Path(args.memory_dir)
    events_dir = memory_dir / "events"

    # Show metrics if requested
    if args.metrics:
        metrics = calculate_restoration_metrics(events_dir)
        print("📊 Context Restoration Metrics:")
        print(f"  Total sessions: {metrics['total_sessions']}")
        print(f"  With A-MEM: {metrics['with_memory_sessions']}")
        print(f"  Baseline (no A-MEM): {metrics['baseline_sessions']}")
        print(f"  Avg restoration time (A-MEM): {metrics['avg_restoration_with_memory']:.1f}s ({metrics['avg_restoration_with_memory'] / 60:.1f}min)")
        print(f"  Avg restoration time (baseline): {metrics['avg_restoration_baseline']:.1f}s ({metrics['avg_restoration_baseline'] / 60:.1f}min)")
        print(f"  Time saved: {metrics['time_saved_percentage']:.1f}%")
        print(f"  Target: ≥{metrics['target']:.0f}%")

        if metrics['meets_target']:
            print(f"  ✅ Target met!")
        else:
            print(f"  ⏳ Need {metrics['target'] - metrics['time_saved_percentage']:.1f}% more improvement")

        if metrics['total_time_saved_seconds'] > 0:
            total_saved_min = metrics['total_time_saved_seconds'] / 60
            print(f"\n  Total time saved: {total_saved_min:.1f} minutes ({total_saved_min / 60:.1f} hours)")

        return 0

    if not args.action:
        parser.error("action is required unless --metrics is specified")

    # Validate arguments
    if args.action == "start":
        if args.with_memory and args.baseline:
            parser.error("Cannot specify both --with-memory and --baseline")

        if not args.with_memory and not args.baseline:
            parser.error("Must specify either --with-memory or --baseline for session start")

        if args.restoration_time is None:
            parser.error("--restoration-time is required for session start")

    # Get session ID
    session_id = args.session_id or datetime.utcnow().strftime("%Y-%m-%d-%H")

    # Log session event
    event = log_session_event(
        args.action,
        args.with_memory,
        args.restoration_time or 0,
        args.baseline_time,
        session_id,
        events_dir
    )

    # Display confirmation
    print(f"✅ Session {args.action} logged")
    print(f"📁 Session ID: {session_id}")

    if args.action == "start":
        if args.with_memory:
            print(f"🧠 Context restored from A-MEM")
            print(f"⏱️  Restoration time: {args.restoration_time}s ({args.restoration_time / 60:.1f}min)")
            time_saved = args.baseline_time - args.restoration_time
            time_saved_pct = (time_saved / args.baseline_time * 100) if args.baseline_time > 0 else 0
            print(f"💡 Time saved: {time_saved}s ({time_saved / 60:.1f}min) = {time_saved_pct:.0f}% faster")
        else:
            print(f"📝 Baseline session (manual context restoration)")
            print(f"⏱️  Restoration time: {args.restoration_time}s ({args.restoration_time / 60:.1f}min)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
