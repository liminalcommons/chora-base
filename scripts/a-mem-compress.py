#!/usr/bin/env python3
"""
A-MEM Event Log Compression

Compresses old event logs to save disk space and improve query performance.

Usage:
    python scripts/a-mem-compress.py --age 30        # Compress events older than 30 days
    python scripts/a-mem-compress.py --all           # Compress all events
    python scripts/a-mem-compress.py --dry-run       # Show what would be compressed
"""

import argparse
import gzip
import json
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List


def get_event_age_days(event: dict) -> int:
    """Calculate age of event in days"""
    try:
        timestamp = event.get("timestamp", "")
        event_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        age = datetime.now(event_time.tzinfo) - event_time
        return age.days
    except Exception:
        return 0


def compress_event_log(
    log_path: Path,
    age_threshold_days: int,
    dry_run: bool = False
) -> dict:
    """
    Compress events older than threshold to .gz file.

    Returns stats about compression.
    """
    if not log_path.exists():
        return {"compressed": 0, "kept": 0, "error": "Log file not found"}

    # Read all events
    events = []
    with open(log_path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    # Split into old and recent
    old_events = []
    recent_events = []

    for event in events:
        age_days = get_event_age_days(event)
        if age_days >= age_threshold_days:
            old_events.append(event)
        else:
            recent_events.append(event)

    # Calculate compression stats
    original_size = log_path.stat().st_size
    compressed_count = len(old_events)
    kept_count = len(recent_events)

    if dry_run:
        return {
            "log": log_path.name,
            "compressed": compressed_count,
            "kept": kept_count,
            "original_size_kb": original_size / 1024,
            "dry_run": True
        }

    # Write compressed archive
    if old_events:
        archive_path = log_path.parent / f"{log_path.stem}-archive.jsonl.gz"

        # Append to existing archive if it exists
        if archive_path.exists():
            # Read existing archive
            with gzip.open(archive_path, "rt") as f:
                existing_events = [json.loads(line) for line in f if line.strip()]
            old_events = existing_events + old_events

        # Write compressed archive
        with gzip.open(archive_path, "wt") as f:
            for event in old_events:
                f.write(json.dumps(event) + "\n")

        compressed_size = archive_path.stat().st_size

    # Overwrite log with recent events only
    with open(log_path, "w") as f:
        for event in recent_events:
            f.write(json.dumps(event) + "\n")

    new_size = log_path.stat().st_size

    return {
        "log": log_path.name,
        "compressed": compressed_count,
        "kept": kept_count,
        "original_size_kb": original_size / 1024,
        "new_size_kb": new_size / 1024,
        "compressed_size_kb": compressed_size / 1024 if old_events else 0,
        "space_saved_kb": (original_size - new_size) / 1024
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM event log compression"
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Compress events older than N days (default: 30)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Compress all events (use with caution)"
    )
    parser.add_argument(
        "--memory-dir",
        default=".chora/memory",
        help="A-MEM directory (default: .chora/memory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be compressed without actually compressing"
    )

    args = parser.parse_args()

    # Resolve paths
    memory_dir = Path(args.memory_dir)
    events_dir = memory_dir / "events"

    if not events_dir.exists():
        print(f"⚠️  Events directory not found: {events_dir}", file=sys.stderr)
        return 1

    # Get all event logs
    event_logs = list(events_dir.glob("*.jsonl"))

    if not event_logs:
        print(f"ℹ️  No event logs found in {events_dir}")
        return 0

    print(f"🗜️  A-MEM Event Log Compression")
    print(f"   Age threshold: {args.age} days")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}\n")

    # Compress each log
    total_compressed = 0
    total_space_saved = 0

    for log_path in event_logs:
        result = compress_event_log(log_path, args.age, args.dry_run)

        print(f"📄 {result['log']}")
        print(f"   Events compressed: {result['compressed']}")
        print(f"   Events kept: {result['kept']}")
        print(f"   Original size: {result['original_size_kb']:.1f} KB")

        if not args.dry_run:
            print(f"   New size: {result['new_size_kb']:.1f} KB")
            print(f"   Compressed archive: {result['compressed_size_kb']:.1f} KB")
            print(f"   Space saved: {result['space_saved_kb']:.1f} KB")

        total_compressed += result['compressed']
        if not args.dry_run:
            total_space_saved += result.get('space_saved_kb', 0)

        print()

    print(f"✅ Summary:")
    print(f"   Total events compressed: {total_compressed}")
    if not args.dry_run:
        print(f"   Total space saved: {total_space_saved:.1f} KB ({total_space_saved / 1024:.2f} MB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
