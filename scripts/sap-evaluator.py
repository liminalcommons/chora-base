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

Examples:
    # Check all installed SAPs
    python scripts/sap-evaluator.py --quick

    # Detailed assessment of testing framework
    python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md

    # Generate quarterly roadmap
    python scripts/sap-evaluator.py --strategic --output project-docs/sap-roadmap.yaml
"""

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime
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

    args = parser.parse_args()

    # Initialize evaluator
    evaluator = SAPEvaluator(repo_root=repo_root)

    try:
        if args.quick:
            # Quick check mode
            if args.quick == "all":
                results = evaluator.quick_check_all()
            else:
                results = evaluator.quick_check(args.quick)

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
