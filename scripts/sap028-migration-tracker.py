#!/usr/bin/env python3
"""
SAP-028 Migration Time Tracker

Tracks migration time from token-based to OIDC trusted publishing.

Usage:
    # Start migration timer
    python scripts/sap028-migration-tracker.py start --project my-package

    # End migration timer
    python scripts/sap028-migration-tracker.py end --project my-package --time 15 --success

    # Show metrics
    python scripts/sap028-migration-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List


def load_events(events_path: Path) -> List[dict]:
    """Load migration events from JSONL file"""
    if not events_path.exists():
        return []

    events = []
    with open(events_path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def log_migration_event(
    action: str,
    project: str,
    success: bool,
    migration_time_minutes: float,
    secrets_removed: int,
    pep740_enabled: bool,
    events_path: Path,
    session_id: str
) -> dict:
    """Log migration time event"""
    event = {
        "event_type": "sap028_migration",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,  # "start" or "end"
        "project": project,
        "success": success,
        "migration_time_minutes": migration_time_minutes,
        "secrets_removed": secrets_removed,
        "pep740_enabled": pep740_enabled,
        "session_id": session_id,
        "tags": ["sap-028", "migration", "token-to-oidc", "roi-tracking"]
    }

    # Append to events log
    with open(events_path, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_metrics(events_path: Path) -> dict:
    """Calculate migration time metrics"""
    events = load_events(events_path)

    if not events:
        return {
            "total_migrations": 0,
            "successful_migrations": 0,
            "avg_migration_time_minutes": 0.0,
            "target_minutes": 15.0,
            "meets_target": False,
            "total_secrets_removed": 0
        }

    end_events = [e for e in events if e.get("action") == "end"]
    successful = [e for e in end_events if e.get("success")]

    avg_time = (
        sum(e.get("migration_time_minutes", 0) for e in successful) / len(successful)
        if successful else 0.0
    )

    total_secrets = sum(e.get("secrets_removed", 0) for e in successful)

    return {
        "total_migrations": len(end_events),
        "successful_migrations": len(successful),
        "failed_migrations": len(end_events) - len(successful),
        "avg_migration_time_minutes": avg_time,
        "target_minutes": 15.0,
        "meets_target": avg_time <= 15.0,
        "total_secrets_removed": total_secrets,
        "pep740_enabled_count": sum(1 for e in successful if e.get("pep740_enabled"))
    }


def main():
    parser = argparse.ArgumentParser(
        description="Track SAP-028 token→OIDC migration time"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["start", "end"],
        help="Start or end migration timer"
    )
    parser.add_argument(
        "--project",
        help="Project name"
    )
    parser.add_argument(
        "--success",
        action="store_true",
        help="Migration completed successfully"
    )
    parser.add_argument(
        "--time",
        type=float,
        default=15.0,
        help="Migration time in minutes (default: 15.0)"
    )
    parser.add_argument(
        "--secrets-removed",
        type=int,
        default=1,
        help="Number of PYPI_API_TOKEN secrets removed (default: 1)"
    )
    parser.add_argument(
        "--pep740",
        action="store_true",
        help="PEP 740 attestations enabled"
    )
    parser.add_argument(
        "--session-id",
        default="default",
        help="Session identifier"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show migration time metrics"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory"
    )

    args = parser.parse_args()

    events_dir = Path(args.events_dir)
    events_dir.mkdir(parents=True, exist_ok=True)
    events_path = events_dir / "sap028-migration.jsonl"

    if args.metrics:
        metrics = calculate_metrics(events_path)
        print(f"SAP-028 Migration Time Metrics")
        print(f"===============================")
        print(f"Total migrations: {metrics['total_migrations']}")
        print(f"Successful: {metrics['successful_migrations']}")
        print(f"Failed: {metrics['failed_migrations']}")
        print(f"Avg migration time: {metrics['avg_migration_time_minutes']:.1f} minutes")
        print(f"Target: ≤{metrics['target_minutes']:.0f} minutes")
        print(f"Status: {'✅ Met' if metrics['meets_target'] else '❌ Not met'}")
        print(f"")
        print(f"Security Impact:")
        print(f"  Total PYPI_API_TOKEN secrets removed: {metrics['total_secrets_removed']}")
        print(f"  Projects with PEP 740 attestations: {metrics['pep740_enabled_count']}")
        return 0

    if not args.action or not args.project:
        parser.error("action and --project required (or use --metrics)")

    event = log_migration_event(
        action=args.action,
        project=args.project,
        success=args.success if args.action == "end" else False,
        migration_time_minutes=args.time if args.action == "end" else 0.0,
        secrets_removed=args.secrets_removed if args.action == "end" else 0,
        pep740_enabled=args.pep740 if args.action == "end" else False,
        events_path=events_path,
        session_id=args.session_id
    )

    if args.action == "start":
        print(f"⏱️  Migration timer started for '{args.project}'")
        print(f"   Migrating from: Token-based publishing (PYPI_API_TOKEN)")
        print(f"   Migrating to: OIDC trusted publishing (zero secrets)")
        print(f"   Run with 'end' when migration complete")
    else:
        status = "✅ Success" if args.success else "❌ Failed"
        print(f"⏱️  Migration complete for '{args.project}': {status}")
        print(f"   Migration time: {args.time:.1f} minutes")
        print(f"   Target: ≤15.0 minutes")
        print(f"   {'✅ Target met!' if args.time <= 15.0 else '⚠️  Exceeded target'}")
        print(f"")
        print(f"Security improvements:")
        print(f"  - Secrets removed: {args.secrets_removed}")
        print(f"  - PEP 740 attestations: {'✅ Enabled' if args.pep740 else '❌ Not enabled'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
