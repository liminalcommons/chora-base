#!/usr/bin/env python3
"""Lightweight usage tracking for automation scripts.

This module provides simple usage tracking for chora-base automation scripts
to demonstrate SAP-008 adoption and enable metrics analysis.

Usage:
    from usage_tracker import track_usage

    @track_usage
    def main():
        # Your script logic here
        pass

    if __name__ == "__main__":
        main()
"""

import json
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable


def get_usage_log_path() -> Path:
    """Get path to usage tracking log file.

    Returns:
        Path to .chora/memory/events/script-usage.jsonl
    """
    repo_root = Path(__file__).parent.parent
    log_dir = repo_root / ".chora" / "memory" / "events"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "script-usage.jsonl"


def track_usage(func: Callable) -> Callable:
    """Decorator to track script usage.

    Logs script invocation to .chora/memory/events/script-usage.jsonl
    with timestamp, script name, arguments, and outcome.

    Args:
        func: Function to track (typically main())

    Returns:
        Wrapped function with usage tracking

    Example:
        @track_usage
        def main():
            print("Hello, world!")

        if __name__ == "__main__":
            main()
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        script_name = Path(sys.argv[0]).name
        start_time = datetime.now()

        # Build event record
        event = {
            "event_id": f"script-{script_name}-{start_time.strftime('%Y%m%d-%H%M%S')}",
            "timestamp": start_time.isoformat(),
            "actor": "automation-script",
            "action": f"script_invocation_{script_name}",
            "metadata": {
                "script": script_name,
                "arguments": sys.argv[1:],
                "cwd": str(Path.cwd())
            }
        }

        try:
            # Run the actual function
            result = func(*args, **kwargs)

            # Record success
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            event["outcome"] = "success"
            event["duration_seconds"] = round(duration, 2)

            # Log the event
            log_path = get_usage_log_path()
            with log_path.open("a") as f:
                f.write(json.dumps(event) + "\n")

            return result

        except Exception as e:
            # Record failure
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            event["outcome"] = "failure"
            event["duration_seconds"] = round(duration, 2)
            event["metadata"]["error"] = str(e)
            event["metadata"]["error_type"] = type(e).__name__

            # Log the event
            log_path = get_usage_log_path()
            with log_path.open("a") as f:
                f.write(json.dumps(event) + "\n")

            # Re-raise the exception
            raise

    return wrapper


def get_usage_stats(script_name: str | None = None, days: int = 30) -> dict:
    """Get usage statistics for scripts.

    Args:
        script_name: Specific script to analyze (None for all scripts)
        days: Number of days to look back (default: 30)

    Returns:
        Dictionary with usage statistics
    """
    log_path = get_usage_log_path()

    if not log_path.exists():
        return {
            "total_invocations": 0,
            "success_count": 0,
            "failure_count": 0,
            "scripts": {}
        }

    # Read all events
    events = []
    with log_path.open("r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    # Filter by script name if specified
    if script_name:
        events = [e for e in events if e["metadata"]["script"] == script_name]

    # Filter by date range
    cutoff_date = datetime.now().timestamp() - (days * 86400)
    events = [
        e for e in events
        if datetime.fromisoformat(e["timestamp"]).timestamp() >= cutoff_date
    ]

    # Calculate statistics
    total = len(events)
    success = len([e for e in events if e["outcome"] == "success"])
    failure = len([e for e in events if e["outcome"] == "failure"])

    # Per-script breakdown
    scripts = {}
    for event in events:
        script = event["metadata"]["script"]
        if script not in scripts:
            scripts[script] = {
                "invocations": 0,
                "successes": 0,
                "failures": 0,
                "avg_duration": 0.0
            }

        scripts[script]["invocations"] += 1
        if event["outcome"] == "success":
            scripts[script]["successes"] += 1
        else:
            scripts[script]["failures"] += 1

    # Calculate average durations
    for script in scripts:
        script_events = [e for e in events if e["metadata"]["script"] == script]
        durations = [e["duration_seconds"] for e in script_events if "duration_seconds" in e]
        if durations:
            scripts[script]["avg_duration"] = round(sum(durations) / len(durations), 2)

    return {
        "total_invocations": total,
        "success_count": success,
        "failure_count": failure,
        "success_rate": round(success / total, 3) if total > 0 else 0.0,
        "scripts": scripts
    }


def generate_usage_report(days: int = 30) -> str:
    """Generate human-readable usage report.

    Args:
        days: Number of days to include in report

    Returns:
        Formatted usage report string
    """
    stats = get_usage_stats(days=days)

    if stats["total_invocations"] == 0:
        return f"No script usage recorded in the last {days} days."

    report = f"""
Script Usage Report (Last {days} Days)
{'=' * 60}

Overall Statistics:
- Total Invocations: {stats['total_invocations']}
- Successes: {stats['success_count']}
- Failures: {stats['failure_count']}
- Success Rate: {stats['success_rate']:.1%}

Per-Script Statistics:
"""

    # Sort scripts by invocation count
    sorted_scripts = sorted(
        stats["scripts"].items(),
        key=lambda x: x[1]["invocations"],
        reverse=True
    )

    for script_name, script_stats in sorted_scripts:
        success_rate = (
            script_stats["successes"] / script_stats["invocations"]
            if script_stats["invocations"] > 0
            else 0.0
        )

        report += f"""
  {script_name}:
    Invocations: {script_stats['invocations']}
    Success Rate: {success_rate:.1%}
    Avg Duration: {script_stats['avg_duration']}s
"""

    return report


if __name__ == "__main__":
    # Example usage report generation
    print(generate_usage_report(days=30))
