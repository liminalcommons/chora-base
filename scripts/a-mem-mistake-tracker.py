#!/usr/bin/env python3
"""
A-MEM Repeated Mistake Tracker

Logs mistakes and tracks recurrence to measure SAP-010 ROI metric: "30% reduction in repeated mistakes"

Usage:
    # Log a new mistake
    python scripts/a-mem-mistake-tracker.py "Jinja2 undefined variable" --resolved

    # Log mistake with knowledge note created
    python scripts/a-mem-mistake-tracker.py "Git merge conflict" --resolved --note git-merge-strategy.md

    # Check if mistake occurred before
    python scripts/a-mem-mistake-tracker.py "Jinja2 undefined variable" --check

    # Show metrics
    python scripts/a-mem-mistake-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def log_mistake_event(
    error_type: str,
    resolved: bool,
    note_created: Optional[str],
    recurrence: int,
    session_id: str,
    events_dir: Path
) -> dict:
    """Log mistake event to events/mistakes.jsonl"""
    events_dir.mkdir(parents=True, exist_ok=True)

    event = {
        "event_type": "mistake",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "error_type": error_type,
        "resolved": resolved,
        "note_created": note_created,
        "recurrence": recurrence,
        "session_id": session_id,
        "tags": ["sap-010", "a-mem", "mistake-tracking", "roi-tracking"]
    }

    mistakes_log = events_dir / "mistakes.jsonl"
    with open(mistakes_log, "a", encoding='utf-8') as f:
        f.write(json.dumps(event) + "\n")

    return event


def measure_recurrence(error_type: str, events_dir: Path) -> int:
    """Count how many times this error has occurred"""
    mistakes_log = events_dir / "mistakes.jsonl"

    if not mistakes_log.exists():
        return 0

    count = 0
    with open(mistakes_log, "r", encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("error_type") == error_type:
                count += 1

    return count


def get_all_mistakes(events_dir: Path) -> List[dict]:
    """Get all logged mistakes"""
    mistakes_log = events_dir / "mistakes.jsonl"

    if not mistakes_log.exists():
        return []

    mistakes = []
    with open(mistakes_log, "r", encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            mistakes.append(json.loads(line))

    return mistakes


def calculate_reduction_metrics(events_dir: Path, baseline_days: int = 30) -> dict:
    """
    Calculate repeated mistake reduction percentage.

    Compares recent period to baseline period.
    """
    from datetime import timedelta


# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    mistakes = get_all_mistakes(events_dir)

    if not mistakes:
        return {
            "total_mistakes": 0,
            "repeated_mistakes": 0,
            "reduction_percentage": 0.0,
            "target": 30.0
        }

    # Parse timestamps
    for mistake in mistakes:
        mistake["datetime"] = datetime.fromisoformat(mistake["timestamp"].replace("Z", "+00:00"))

    # Sort by timestamp
    mistakes.sort(key=lambda m: m["datetime"])

    if not mistakes:
        return {
            "total_mistakes": 0,
            "repeated_mistakes": 0,
            "reduction_percentage": 0.0,
            "target": 30.0
        }

    # Split into baseline and recent
    latest = mistakes[-1]["datetime"]
    baseline_cutoff = latest - timedelta(days=baseline_days * 2)
    recent_cutoff = latest - timedelta(days=baseline_days)

    baseline_mistakes = [m for m in mistakes if baseline_cutoff <= m["datetime"] < recent_cutoff]
    recent_mistakes = [m for m in mistakes if m["datetime"] >= recent_cutoff]

    # Count repeated mistakes (recurrence > 1)
    baseline_repeated = sum(1 for m in baseline_mistakes if m.get("recurrence", 0) > 1)
    recent_repeated = sum(1 for m in recent_mistakes if m.get("recurrence", 0) > 1)

    # Calculate reduction
    if len(baseline_mistakes) == 0:
        reduction_percentage = 0.0
    else:
        baseline_repeat_rate = baseline_repeated / len(baseline_mistakes) * 100
        recent_repeat_rate = recent_repeated / len(recent_mistakes) * 100 if recent_mistakes else 0
        reduction_percentage = baseline_repeat_rate - recent_repeat_rate

    return {
        "total_mistakes": len(mistakes),
        "baseline_mistakes": len(baseline_mistakes),
        "recent_mistakes": len(recent_mistakes),
        "baseline_repeated": baseline_repeated,
        "recent_repeated": recent_repeated,
        "reduction_percentage": reduction_percentage,
        "target": 30.0,
        "meets_target": reduction_percentage >= 30.0
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM mistake tracker for ROI validation"
    )
    parser.add_argument(
        "error_type",
        nargs="?",
        help="Error type or description (e.g., 'Jinja2 undefined variable')"
    )
    parser.add_argument(
        "--resolved",
        action="store_true",
        help="Mark mistake as resolved"
    )
    parser.add_argument(
        "--note",
        help="Knowledge note created (e.g., jinja2-fix.md)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if this mistake occurred before"
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
        help="Show mistake reduction metrics"
    )

    args = parser.parse_args()

    # Resolve paths
    memory_dir = Path(args.memory_dir)
    events_dir = memory_dir / "events"

    # Show metrics if requested
    if args.metrics:
        metrics = calculate_reduction_metrics(events_dir)
        print("📊 Repeated Mistake Reduction Metrics:")
        print(f"  Total mistakes logged: {metrics['total_mistakes']}")
        print(f"  Baseline period mistakes: {metrics['baseline_mistakes']}")
        print(f"  Recent period mistakes: {metrics['recent_mistakes']}")
        print(f"  Baseline repeated: {metrics['baseline_repeated']}")
        print(f"  Recent repeated: {metrics['recent_repeated']}")
        print(f"  Reduction: {metrics['reduction_percentage']:.1f}%")
        print(f"  Target: ≥{metrics['target']:.0f}%")

        if metrics['meets_target']:
            print(f"  ✅ Target met!")
        else:
            print(f"  ⏳ Need {metrics['target'] - metrics['reduction_percentage']:.1f}% more reduction")

        return 0

    if not args.error_type:
        parser.error("error_type is required unless --metrics is specified")

    # Check if mistake occurred before
    recurrence = measure_recurrence(args.error_type, events_dir)

    if args.check:
        print(f"🔍 Checking: {args.error_type}")
        if recurrence == 0:
            print(f"✅ First time encountering this error")
        else:
            print(f"⚠️  This error has occurred {recurrence} time(s) before")
            print(f"   Check .chora/memory/events/mistakes.jsonl for details")

        # Look for related knowledge notes
        knowledge_dir = memory_dir / "knowledge"
        if knowledge_dir.exists():
            related_notes = []
            for note in knowledge_dir.glob("*.md"):
                content = note.read_text().lower()
                if args.error_type.lower() in content:
                    related_notes.append(note.name)

            if related_notes:
                print(f"\n📚 Related knowledge notes:")
                for note in related_notes:
                    print(f"   - {note}")

        return 0

    # Get session ID
    session_id = args.session_id or datetime.utcnow().strftime("%Y-%m-%d-%H")

    # Log mistake event
    event = log_mistake_event(
        args.error_type,
        args.resolved,
        args.note,
        recurrence,
        session_id,
        events_dir
    )

    # Display confirmation
    print(f"📝 Mistake logged")
    print(f"❌ Error: {args.error_type}")
    print(f"🔢 Occurrence: #{recurrence + 1}")

    if recurrence > 0:
        print(f"⚠️  WARNING: This is a repeated mistake!")
        print(f"   Occurred {recurrence} time(s) previously")

    if args.resolved:
        print(f"✅ Status: Resolved")

    if args.note:
        print(f"📚 Knowledge note created: {args.note}")
        print(f"   Next time this occurs, check the note first!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
