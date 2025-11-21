#!/usr/bin/env python3
"""
Work Context Coordination Metrics Collection

Collects production usage metrics for chora.coordination.work_context SAP.
Part of L3 Phase 6 (Production Metrics).

Usage:
    work-context-metrics.py [--since YYYY-MM-DD] [--format json|markdown]

Output:
    - Contexts registered (manual + auto)
    - Conflicts detected
    - Risk assessments performed
    - Dashboard views
    - ROI validation (projected vs actual)
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Collect work context coordination metrics"
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Start date (YYYY-MM-DD), defaults to 30 days ago",
        default=None
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format"
    )
    parser.add_argument(
        "--events-dir",
        type=Path,
        default=Path(".chora/memory/events"),
        help="Events directory path"
    )
    return parser.parse_args()


def load_events(events_dir: Path, since_date: datetime = None):
    """Load all A-MEM events, optionally filtered by date."""
    events = []

    # Find all JSONL files (YYYY-MM.jsonl)
    event_files = sorted(events_dir.glob("????-??.jsonl"))

    for event_file in event_files:
        try:
            with open(event_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        event = json.loads(line)
                        # Parse timestamp as naive datetime for comparison
                        timestamp_str = event['timestamp'].replace('Z', '')
                        event_time = datetime.fromisoformat(timestamp_str)

                        # Filter by date if specified
                        if since_date and event_time < since_date:
                            continue

                        events.append(event)
                    except json.JSONDecodeError:
                        # Skip malformed events
                        continue
        except Exception as e:
            print(f"Warning: Could not read {event_file}: {e}", file=sys.stderr)

    return events


def calculate_metrics(events):
    """Calculate work context coordination metrics."""
    metrics = {
        "total_events": len(events),
        "contexts_registered_manual": 0,
        "contexts_registered_auto": 0,
        "contexts_updated": 0,
        "contexts_cleaned": 0,
        "conflicts_detected": 0,
        "risk_assessments": 0,
        "dashboard_views": 0,
        "unique_contexts": set(),
        "event_breakdown": defaultdict(int),
        "time_period": {
            "start": None,
            "end": None,
            "days": 0
        }
    }

    # Track time range
    timestamps = []

    for event in events:
        event_type = event.get("event_type", "")
        metrics["event_breakdown"][event_type] += 1

        # Track timestamps
        try:
            timestamp_str = event['timestamp'].replace('Z', '')
            event_time = datetime.fromisoformat(timestamp_str)
            timestamps.append(event_time)
        except:
            pass

        # Count specific work context events
        if event_type == "work_context_registered":
            context = event.get("context", {})
            reg_type = context.get("registration_type", "unknown")

            if reg_type == "manual":
                metrics["contexts_registered_manual"] += 1
            elif reg_type == "auto":
                metrics["contexts_registered_auto"] += 1

            # Track unique contexts
            ctx_id = context.get("context_id")
            if ctx_id:
                metrics["unique_contexts"].add(ctx_id)

        elif event_type == "work_context_auto_registered":
            metrics["contexts_registered_auto"] += 1
            context = event.get("context", {})
            ctx_id = context.get("context_id")
            if ctx_id:
                metrics["unique_contexts"].add(ctx_id)

        elif event_type == "work_context_updated":
            metrics["contexts_updated"] += 1

        elif event_type == "work_contexts_cleaned":
            context = event.get("context", {})
            metrics["contexts_cleaned"] += context.get("cleaned_count", 0)

        # Note: Dashboard views and risk assessments aren't explicitly logged yet
        # These would need to be added to the SAP in future iterations

    # Calculate time period
    if timestamps:
        timestamps.sort()
        metrics["time_period"]["start"] = timestamps[0].isoformat()
        metrics["time_period"]["end"] = timestamps[-1].isoformat()
        duration = timestamps[-1] - timestamps[0]
        metrics["time_period"]["days"] = max(1, duration.days)

    # Convert set to count
    metrics["unique_contexts"] = len(metrics["unique_contexts"])

    return metrics


def calculate_roi(metrics):
    """Calculate ROI based on projected savings."""
    # Projected savings (from L1 pilot validation):
    # - 26 hours/year saved
    # - $3900 savings
    # - Investment: 5 hours ($750)
    # - ROI: 420%

    projected = {
        "investment_hours": 6,  # L2 investment (L1 pilot 5h + L2 docs 1h)
        "investment_usd": 900,
        "savings_per_year_hours": 26,
        "savings_per_year_usd": 3900,
        "roi_percent": 333,  # (3900 - 900) / 900 * 100
        "payback_weeks": 7
    }

    # Actual savings estimation:
    # - Each auto-registration saves ~5 min vs manual (infers patterns)
    # - Each conflict detection saves ~15 min of merge conflict resolution
    # - Dashboard view saves ~2 min vs checking files manually

    days = metrics["time_period"]["days"]
    if days == 0:
        days = 1

    # Estimate actual savings
    auto_reg_savings_hours = metrics["contexts_registered_auto"] * (5 / 60)  # 5 min each
    conflict_savings_hours = metrics["conflicts_detected"] * (15 / 60)  # 15 min each
    dashboard_savings_hours = metrics["dashboard_views"] * (2 / 60)  # 2 min each

    total_savings_hours = auto_reg_savings_hours + conflict_savings_hours + dashboard_savings_hours
    total_savings_usd = total_savings_hours * 150  # $150/hour rate

    # Extrapolate to yearly
    if days >= 7:
        yearly_multiplier = 365 / days
        yearly_savings_hours = total_savings_hours * yearly_multiplier
        yearly_savings_usd = total_savings_usd * yearly_multiplier
    else:
        # Too early to extrapolate
        yearly_savings_hours = None
        yearly_savings_usd = None

    actual = {
        "days_tracked": days,
        "savings_hours_period": round(total_savings_hours, 2),
        "savings_usd_period": round(total_savings_usd, 2),
        "savings_per_year_hours": round(yearly_savings_hours, 1) if yearly_savings_hours else "insufficient_data",
        "savings_per_year_usd": round(yearly_savings_usd, 0) if yearly_savings_usd else "insufficient_data",
        "breakdown": {
            "auto_registration": {
                "count": metrics["contexts_registered_auto"],
                "hours_saved": round(auto_reg_savings_hours, 2),
                "usd_saved": round(auto_reg_savings_hours * 150, 2)
            },
            "conflict_detection": {
                "count": metrics["conflicts_detected"],
                "hours_saved": round(conflict_savings_hours, 2),
                "usd_saved": round(conflict_savings_hours * 150, 2)
            },
            "dashboard_views": {
                "count": metrics["dashboard_views"],
                "hours_saved": round(dashboard_savings_hours, 2),
                "usd_saved": round(dashboard_savings_hours * 150, 2)
            }
        }
    }

    # Calculate ROI if we have yearly projections
    if yearly_savings_usd:
        net_savings = yearly_savings_usd - projected["investment_usd"]
        actual_roi_percent = (net_savings / projected["investment_usd"]) * 100
        actual["roi_percent"] = round(actual_roi_percent, 0)

        # Compare to projected
        actual["vs_projected"] = {
            "savings_ratio": round(yearly_savings_usd / projected["savings_per_year_usd"], 2),
            "roi_ratio": round(actual_roi_percent / projected["roi_percent"], 2),
            "status": "on_track" if actual_roi_percent >= projected["roi_percent"] * 0.8 else "below_projection"
        }
    else:
        actual["roi_percent"] = "insufficient_data"
        actual["vs_projected"] = "insufficient_data"

    return {
        "projected": projected,
        "actual": actual
    }


def format_markdown(metrics, roi):
    """Format metrics as markdown report."""
    output = []
    output.append("# Work Context Coordination Metrics")
    output.append("")
    output.append(f"**Period**: {metrics['time_period']['start']} to {metrics['time_period']['end']} ({metrics['time_period']['days']} days)")
    output.append("")

    output.append("## Usage Statistics")
    output.append("")
    output.append(f"- **Total Events**: {metrics['total_events']}")
    output.append(f"- **Unique Contexts**: {metrics['unique_contexts']}")
    output.append(f"- **Contexts Registered** (Manual): {metrics['contexts_registered_manual']}")
    output.append(f"- **Contexts Registered** (Auto): {metrics['contexts_registered_auto']}")
    output.append(f"- **Contexts Updated**: {metrics['contexts_updated']}")
    output.append(f"- **Contexts Cleaned**: {metrics['contexts_cleaned']}")
    output.append(f"- **Conflicts Detected**: {metrics['conflicts_detected']} *(not yet implemented)*")
    output.append(f"- **Dashboard Views**: {metrics['dashboard_views']} *(not yet instrumented)*")
    output.append("")

    output.append("## Event Breakdown")
    output.append("")
    for event_type, count in sorted(metrics['event_breakdown'].items()):
        output.append(f"- `{event_type}`: {count}")
    output.append("")

    output.append("## ROI Analysis")
    output.append("")
    output.append("### Projected (from L2 Adoption)")
    proj = roi["projected"]
    output.append(f"- Investment: {proj['investment_hours']}h (${proj['investment_usd']})")
    output.append(f"- Yearly Savings: {proj['savings_per_year_hours']}h (${proj['savings_per_year_usd']})")
    output.append(f"- ROI: {proj['roi_percent']}%")
    output.append(f"- Payback: {proj['payback_weeks']} weeks")
    output.append("")

    output.append("### Actual (Period Measured)")
    actual = roi["actual"]
    output.append(f"- Days Tracked: {actual['days_tracked']}")
    output.append(f"- Savings (Period): {actual['savings_hours_period']}h (${actual['savings_usd_period']})")

    if actual["savings_per_year_hours"] != "insufficient_data":
        output.append(f"- Projected Yearly: {actual['savings_per_year_hours']}h (${actual['savings_per_year_usd']})")
        output.append(f"- ROI: {actual['roi_percent']}%")
        output.append("")

        if actual["vs_projected"] != "insufficient_data":
            vs_proj = actual["vs_projected"]
            output.append(f"**Status**: {vs_proj['status'].replace('_', ' ').title()}")
            output.append(f"- Savings vs Projected: {vs_proj['savings_ratio']}x")
            output.append(f"- ROI vs Projected: {vs_proj['roi_ratio']}x")
    else:
        output.append(f"- Projected Yearly: *Insufficient data (need ≥7 days)*")

    output.append("")
    output.append("### Savings Breakdown")
    breakdown = actual["breakdown"]
    for category, data in breakdown.items():
        output.append(f"- **{category.replace('_', ' ').title()}**: {data['count']} × → {data['hours_saved']}h (${data['usd_saved']})")

    output.append("")
    output.append("---")
    output.append("*Generated by `scripts/work-context-metrics.py`*")

    return "\n".join(output)


def format_json(metrics, roi):
    """Format metrics as JSON."""
    return json.dumps({
        "metrics": metrics,
        "roi": roi,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }, indent=2, default=str)


def main():
    args = parse_args()

    # Calculate since_date (timezone-aware)
    if args.since:
        since_date = datetime.fromisoformat(args.since).replace(tzinfo=None)
    else:
        # Default: last 30 days
        since_date = datetime.now() - timedelta(days=30)

    # Load events
    events = load_events(args.events_dir, since_date)

    if not events:
        print("No work context events found in the specified period.", file=sys.stderr)
        sys.exit(1)

    # Calculate metrics
    metrics = calculate_metrics(events)
    roi = calculate_roi(metrics)

    # Output
    if args.format == "json":
        print(format_json(metrics, roi))
    else:
        print(format_markdown(metrics, roi))


if __name__ == "__main__":
    main()
