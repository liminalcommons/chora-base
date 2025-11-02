#!/usr/bin/env python3
"""
Respond to Coordination Request - Generate structured responses

Creates formatted responses to coordination requests with status updates,
effort estimates, and acceptance/decline decisions.

Usage:
    # Accept coordination request
    python scripts/respond-to-coordination.py \\
        --request COORD-2025-006 \\
        --status accepted \\
        --effort "8-12 hours" \\
        --notes "Starting implementation, ETA 3 days"

    # Decline coordination request
    python scripts/respond-to-coordination.py \\
        --request COORD-2025-006 \\
        --status declined \\
        --reason "Resource constraints, suggest deferring to Q2"

    # Acknowledge receipt (initial response)
    python scripts/respond-to-coordination.py \\
        --request COORD-2025-006 \\
        --status acknowledged \\
        --notes "Reviewing requirements, will respond within 2 days"
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

VERSION = "1.0.0"


def create_response(
    request_id: str,
    status: str,
    from_repo: str,
    effort: Optional[str] = None,
    timeline: Optional[str] = None,
    notes: Optional[str] = None,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create coordination response.

    Args:
        request_id: Request ID being responded to
        status: Response status (acknowledged, accepted, declined)
        from_repo: Repository generating response
        effort: Effort estimate (if accepted)
        timeline: Timeline/milestones (if accepted)
        notes: Additional notes
        reason: Decline reason (if declined)

    Returns:
        Response data dictionary
    """
    response = {
        "type": "coordination_response",
        "request_id": request_id,
        "responding_repo": from_repo,
        "status": status,
        "responded_at": datetime.now().isoformat(),
    }

    if status == "accepted":
        response["accepted"] = True
        if effort:
            response["estimated_effort"] = effort
        if timeline:
            response["timeline"] = timeline
        if notes:
            response["implementation_notes"] = notes

    elif status == "declined":
        response["accepted"] = False
        if reason:
            response["decline_reason"] = reason
        if notes:
            response["additional_notes"] = notes

    elif status == "acknowledged":
        if notes:
            response["acknowledgment_notes"] = notes

    return response


def emit_event(
    inbox_path: Path,
    request_id: str,
    event_type: str,
    status: str,
    notes: Optional[str] = None
):
    """
    Emit event to coordination log.

    Args:
        inbox_path: Path to inbox directory
        request_id: Request ID
        event_type: Event type
        status: Response status
        notes: Optional notes
    """
    events_file = inbox_path / "coordination" / "events.jsonl"
    events_file.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "request_id": request_id,
        "status": status,
    }

    if notes:
        event["notes"] = notes

    with open(events_file, 'a') as f:
        f.write(json.dumps(event) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Respond to coordination request",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--request',
        required=True,
        help='Request ID (e.g., COORD-2025-006)'
    )
    parser.add_argument(
        '--status',
        required=True,
        choices=['acknowledged', 'accepted', 'declined'],
        help='Response status'
    )
    parser.add_argument(
        '--from-repo',
        default='github.com/liminalcommons/chora-base',
        help='Responding repository (default: chora-base)'
    )
    parser.add_argument(
        '--effort',
        help='Effort estimate (e.g., "8-12 hours", "2-3 days")'
    )
    parser.add_argument(
        '--timeline',
        help='Timeline or milestones'
    )
    parser.add_argument(
        '--notes',
        help='Additional notes'
    )
    parser.add_argument(
        '--reason',
        help='Decline reason (if status=declined)'
    )
    parser.add_argument(
        '--inbox-path',
        type=Path,
        default=Path.cwd() / "inbox",
        help='Path to inbox directory (default: ./inbox)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file path (default: inbox/outgoing/<request_id>-response.json)'
    )
    parser.add_argument(
        '--emit-event',
        action='store_true',
        default=True,
        help='Emit event to coordination log (default: true)'
    )
    parser.add_argument(
        '--move-to-active',
        action='store_true',
        help='Move request to active/ (if accepted)'
    )

    args = parser.parse_args()

    try:
        # Create response
        response = create_response(
            request_id=args.request,
            status=args.status,
            from_repo=args.from_repo,
            effort=args.effort,
            timeline=args.timeline,
            notes=args.notes,
            reason=args.reason
        )

        # Determine output path
        if args.output:
            output_file = args.output
        else:
            outgoing_dir = args.inbox_path / "outgoing"
            outgoing_dir.mkdir(parents=True, exist_ok=True)
            output_file = outgoing_dir / f"{args.request}-response.json"

        # Write response
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=2)

        print(f"✓ Response created: {output_file}")

        # Emit event
        if args.emit_event:
            event_type = f"{args.status}"
            emit_event(
                args.inbox_path,
                args.request,
                event_type,
                args.status,
                args.notes
            )
            print(f"✓ Event emitted: {event_type}")

        # Move to active if accepted
        if args.move_to_active and args.status == "accepted":
            incoming_file = args.inbox_path / "incoming" / "coordination" / f"{args.request}.json"
            if incoming_file.exists():
                active_file = args.inbox_path / "active" / f"{args.request}.json"
                active_file.parent.mkdir(parents=True, exist_ok=True)
                incoming_file.rename(active_file)
                print(f"✓ Moved to active: {active_file}")

        print()
        print("Response Summary:")
        print(json.dumps(response, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
