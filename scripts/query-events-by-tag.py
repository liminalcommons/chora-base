#!/usr/bin/env python3
"""
Query Events by Tag

Query A-MEM event logs using the event tag taxonomy for filtering,
counting, and analyzing events across traces, domains, and time periods.

Part of Phase 3: Machine-Readable Exports (Curatorial Enhancements)
SAP Integration: SAP-010 (memory-system)

Usage:
    python scripts/query-events-by-tag.py --tags sap-evaluation           # Find all SAP evaluation events
    python scripts/query-events-by-tag.py --tags script-failure --days 7  # Recent script failures
    python scripts/query-events-by-tag.py --count-by-tag                  # Count events by tag
    python scripts/query-events-by-tag.py --list-tags                     # List all tags in use
    python scripts/query-events-by-tag.py --validate-tags                 # Validate tags against taxonomy
"""

import json
import yaml
import os
import re
import glob
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from datetime import datetime, timezone, timedelta
from collections import Counter



# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def load_taxonomy(taxonomy_path: str = "schemas/event-tag-taxonomy.yaml") -> Dict[str, Any]:
    """Load event tag taxonomy from YAML file."""
    try:
        with open(taxonomy_path, 'r', encoding='utf-8') as f:
            taxonomy = yaml.safe_load(f)
        return taxonomy
    except Exception as e:
        print(f"Warning: Could not load taxonomy from {taxonomy_path}: {e}")
        return {}


def extract_all_tags_from_taxonomy(taxonomy: Dict[str, Any]) -> Set[str]:
    """Extract all valid tag names from the taxonomy."""
    valid_tags = set()

    # Extract from taxonomy domains
    for domain_name, domain_data in taxonomy.get('taxonomy', {}).items():
        for category_name, category_data in domain_data.get('categories', {}).items():
            for tag_obj in category_data.get('tags', []):
                if isinstance(tag_obj, dict):
                    valid_tags.add(tag_obj.get('name'))
                elif isinstance(tag_obj, str):
                    valid_tags.add(tag_obj)

    # Extract from cross-cutting tags
    for category_name, category_data in taxonomy.get('cross_cutting', {}).items():
        for tag_obj in category_data.get('tags', []):
            if isinstance(tag_obj, dict):
                valid_tags.add(tag_obj.get('name'))
            elif isinstance(tag_obj, str):
                valid_tags.add(tag_obj)

    return valid_tags


def find_event_files(
    events_dir: str = ".chora/memory/events",
    days: Optional[int] = None
) -> List[str]:
    """
    Find all event JSONL files.

    Args:
        events_dir: Root events directory
        days: If specified, only include files modified in last N days

    Returns:
        List of event file paths
    """
    event_files = []

    for root, dirs, files in os.walk(events_dir):
        for file in files:
            if file.endswith('.jsonl'):
                file_path = os.path.join(root, file)

                # Filter by modification time if days specified
                if days is not None:
                    mtime = os.path.getmtime(file_path)
                    file_age = (datetime.now().timestamp() - mtime) / 86400  # days
                    if file_age > days:
                        continue

                event_files.append(file_path)

    return sorted(event_files)


def read_events_from_file(file_path: str) -> List[Dict[str, Any]]:
    """Read all events from a JSONL file."""
    events = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except json.JSONDecodeError as e:
                    print(f"Warning: Could not parse line {line_num} in {file_path}: {e}")
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")

    return events


def filter_events_by_tags(
    events: List[Dict[str, Any]],
    required_tags: List[str],
    any_match: bool = False
) -> List[Dict[str, Any]]:
    """
    Filter events by tags.

    Args:
        events: List of event dicts
        required_tags: Tags to filter by
        any_match: If True, match any tag (OR). If False, match all tags (AND)

    Returns:
        Filtered list of events
    """
    filtered = []

    for event in events:
        event_tags = event.get('metadata', {}).get('tags', [])

        if not event_tags:
            continue

        if any_match:
            # Match if ANY required tag is present
            if any(tag in event_tags for tag in required_tags):
                filtered.append(event)
        else:
            # Match if ALL required tags are present
            if all(tag in event_tags for tag in required_tags):
                filtered.append(event)

    return filtered


def filter_events_by_status(
    events: List[Dict[str, Any]],
    status: str
) -> List[Dict[str, Any]]:
    """Filter events by status (success, failure, pending, timeout)."""
    return [e for e in events if e.get('status') == status]


def count_events_by_tag(events: List[Dict[str, Any]]) -> Counter:
    """Count events by tag."""
    tag_counts = Counter()

    for event in events:
        event_tags = event.get('metadata', {}).get('tags', [])
        for tag in event_tags:
            tag_counts[tag] += 1

    return tag_counts


def list_all_tags_in_use(events: List[Dict[str, Any]]) -> Set[str]:
    """Extract all unique tags currently in use."""
    tags_in_use = set()

    for event in events:
        event_tags = event.get('metadata', {}).get('tags', [])
        tags_in_use.update(event_tags)

    return tags_in_use


def validate_tags_against_taxonomy(
    events: List[Dict[str, Any]],
    taxonomy: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate that all tags in events are defined in taxonomy.

    Returns:
        Dict with validation results:
        {
            "valid_tags": [...],
            "invalid_tags": [...],
            "events_with_invalid_tags": [...]
        }
    """
    valid_tags = extract_all_tags_from_taxonomy(taxonomy)
    tags_in_use = list_all_tags_in_use(events)

    invalid_tags = tags_in_use - valid_tags
    events_with_invalid = []

    for event in events:
        event_tags = set(event.get('metadata', {}).get('tags', []))
        if event_tags & invalid_tags:  # Intersection
            events_with_invalid.append({
                'event_id': event.get('event_id'),
                'timestamp': event.get('timestamp'),
                'invalid_tags': list(event_tags & invalid_tags)
            })

    return {
        'valid_tags': sorted(list(valid_tags)),
        'invalid_tags': sorted(list(invalid_tags)),
        'events_with_invalid_tags': events_with_invalid
    }


def format_event_summary(event: Dict[str, Any]) -> str:
    """Format a single event for display."""
    timestamp = event.get('timestamp', 'unknown')
    event_id = event.get('event_id', 'unknown')
    action = event.get('action', event.get('event_type', 'unknown'))
    status = event.get('status', event.get('outcome', 'unknown'))
    tags = event.get('metadata', {}).get('tags', [])

    return f"{timestamp} | {event_id} | {action} | {status} | tags={tags}"


def query_events(
    tags: List[str] = None,
    status: str = None,
    days: int = None,
    any_match: bool = False,
    events_dir: str = ".chora/memory/events"
) -> List[Dict[str, Any]]:
    """
    Query events with filters.

    Args:
        tags: Filter by tags (AND by default, OR if any_match=True)
        status: Filter by status
        days: Only include events from last N days
        any_match: If True, match any tag (OR). If False, match all tags (AND)
        events_dir: Events directory path

    Returns:
        List of matching events
    """
    # Find event files
    event_files = find_event_files(events_dir=events_dir, days=days)

    # Read all events
    all_events = []
    for file_path in event_files:
        events = read_events_from_file(file_path)
        all_events.extend(events)

    # Apply filters
    filtered_events = all_events

    if tags:
        filtered_events = filter_events_by_tags(filtered_events, tags, any_match=any_match)

    if status:
        filtered_events = filter_events_by_status(filtered_events, status)

    return filtered_events


def main():
    parser = argparse.ArgumentParser(description="Query A-MEM events by tag")
    parser.add_argument(
        "--tags",
        nargs="+",
        help="Filter by tags (AND by default, OR with --any-match)"
    )
    parser.add_argument(
        "--status",
        choices=["success", "failure", "pending", "timeout"],
        help="Filter by event status"
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Only include events from last N days"
    )
    parser.add_argument(
        "--any-match",
        action="store_true",
        help="Match any tag (OR) instead of all tags (AND)"
    )
    parser.add_argument(
        "--count-by-tag",
        action="store_true",
        help="Count events by tag"
    )
    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="List all tags currently in use"
    )
    parser.add_argument(
        "--validate-tags",
        action="store_true",
        help="Validate tags against taxonomy"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory (default: .chora/memory/events)"
    )
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()

    # Load taxonomy
    taxonomy = load_taxonomy()

    # List tags command
    if args.list_tags:
        event_files = find_event_files(events_dir=args.events_dir)
        all_events = []
        for file_path in event_files:
            all_events.extend(read_events_from_file(file_path))

        tags_in_use = sorted(list_all_tags_in_use(all_events))

        print(f"📋 Tags in Use ({len(tags_in_use)} unique tags):\n")
        for tag in tags_in_use:
            print(f"  - {tag}")

        return

    # Count by tag command
    if args.count_by_tag:
        event_files = find_event_files(events_dir=args.events_dir, days=args.days)
        all_events = []
        for file_path in event_files:
            all_events.extend(read_events_from_file(file_path))

        tag_counts = count_events_by_tag(all_events)

        print(f"📊 Event Counts by Tag:\n")
        for tag, count in tag_counts.most_common():
            print(f"  {tag}: {count}")

        return

    # Validate tags command
    if args.validate_tags:
        event_files = find_event_files(events_dir=args.events_dir)
        all_events = []
        for file_path in event_files:
            all_events.extend(read_events_from_file(file_path))

        validation = validate_tags_against_taxonomy(all_events, taxonomy)

        print(f"✅ Valid Tags ({len(validation['valid_tags'])}):")
        for tag in validation['valid_tags'][:10]:
            print(f"  - {tag}")
        if len(validation['valid_tags']) > 10:
            print(f"  ... and {len(validation['valid_tags']) - 10} more")

        print(f"\n❌ Invalid Tags ({len(validation['invalid_tags'])}):")
        for tag in validation['invalid_tags']:
            print(f"  - {tag}")

        if validation['events_with_invalid_tags']:
            print(f"\n⚠️  Events with Invalid Tags ({len(validation['events_with_invalid_tags'])}):")
            for event_info in validation['events_with_invalid_tags'][:5]:
                print(f"  {event_info['event_id']}: {event_info['invalid_tags']}")
            if len(validation['events_with_invalid_tags']) > 5:
                print(f"  ... and {len(validation['events_with_invalid_tags']) - 5} more")

        return

    # Query events
    events = query_events(
        tags=args.tags,
        status=args.status,
        days=args.days,
        any_match=args.any_match,
        events_dir=args.events_dir
    )

    # Output results
    if args.output == "json":
        print(json.dumps(events, indent=2))
    else:
        # Text output
        filter_desc = []
        if args.tags:
            match_type = "any" if args.any_match else "all"
            filter_desc.append(f"tags={match_type} of {args.tags}")
        if args.status:
            filter_desc.append(f"status={args.status}")
        if args.days:
            filter_desc.append(f"last {args.days} days")

        filter_str = ", ".join(filter_desc) if filter_desc else "none"

        print(f"🔍 Query Results (filters: {filter_str}):\n")
        print(f"   Found {len(events)} events\n")

        if len(events) > 0:
            print("Events:")
            for event in events[:20]:  # Show first 20
                print(f"  {format_event_summary(event)}")

            if len(events) > 20:
                print(f"\n  ... and {len(events) - 20} more events")


if __name__ == "__main__":
    main()
