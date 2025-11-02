#!/usr/bin/env python3
"""
Inbox Query Tool - Agent-friendly inbox management interface

Provides structured queries for inbox items with filtering, sorting, and formatting.
Optimized for AI agent invocation with clear commands and machine-readable output.

Usage:
    # Check for new unacknowledged items
    python scripts/inbox-query.py --incoming --unacknowledged

    # View specific coordination request
    python scripts/inbox-query.py --request COORD-2025-006

    # List all items with specific status
    python scripts/inbox-query.py --status in_progress

    # Show items older than 3 days
    python scripts/inbox-query.py --incoming --age ">3d"

    # JSON output for parsing
    python scripts/inbox-query.py --incoming --format json

    # Count items by status
    python scripts/inbox-query.py --count-by-status
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re

# Version
VERSION = "1.0.0"


class InboxQuery:
    """Query and filter inbox coordination items."""

    def __init__(self, inbox_path: Path, verbose: bool = False):
        """
        Initialize inbox query.

        Args:
            inbox_path: Path to inbox directory
            verbose: Verbose output
        """
        self.inbox_path = inbox_path
        self.verbose = verbose

    def log(self, message: str):
        """Log if verbose."""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def get_incoming(
        self,
        item_type: str = "coordination",
        unacknowledged: bool = False,
        age_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get incoming items.

        Args:
            item_type: Type of items (coordination, tasks, proposals)
            unacknowledged: Filter to unacknowledged items only
            age_filter: Age filter (e.g., ">3d", "<1h")

        Returns:
            List of inbox items with metadata
        """
        incoming_dir = self.inbox_path / "incoming" / item_type
        if not incoming_dir.exists():
            self.log(f"Incoming directory does not exist: {incoming_dir}")
            return []

        items = []
        for item_file in incoming_dir.glob("*.json"):
            try:
                with open(item_file) as f:
                    data = json.load(f)

                # Add metadata
                stat = item_file.stat()
                item = {
                    "file": str(item_file.relative_to(self.inbox_path.parent)),
                    "id": item_file.stem,
                    "type": data.get("type", item_type),
                    "title": data.get("title", "Untitled"),
                    "priority": data.get("priority", "P2"),
                    "urgency": data.get("urgency", "next_sprint"),
                    "from_repo": data.get("from_repo", "unknown"),
                    "created": data.get("created", "unknown"),
                    "file_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "file_age_hours": (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 3600,
                    "data": data
                }

                # Filter by acknowledged status
                if unacknowledged:
                    # Check if item has been moved to active/ or acknowledged in events
                    acknowledged = self._is_acknowledged(item["id"])
                    if acknowledged:
                        continue

                # Filter by age
                if age_filter and not self._matches_age_filter(item["file_age_hours"], age_filter):
                    continue

                items.append(item)

            except Exception as e:
                self.log(f"Error reading {item_file}: {e}")

        return sorted(items, key=lambda x: x["file_modified"], reverse=True)

    def get_active(self) -> List[Dict[str, Any]]:
        """
        Get active coordination items.

        Returns:
            List of active items with metadata
        """
        active_dir = self.inbox_path / "active"
        if not active_dir.exists():
            return []

        items = []
        for item_file in active_dir.glob("*.json"):
            try:
                with open(item_file) as f:
                    data = json.load(f)

                stat = item_file.stat()
                item = {
                    "file": str(item_file.relative_to(self.inbox_path.parent)),
                    "id": item_file.stem,
                    "type": data.get("type", "unknown"),
                    "title": data.get("title", "Untitled"),
                    "priority": data.get("priority", "P2"),
                    "status": self._get_status_from_events(item_file.stem),
                    "file_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "data": data
                }

                items.append(item)

            except Exception as e:
                self.log(f"Error reading {item_file}: {e}")

        return sorted(items, key=lambda x: x["file_modified"], reverse=True)

    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific item by ID.

        Args:
            item_id: Item identifier (e.g., COORD-2025-006)

        Returns:
            Item data with metadata, or None if not found
        """
        # Search in incoming, active, completed
        search_dirs = [
            self.inbox_path / "incoming" / "coordination",
            self.inbox_path / "incoming" / "tasks",
            self.inbox_path / "incoming" / "proposals",
            self.inbox_path / "active",
            self.inbox_path / "completed"
        ]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            item_file = search_dir / f"{item_id}.json"
            if item_file.exists():
                try:
                    with open(item_file) as f:
                        data = json.load(f)

                    stat = item_file.stat()
                    location = "incoming" if "incoming" in str(item_file) else \
                              "active" if "active" in str(item_file) else "completed"

                    return {
                        "file": str(item_file.relative_to(self.inbox_path.parent)),
                        "id": item_id,
                        "location": location,
                        "type": data.get("type", "unknown"),
                        "title": data.get("title", "Untitled"),
                        "priority": data.get("priority", "unknown"),
                        "urgency": data.get("urgency", "unknown"),
                        "from_repo": data.get("from_repo", "unknown"),
                        "to_repo": data.get("to_repo", "unknown"),
                        "created": data.get("created", "unknown"),
                        "file_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "status": self._get_status_from_events(item_id),
                        "data": data
                    }

                except Exception as e:
                    self.log(f"Error reading {item_file}: {e}")
                    return None

        return None

    def count_by_status(self) -> Dict[str, int]:
        """
        Count items by status.

        Returns:
            Dictionary of status -> count
        """
        counts = {
            "incoming_coordination": 0,
            "incoming_tasks": 0,
            "incoming_proposals": 0,
            "active": 0,
            "completed": 0,
            "unacknowledged": 0
        }

        # Count incoming
        for item_type in ["coordination", "tasks", "proposals"]:
            incoming_dir = self.inbox_path / "incoming" / item_type
            if incoming_dir.exists():
                count = len(list(incoming_dir.glob("*.json")))
                counts[f"incoming_{item_type}"] = count

                # Count unacknowledged
                for item_file in incoming_dir.glob("*.json"):
                    if not self._is_acknowledged(item_file.stem):
                        counts["unacknowledged"] += 1

        # Count active
        active_dir = self.inbox_path / "active"
        if active_dir.exists():
            counts["active"] = len(list(active_dir.glob("*.json")))

        # Count completed
        completed_dir = self.inbox_path / "completed"
        if completed_dir.exists():
            counts["completed"] = len(list(completed_dir.glob("*.json")))

        return counts

    def _is_acknowledged(self, item_id: str) -> bool:
        """Check if item has been acknowledged."""
        # Check if exists in active/
        active_file = self.inbox_path / "active" / f"{item_id}.json"
        if active_file.exists():
            return True

        # Check events log for acknowledgment
        events_file = self.inbox_path / "coordination" / "events.jsonl"
        if events_file.exists():
            try:
                with open(events_file) as f:
                    for line in f:
                        event = json.loads(line)
                        if event.get("request_id") == item_id and \
                           event.get("event_type") in ["acknowledged", "accepted", "declined"]:
                            return True
            except Exception as e:
                self.log(f"Error reading events: {e}")

        return False

    def _get_status_from_events(self, item_id: str) -> str:
        """Get latest status from event log."""
        events_file = self.inbox_path / "coordination" / "events.jsonl"
        if not events_file.exists():
            return "unknown"

        latest_status = "unknown"
        try:
            with open(events_file) as f:
                for line in f:
                    event = json.loads(line)
                    if event.get("request_id") == item_id:
                        # Update status based on event type
                        event_type = event.get("event_type")
                        if event_type == "coordination_request_created":
                            latest_status = "created"
                        elif event_type == "acknowledged":
                            latest_status = "acknowledged"
                        elif event_type == "accepted":
                            latest_status = "accepted"
                        elif event_type == "declined":
                            latest_status = "declined"
                        elif event_type == "in_progress":
                            latest_status = "in_progress"
                        elif event_type == "completed":
                            latest_status = "completed"
                        elif event_type == "blocked":
                            latest_status = "blocked"

        except Exception as e:
            self.log(f"Error reading events: {e}")

        return latest_status

    def _matches_age_filter(self, age_hours: float, age_filter: str) -> bool:
        """
        Check if age matches filter.

        Args:
            age_hours: Age in hours
            age_filter: Filter string (e.g., ">3d", "<1h", "=2d")

        Returns:
            True if matches filter
        """
        # Parse filter: operator + value + unit
        match = re.match(r'([<>=]+)(\d+)([hdw])', age_filter)
        if not match:
            return True  # Invalid filter, no filtering

        operator, value, unit = match.groups()
        value = int(value)

        # Convert to hours
        multipliers = {'h': 1, 'd': 24, 'w': 168}
        threshold_hours = value * multipliers[unit]

        # Apply operator
        if operator == '>':
            return age_hours > threshold_hours
        elif operator == '<':
            return age_hours < threshold_hours
        elif operator == '>=':
            return age_hours >= threshold_hours
        elif operator == '<=':
            return age_hours <= threshold_hours
        elif operator == '=':
            return abs(age_hours - threshold_hours) < 1  # Within 1 hour
        else:
            return True


def format_output(items: List[Dict[str, Any]], output_format: str = "table") -> str:
    """
    Format items for output.

    Args:
        items: List of items to format
        output_format: Output format (table, json, summary)

    Returns:
        Formatted string
    """
    if output_format == "json":
        return json.dumps(items, indent=2)

    elif output_format == "summary":
        if not items:
            return "No items found."

        output = []
        for item in items:
            output.append(f"[{item['id']}] {item['title']}")
            output.append(f"  Priority: {item.get('priority', 'unknown')} | Urgency: {item.get('urgency', 'unknown')}")
            if 'status' in item:
                output.append(f"  Status: {item['status']}")
            output.append("")

        return "\n".join(output)

    else:  # table
        if not items:
            return "No items found."

        # Compact table format
        output = []
        header = f"{'ID':<20} {'Title':<50} {'Priority':<8} {'Status':<15}"
        output.append(header)
        output.append("-" * len(header))

        for item in items:
            row = f"{item['id']:<20} {item['title'][:48]:<50} {item.get('priority', 'P2'):<8} {item.get('status', 'incoming'):<15}"
            output.append(row)

        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Query inbox coordination items",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Query modes
    query_group = parser.add_mutually_exclusive_group()
    query_group.add_argument(
        '--incoming',
        action='store_true',
        help='Show incoming items'
    )
    query_group.add_argument(
        '--active',
        action='store_true',
        help='Show active items'
    )
    query_group.add_argument(
        '--request',
        help='Show specific request by ID (e.g., COORD-2025-006)'
    )
    query_group.add_argument(
        '--count-by-status',
        action='store_true',
        help='Count items by status'
    )

    # Filters
    parser.add_argument(
        '--type',
        choices=['coordination', 'tasks', 'proposals'],
        default='coordination',
        help='Item type (default: coordination)'
    )
    parser.add_argument(
        '--unacknowledged',
        action='store_true',
        help='Show only unacknowledged items'
    )
    parser.add_argument(
        '--age',
        help='Age filter (e.g., ">3d" for older than 3 days, "<1h" for less than 1 hour)'
    )
    parser.add_argument(
        '--status',
        help='Filter by status (created, acknowledged, in_progress, blocked, completed)'
    )

    # Output
    parser.add_argument(
        '--format',
        choices=['table', 'json', 'summary'],
        default='table',
        help='Output format (default: table)'
    )
    parser.add_argument(
        '--inbox-path',
        type=Path,
        default=Path.cwd() / "inbox",
        help='Path to inbox directory (default: ./inbox)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Initialize query
    query = InboxQuery(inbox_path=args.inbox_path, verbose=args.verbose)

    # Execute query
    try:
        if args.count_by_status:
            # Count by status
            counts = query.count_by_status()
            if args.format == "json":
                print(json.dumps(counts, indent=2))
            else:
                print("Inbox Status Counts:")
                print(f"  Incoming Coordination: {counts['incoming_coordination']}")
                print(f"  Incoming Tasks: {counts['incoming_tasks']}")
                print(f"  Incoming Proposals: {counts['incoming_proposals']}")
                print(f"  Active: {counts['active']}")
                print(f"  Completed: {counts['completed']}")
                print(f"  Unacknowledged: {counts['unacknowledged']}")

        elif args.request:
            # Get specific item
            item = query.get_item(args.request)
            if item:
                if args.format == "json":
                    print(json.dumps(item, indent=2))
                else:
                    print(f"Request: {item['id']}")
                    print(f"Title: {item['title']}")
                    print(f"Location: {item['location']}")
                    print(f"Status: {item['status']}")
                    print(f"Priority: {item['priority']} | Urgency: {item['urgency']}")
                    print(f"From: {item['from_repo']}")
                    print(f"To: {item['to_repo']}")
                    print(f"Created: {item['created']}")
                    print(f"File: {item['file']}")
                    print()
                    print("Full Data:")
                    print(json.dumps(item['data'], indent=2))
            else:
                print(f"Item not found: {args.request}", file=sys.stderr)
                sys.exit(1)

        elif args.active:
            # Get active items
            items = query.get_active()
            if args.status:
                items = [i for i in items if i.get('status') == args.status]
            print(format_output(items, args.format))

        else:  # incoming (default)
            # Get incoming items
            items = query.get_incoming(
                item_type=args.type,
                unacknowledged=args.unacknowledged,
                age_filter=args.age
            )
            if args.status:
                items = [i for i in items if query._get_status_from_events(i['id']) == args.status]
            print(format_output(items, args.format))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
