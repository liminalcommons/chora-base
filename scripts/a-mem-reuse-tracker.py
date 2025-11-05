#!/usr/bin/env python3
"""
A-MEM Note Reuse Tracker

Logs when knowledge notes are reused to track SAP-010 ROI metric: "Note reuse ≥50%"

Usage:
    python scripts/a-mem-reuse-tracker.py sap-maturity-assessment-2025-11.md "Applied L3 criteria"
    python scripts/a-mem-reuse-tracker.py jinja2-fix.md "Fixed template bug" --time-saved 15
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def log_reuse_event(
    note_id: str,
    context: str,
    time_saved_minutes: int,
    session_id: str,
    events_dir: Path
) -> dict:
    """Log knowledge note reuse event"""
    events_dir.mkdir(parents=True, exist_ok=True)

    event = {
        "event_type": "knowledge_reuse",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "note_id": note_id,
        "context": context,
        "time_saved_minutes": time_saved_minutes,
        "session_id": session_id,
        "tags": ["sap-010", "a-mem", "reuse", "roi-tracking"]
    }

    reuse_log = events_dir / "knowledge-reuse.jsonl"
    with open(reuse_log, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_reuse_metrics(knowledge_dir: Path, events_dir: Path) -> dict:
    """
    Calculate note reuse percentage.

    Reuse % = (notes with ≥1 reuse event) / (total notes)
    """
    if not knowledge_dir.exists():
        return {"total_notes": 0, "reused_notes": 0, "reuse_percentage": 0.0}

    # Count total notes
    total_notes = len(list(knowledge_dir.glob("*.md")))

    # Count reused notes
    reuse_log = events_dir / "knowledge-reuse.jsonl"
    if not reuse_log.exists():
        return {
            "total_notes": total_notes,
            "reused_notes": 0,
            "reuse_percentage": 0.0,
            "target": 50.0
        }

    reused_note_ids = set()
    total_time_saved = 0

    with open(reuse_log, "r") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            reused_note_ids.add(event.get("note_id"))
            total_time_saved += event.get("time_saved_minutes", 0)

    reuse_percentage = (len(reused_note_ids) / total_notes * 100) if total_notes > 0 else 0.0

    return {
        "total_notes": total_notes,
        "reused_notes": len(reused_note_ids),
        "reuse_percentage": reuse_percentage,
        "target": 50.0,
        "meets_target": reuse_percentage >= 50.0,
        "total_time_saved_minutes": total_time_saved
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM note reuse tracker for ROI validation"
    )
    parser.add_argument("note_id", help="Knowledge note filename (e.g., jinja2-fix.md)")
    parser.add_argument("context", help="How the note was used (e.g., 'Fixed template bug')")
    parser.add_argument(
        "--time-saved",
        type=int,
        default=0,
        help="Estimated time saved in minutes (default: 0)"
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
        help="Show reuse metrics after logging"
    )

    args = parser.parse_args()

    # Resolve paths
    memory_dir = Path(args.memory_dir)
    knowledge_dir = memory_dir / "knowledge"
    events_dir = memory_dir / "events"

    # Get session ID
    session_id = args.session_id or datetime.utcnow().strftime("%Y-%m-%d-%H")

    # Verify note exists
    note_path = knowledge_dir / args.note_id
    if not note_path.exists():
        print(f"⚠️  Warning: Note not found: {args.note_id}", file=sys.stderr)
        print(f"   (logging reuse event anyway)", file=sys.stderr)

    # Log reuse event
    event = log_reuse_event(
        args.note_id,
        args.context,
        args.time_saved,
        session_id,
        events_dir
    )

    # Display confirmation
    print(f"✅ Knowledge reuse logged")
    print(f"📄 Note: {args.note_id}")
    print(f"🎯 Context: {args.context}")

    if args.time_saved > 0:
        print(f"⏱️  Time saved: {args.time_saved} minutes")

    # Show metrics if requested
    if args.metrics:
        metrics = calculate_reuse_metrics(knowledge_dir, events_dir)
        print(f"\n📊 Reuse Metrics:")
        print(f"  Total notes: {metrics['total_notes']}")
        print(f"  Reused notes: {metrics['reused_notes']}")
        print(f"  Reuse percentage: {metrics['reuse_percentage']:.1f}%")
        print(f"  Target: ≥{metrics['target']:.0f}%")

        if metrics['meets_target']:
            print(f"  ✅ Target met!")
        else:
            needed = int(metrics['total_notes'] * 0.5 - metrics['reused_notes'])
            print(f"  ⏳ Need {needed} more notes reused")

        if metrics['total_time_saved_minutes'] > 0:
            print(f"\n  Total time saved: {metrics['total_time_saved_minutes']} minutes ({metrics['total_time_saved_minutes'] / 60:.1f} hours)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
