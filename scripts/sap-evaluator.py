#!/usr/bin/env python3
"""
SAP Self-Evaluation CLI Tool

Evaluate SAP adoption depth and generate improvement roadmaps.

Usage:
    # Quick check (30 seconds)
    python scripts/sap-evaluator.py --quick
    python scripts/sap-evaluator.py --quick SAP-004

    # Deep dive (5 minutes)
    python scripts/sap-evaluator.py --deep SAP-004
    python scripts/sap-evaluator.py --deep SAP-004 --output report.md

    # Strategic analysis (30 minutes)
    python scripts/sap-evaluator.py --strategic
    python scripts/sap-evaluator.py --strategic --output roadmap.yaml

    # Export evaluation history
    python scripts/sap-evaluator.py --export-history
    python scripts/sap-evaluator.py --export-history --sap SAP-004
    python scripts/sap-evaluator.py --export-history --format json --output history.json

Examples:
    # Check all installed SAPs
    python scripts/sap-evaluator.py --quick

    # Detailed assessment of testing framework
    python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md

    # Generate quarterly roadmap
    python scripts/sap-evaluator.py --strategic --output project-docs/sap-roadmap.yaml

    # View evaluation history for trend analysis
    python scripts/sap-evaluator.py --export-history --days 30
"""

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add repo root to path for imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from utils.sap_evaluation import (
    SAPEvaluator,
    EvaluationResult,
    AdoptionRoadmap,
    format_quick_results
)
from usage_tracker import track_usage


def print_quick_results_terminal(results: list[EvaluationResult] | EvaluationResult):
    """Print quick check results to terminal"""
    print(format_quick_results(results))


def print_deep_results_terminal(result: EvaluationResult):
    """Print deep dive results to terminal"""
    print(f"\n{result.sap_id} ({result.sap_name}) - Deep Dive Assessment")
    print("=" * 60)
    print(f"Generated: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Evaluation Time: {result.duration_seconds:.1f} seconds")
    print("")

    print("## Current State")
    print(f"- Adoption Level: {result.current_level}")
    print(f"- Completion: {result.completion_percent:.0f}% toward next level")
    print(f"- Next Milestone: {result.next_milestone}")
    print("")

    if result.validation_results:
        print("## Validation Results")
        for check, passed in result.validation_results.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check}")
        print("")

    if result.gaps:
        print(f"## Gaps Identified ({len(result.gaps)})")
        for i, gap in enumerate(result.gaps, 1):
            print(f"\n### Gap {i}: {gap.title} ({gap.priority})")
            print(f"**Impact**: {gap.impact} | **Effort**: {gap.effort}")
            print(f"**Description**: {gap.description}")
            if gap.estimated_hours > 0:
                print(f"**Estimated Effort**: {gap.estimated_hours} hours")
        print("")

    if result.blockers:
        print("## Blockers")
        for blocker in result.blockers:
            print(f"- {blocker}")
        print("")

    if result.warnings:
        print("## Warnings")
        for warning in result.warnings:
            print(f"⚠️  {warning}")
        print("")

    print(f"Run deep dive with --output to save detailed report")


def print_strategic_results_terminal(roadmap: AdoptionRoadmap):
    """Print strategic analysis results to terminal"""
    print(f"\nSAP Adoption Roadmap")
    print("=" * 60)
    print(f"Generated: {roadmap.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target Quarter: {roadmap.target_quarter}")
    print("")

    print("## Current State")
    print(f"- Total SAPs Installed: {roadmap.total_saps_installed}")
    print(f"- Average Level: {roadmap.average_adoption_level:.2f}")
    print("")

    print("## Distribution by Level")
    for level, count in roadmap.adoption_distribution.items():
        print(f"- {level}: {count} SAPs")
    print("")

    if roadmap.priority_gaps:
        print(f"## Priority Gaps ({len(roadmap.priority_gaps)})")
        for gap in roadmap.priority_gaps[:5]:  # Top 5
            print(f"{gap.rank}. {gap.sap_id}: {gap.gap.title} (P{gap.gap.priority})")
        print("")

    print("Run strategic analysis with --output to save full roadmap")


def save_markdown_report(result: EvaluationResult, output_path: Path):
    """Save deep dive result as markdown report"""
    md = []
    md.append(f"# {result.sap_id} ({result.sap_name}) - Deep Dive Assessment")
    md.append(f"**Generated**: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    md.append(f"**Evaluation Time**: {result.duration_seconds:.1f} seconds")
    md.append("")

    md.append("## Current State")
    md.append(f"- **Adoption Level**: {result.current_level}")
    md.append(f"- **Completion**: {result.completion_percent:.0f}% toward next level")
    md.append(f"- **Next Milestone**: {result.next_milestone}")
    md.append("")

    if result.validation_results:
        md.append("## Validation Results")
        for check, passed in result.validation_results.items():
            status = "✅" if passed else "❌"
            md.append(f"{status} **{check}**")
        md.append("")

    if result.gaps:
        md.append(f"## Gap Analysis ({len(result.gaps)} gaps identified)")
        md.append("")
        for i, gap in enumerate(result.gaps, 1):
            md.append(f"### Gap {i}: {gap.title} ({gap.priority})")
            md.append(f"**Impact**: {gap.impact} | **Effort**: {gap.effort} | **Urgency**: {gap.urgency}")
            md.append("")
            md.append(f"**Current State**: {gap.current_state}")
            md.append(f"**Desired State**: {gap.desired_state}")
            md.append("")
            if gap.description:
                md.append(f"{gap.description}")
                md.append("")
            if gap.estimated_hours > 0:
                md.append(f"**Estimated Effort**: {gap.estimated_hours} hours")
                md.append("")
            if gap.blocks:
                md.append(f"**Blocks**: {', '.join(gap.blocks)}")
                md.append("")

    if result.blockers:
        md.append("## Blockers")
        for blocker in result.blockers:
            md.append(f"- {blocker}")
        md.append("")

    if result.warnings:
        md.append("## Warnings")
        for warning in result.warnings:
            md.append(f"⚠️ {warning}")
        md.append("")

    md.append("---")
    md.append(f"*Generated by SAP-019 Self-Evaluation*")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write("\n".join(md))

    print(f"✅ Report saved to: {output_path}")


def save_json_output(data: dict, output_path: Path):
    """Save evaluation result as JSON"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"✅ JSON saved to: {output_path}")


def save_yaml_roadmap(roadmap: AdoptionRoadmap, output_path: Path):
    """Save strategic roadmap as YAML"""
    # Simple YAML generation without external dependencies
    yaml_lines = []
    yaml_lines.append(f"# SAP Adoption Roadmap")
    yaml_lines.append(f"# Generated: {roadmap.generated_at.isoformat()}")
    yaml_lines.append(f"# Next Review: {roadmap.next_review_date or 'TBD'}")
    yaml_lines.append("")

    yaml_lines.append("metadata:")
    yaml_lines.append(f"  generated_at: {roadmap.generated_at.isoformat()}")
    yaml_lines.append(f"  target_quarter: {roadmap.target_quarter}")
    yaml_lines.append("")

    yaml_lines.append("current_state:")
    yaml_lines.append(f"  total_saps_installed: {roadmap.total_saps_installed}")
    yaml_lines.append(f"  average_adoption_level: {roadmap.average_adoption_level:.2f}")
    yaml_lines.append("")

    yaml_lines.append("  distribution:")
    for level, count in roadmap.adoption_distribution.items():
        yaml_lines.append(f"    {level}: {count}")
    yaml_lines.append("")

    if roadmap.priority_gaps:
        yaml_lines.append("priority_gaps:")
        for gap in roadmap.priority_gaps[:10]:  # Top 10
            yaml_lines.append(f"  - rank: {gap.rank}")
            yaml_lines.append(f"    sap_id: {gap.sap_id}")
            yaml_lines.append(f"    gap_title: \"{gap.gap.title}\"")
            yaml_lines.append(f"    impact: {gap.gap.impact}")
            yaml_lines.append(f"    effort: {gap.gap.effort}")
            yaml_lines.append(f"    priority_score: {gap.priority_score:.2f}")
            yaml_lines.append(f"    sprint: {gap.sprint}")
            yaml_lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write("\n".join(yaml_lines))

    print(f"✅ Roadmap saved to: {output_path}")


def save_evaluation_to_history(result: EvaluationResult | AdoptionRoadmap, evaluation_type: str):
    """
    Save evaluation result to history file for trend analysis.

    History file: .chora/memory/events/sap-evaluations.jsonl
    """
    history_dir = repo_root / ".chora" / "memory" / "events"
    history_file = history_dir / "sap-evaluations.jsonl"

    # Create directory if it doesn't exist
    history_dir.mkdir(parents=True, exist_ok=True)

    # Prepare history entry
    if isinstance(result, EvaluationResult):
        history_entry = {
            "timestamp": result.timestamp.isoformat(),
            "evaluation_type": evaluation_type,
            "sap_id": result.sap_id,
            "sap_name": result.sap_name,
            "current_level": result.current_level,
            "completion_percent": result.completion_percent,
            "is_installed": result.is_installed,
            "gap_count": len(result.gaps),
            "blocker_count": len(result.blockers),
            "estimated_effort_hours": result.estimated_effort_hours,
            "duration_seconds": result.duration_seconds,
            "confidence": result.confidence
        }
    else:  # AdoptionRoadmap
        history_entry = {
            "timestamp": result.generated_at.isoformat(),
            "evaluation_type": "strategic",
            "total_saps_installed": result.total_saps_installed,
            "average_adoption_level": result.average_adoption_level,
            "adoption_distribution": result.adoption_distribution,
            "priority_gap_count": len(result.priority_gaps) if result.priority_gaps else 0,
            "target_quarter": result.target_quarter
        }

    # Append to history file (JSONL format)
    with open(history_file, "a") as f:
        f.write(json.dumps(history_entry, default=str) + "\n")


def load_evaluation_history(
    history_file: Path = None,
    sap_id: str = None,
    days: int = None,
    evaluation_type: str = None
) -> list[dict]:
    """
    Load evaluation history from JSONL file with optional filters.

    Args:
        history_file: Path to history file (default: .chora/memory/events/sap-evaluations.jsonl)
        sap_id: Filter by SAP ID
        days: Only include evaluations from last N days
        evaluation_type: Filter by evaluation type (quick, deep, strategic)

    Returns:
        List of evaluation history entries
    """
    if history_file is None:
        history_file = repo_root / ".chora" / "memory" / "events" / "sap-evaluations.jsonl"

    if not history_file.exists():
        return []

    history = []
    cutoff_date = None
    if days:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    with open(history_file, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())

                # Apply filters
                if sap_id and entry.get("sap_id") != sap_id:
                    continue

                if evaluation_type and entry.get("evaluation_type") != evaluation_type:
                    continue

                if days:
                    entry_date = datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
                    if entry_date < cutoff_date:
                        continue

                history.append(entry)
            except json.JSONDecodeError:
                continue

    return history


def analyze_evaluation_trends(history: list[dict]) -> dict:
    """
    Analyze evaluation history to identify trends.

    Returns:
        Dict with trend analysis:
        - level_changes: SAPs that changed levels
        - gap_trends: Gap count trends
        - effort_trends: Effort estimate trends
    """
    # Group by SAP ID
    sap_history = defaultdict(list)
    for entry in history:
        if "sap_id" in entry:
            sap_history[entry["sap_id"]].append(entry)

    # Sort each SAP's history by timestamp
    for sap_id in sap_history:
        sap_history[sap_id].sort(key=lambda x: x["timestamp"])

    # Analyze trends
    level_changes = []
    gap_trends = []
    effort_trends = []

    for sap_id, entries in sap_history.items():
        if len(entries) < 2:
            continue

        # Level changes
        first_level = entries[0].get("current_level", 0)
        last_level = entries[-1].get("current_level", 0)
        if first_level != last_level:
            level_changes.append({
                "sap_id": sap_id,
                "from_level": first_level,
                "to_level": last_level,
                "change": last_level - first_level,
                "evaluations": len(entries)
            })

        # Gap trends
        gap_counts = [e.get("gap_count", 0) for e in entries]
        if gap_counts:
            gap_trends.append({
                "sap_id": sap_id,
                "first_gaps": gap_counts[0],
                "last_gaps": gap_counts[-1],
                "change": gap_counts[-1] - gap_counts[0],
                "trend": "improving" if gap_counts[-1] < gap_counts[0] else "declining" if gap_counts[-1] > gap_counts[0] else "stable"
            })

        # Effort trends
        effort_hours = [e.get("estimated_effort_hours", 0.0) for e in entries if "estimated_effort_hours" in e]
        if len(effort_hours) >= 2:
            effort_trends.append({
                "sap_id": sap_id,
                "first_effort": effort_hours[0],
                "last_effort": effort_hours[-1],
                "change": effort_hours[-1] - effort_hours[0]
            })

    return {
        "level_changes": sorted(level_changes, key=lambda x: -abs(x["change"])),
        "gap_trends": sorted(gap_trends, key=lambda x: x["change"]),
        "effort_trends": sorted(effort_trends, key=lambda x: -abs(x["change"]))
    }


def print_evaluation_history(history: list[dict], trends: dict = None):
    """Print evaluation history to terminal."""
    if not history:
        print("No evaluation history found.")
        return

    # Group by SAP
    sap_history = defaultdict(list)
    strategic_history = []

    for entry in history:
        if entry.get("evaluation_type") == "strategic":
            strategic_history.append(entry)
        elif "sap_id" in entry:
            sap_history[entry["sap_id"]].append(entry)

    # Print SAP-specific history
    if sap_history:
        print(f"\n📊 Evaluation History ({len(history)} evaluations)")
        print("=" * 80)

        for sap_id in sorted(sap_history.keys()):
            entries = sorted(sap_history[sap_id], key=lambda x: x["timestamp"])
            print(f"\n### {sap_id} ({len(entries)} evaluations)")

            for entry in entries:
                timestamp = entry["timestamp"][:19].replace('T', ' ')
                eval_type = entry.get("evaluation_type", "unknown")
                level = entry.get("current_level", "?")
                gaps = entry.get("gap_count", 0)
                effort = entry.get("estimated_effort_hours", 0.0)

                print(f"  {timestamp} | {eval_type:8s} | L{level} | {gaps} gaps | {effort:.1f}h effort")

    # Print strategic history
    if strategic_history:
        print(f"\n### Strategic Evaluations ({len(strategic_history)})")
        for entry in sorted(strategic_history, key=lambda x: x["timestamp"]):
            timestamp = entry["timestamp"][:19].replace('T', ' ')
            total_saps = entry.get("total_saps_installed", 0)
            avg_level = entry.get("average_adoption_level", 0.0)
            priority_gaps = entry.get("priority_gap_count", 0)

            print(f"  {timestamp} | {total_saps} SAPs | avg L{avg_level:.1f} | {priority_gaps} priority gaps")

    # Print trends
    if trends:
        print("\n## Trend Analysis")
        print("=" * 80)

        if trends["level_changes"]:
            print("\n### Level Changes")
            for change in trends["level_changes"][:5]:
                arrow = "↑" if change["change"] > 0 else "↓"
                print(f"  {arrow} {change['sap_id']}: L{change['from_level']} → L{change['to_level']} ({change['change']:+d} levels, {change['evaluations']} evals)")

        if trends["gap_trends"]:
            print("\n### Gap Trends (Top 5 Improving)")
            for trend in [t for t in trends["gap_trends"] if t["trend"] == "improving"][:5]:
                print(f"  ✅ {trend['sap_id']}: {trend['first_gaps']} → {trend['last_gaps']} gaps ({trend['change']:+d})")

            print("\n### Gap Trends (Top 5 Declining)")
            for trend in [t for t in trends["gap_trends"] if t["trend"] == "declining"][:5]:
                print(f"  ⚠️  {trend['sap_id']}: {trend['first_gaps']} → {trend['last_gaps']} gaps ({trend['change']:+d})")


def export_evaluation_history(
    sap_id: str = None,
    days: int = None,
    evaluation_type: str = None,
    output_path: Path = None,
    format: str = "terminal"
):
    """Export evaluation history with optional filters."""
    history = load_evaluation_history(sap_id=sap_id, days=days, evaluation_type=evaluation_type)

    if not history:
        print("No evaluation history found matching filters.")
        return

    trends = analyze_evaluation_trends(history)

    if format == "json":
        data = {
            "metadata": {
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "filters": {
                    "sap_id": sap_id,
                    "days": days,
                    "evaluation_type": evaluation_type
                },
                "total_evaluations": len(history)
            },
            "history": history,
            "trends": trends
        }

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
            print(f"✅ History exported to: {output_path}")
        else:
            print(json.dumps(data, indent=2, default=str))

    else:  # terminal
        print_evaluation_history(history, trends)


@track_usage
def main():
    parser = argparse.ArgumentParser(
        description="SAP Self-Evaluation Tool - Assess SAP adoption depth",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Evaluation modes (mutually exclusive)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--quick",
        nargs="?",
        const="all",
        metavar="SAP-ID",
        help="Quick check (30s) - validate installation and basic checks. Use 'all' or omit SAP-ID to check all SAPs."
    )
    mode.add_argument(
        "--deep",
        metavar="SAP-ID",
        help="Deep dive (5min) - detailed gap analysis for specific SAP"
    )
    mode.add_argument(
        "--strategic",
        action="store_true",
        help="Strategic analysis (30min) - generate quarterly roadmap"
    )
    mode.add_argument(
        "--export-history",
        action="store_true",
        help="Export evaluation history for trend analysis"
    )

    # Output options
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (markdown for --deep, YAML for --strategic, JSON with --format json)"
    )
    parser.add_argument(
        "--format",
        choices=["terminal", "json", "markdown", "yaml"],
        default="terminal",
        help="Output format (default: terminal)"
    )

    # History export options
    parser.add_argument(
        "--sap",
        metavar="SAP-ID",
        help="Filter history by SAP ID (for --export-history)"
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Only include evaluations from last N days (for --export-history)"
    )
    parser.add_argument(
        "--evaluation-type",
        choices=["quick", "deep", "strategic"],
        help="Filter history by evaluation type (for --export-history)"
    )

    args = parser.parse_args()

    # Initialize evaluator
    evaluator = SAPEvaluator(repo_root=repo_root)

    try:
        if args.export_history:
            # Export evaluation history mode
            export_evaluation_history(
                sap_id=args.sap,
                days=args.days,
                evaluation_type=args.evaluation_type,
                output_path=args.output,
                format=args.format
            )

        elif args.quick:
            # Quick check mode
            if args.quick == "all":
                results = evaluator.quick_check_all()
            else:
                results = evaluator.quick_check(args.quick)

            # Save to history
            if isinstance(results, list):
                for result in results:
                    save_evaluation_to_history(result, "quick")
            else:
                save_evaluation_to_history(results, "quick")

            # Output
            if args.format == "json":
                if isinstance(results, list):
                    data = [asdict(r) for r in results]
                else:
                    data = asdict(results)

                if args.output:
                    save_json_output(data, args.output)
                else:
                    print(json.dumps(data, indent=2, default=str))
            else:
                print_quick_results_terminal(results)

        elif args.deep:
            # Deep dive mode
            result = evaluator.deep_dive(args.deep)

            # Save to history
            save_evaluation_to_history(result, "deep")

            # Output
            if args.format == "json":
                data = asdict(result)
                if args.output:
                    save_json_output(data, args.output)
                else:
                    print(json.dumps(data, indent=2, default=str))
            elif args.output:
                save_markdown_report(result, args.output)
            else:
                print_deep_results_terminal(result)

        elif args.strategic:
            # Strategic analysis mode
            roadmap = evaluator.strategic_analysis()

            # Save to history
            save_evaluation_to_history(roadmap, "strategic")

            # Output
            if args.format == "json":
                data = asdict(roadmap)
                if args.output:
                    save_json_output(data, args.output)
                else:
                    print(json.dumps(data, indent=2, default=str))
            elif args.output:
                save_yaml_roadmap(roadmap, args.output)
            else:
                print_strategic_results_terminal(roadmap)

        return 0

    except KeyboardInterrupt:
        print("\n\nEvaluation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
