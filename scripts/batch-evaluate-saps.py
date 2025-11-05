#!/usr/bin/env python3
"""
Batch SAP Evaluation Script

Runs deep dive evaluations on all SAPs and generates a comprehensive gap report.
Focuses on awareness file coverage and strategic priorities.

Usage:
    python scripts/batch-evaluate-saps.py [--output results.json]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.sap_evaluation import SAPEvaluator


def load_sap_catalog(repo_root: Path) -> List[Dict[str, Any]]:
    """Load SAP catalog from sap-catalog.json"""
    catalog_path = repo_root / "sap-catalog.json"

    if not catalog_path.exists():
        print(f"Error: SAP catalog not found at {catalog_path}")
        sys.exit(1)

    with open(catalog_path, 'r') as f:
        data = json.load(f)

    return data.get("saps", [])


def evaluate_all_saps(repo_root: Path) -> Dict[str, Any]:
    """Run deep dive evaluation on all SAPs"""
    evaluator = SAPEvaluator(repo_root)
    catalog = load_sap_catalog(repo_root)

    results = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_saps": len(catalog),
            "repo_root": str(repo_root)
        },
        "evaluations": [],
        "summary": {
            "by_adoption_level": {},
            "awareness_coverage": {
                "both_files": [],
                "agents_only": [],
                "claude_only": [],
                "neither": []
            },
            "total_gaps": 0,
            "p1_gaps": 0,
            "p2_gaps": 0
        }
    }

    for sap in catalog:
        sap_id = sap.get("id", "")
        location = sap.get("location", "")

        if not sap_id or not location:
            continue

        print(f"Evaluating {sap_id}...", end=" ", flush=True)

        # Run deep dive
        eval_result = evaluator.deep_dive(sap_id)

        # Check awareness files
        sap_dir = repo_root / location
        has_agents = (sap_dir / "AGENTS.md").exists()
        has_claude = (sap_dir / "CLAUDE.md").exists()

        # Count gaps by priority (eval_result is EvaluationResult dataclass)
        p1_gaps = [g for g in eval_result.gaps if g.priority == "P1"]
        p2_gaps = [g for g in eval_result.gaps if g.priority == "P2"]

        # Convert gaps to dict for JSON serialization
        gaps_dict = [
            {
                "gap_id": g.gap_id,
                "title": g.title,
                "priority": g.priority,
                "impact": g.impact,
                "effort": g.effort,
                "estimated_hours": g.estimated_hours
            }
            for g in eval_result.gaps
        ]

        sap_result = {
            "sap_id": sap_id,
            "location": location,
            "adoption_level": eval_result.current_level,
            "completion": eval_result.completion_percent,
            "awareness_files": {
                "agents_md": has_agents,
                "claude_md": has_claude,
                "status": "both_files" if (has_agents and has_claude) else
                         "agents_only" if has_agents else
                         "claude_only" if has_claude else
                         "neither"
            },
            "gaps": {
                "total": len(eval_result.gaps),
                "p1": len(p1_gaps),
                "p2": len(p2_gaps),
                "details": gaps_dict
            }
        }

        results["evaluations"].append(sap_result)

        # Update summary
        level = sap_result["adoption_level"]
        results["summary"]["by_adoption_level"][f"level_{level}"] = \
            results["summary"]["by_adoption_level"].get(f"level_{level}", 0) + 1

        status = sap_result["awareness_files"]["status"]
        results["summary"]["awareness_coverage"][status].append(sap_id)

        results["summary"]["total_gaps"] += sap_result["gaps"]["total"]
        results["summary"]["p1_gaps"] += sap_result["gaps"]["p1"]
        results["summary"]["p2_gaps"] += sap_result["gaps"]["p2"]

        print(f"✓ (Level {level}, {sap_result['gaps']['total']} gaps)")

    return results


def print_summary(results: Dict[str, Any]):
    """Print human-readable summary"""
    summary = results["summary"]

    print("\n" + "="*80)
    print("BATCH SAP EVALUATION SUMMARY")
    print("="*80)

    print(f"\nGenerated: {results['metadata']['generated_at']}")
    print(f"Total SAPs Evaluated: {results['metadata']['total_saps']}")

    print("\n## Adoption Levels")
    for level, count in sorted(summary["by_adoption_level"].items()):
        print(f"  {level}: {count} SAPs")

    print("\n## Awareness File Coverage")
    coverage = summary["awareness_coverage"]
    print(f"  Both files (A+C):  {len(coverage['both_files'])} SAPs")
    print(f"  AGENTS.md only:    {len(coverage['agents_only'])} SAPs")
    print(f"  CLAUDE.md only:    {len(coverage['claude_only'])} SAPs")
    print(f"  Neither file:      {len(coverage['neither'])} SAPs")

    print("\n## Gap Analysis")
    print(f"  Total gaps:   {summary['total_gaps']}")
    print(f"  P1 gaps:      {summary['p1_gaps']}")
    print(f"  P2 gaps:      {summary['p2_gaps']}")

    # Strategic priorities (missing awareness files + high adoption level)
    print("\n## Strategic Priorities (Missing Awareness Files)")

    strategic = []
    for eval_item in results["evaluations"]:
        if eval_item["awareness_files"]["status"] == "neither":
            strategic.append({
                "sap_id": eval_item["sap_id"],
                "level": eval_item["adoption_level"],
                "gaps": eval_item["gaps"]["total"]
            })

    strategic.sort(key=lambda x: (-x["level"], -x["gaps"]))

    if strategic:
        print("\n  Top SAPs needing awareness files (by adoption level):")
        for item in strategic[:10]:  # Top 10
            print(f"    {item['sap_id']:30s} Level {item['level']}, {item['gaps']} gaps")
    else:
        print("  No SAPs missing awareness files!")

    # SAPs with only one file (need equivalent support)
    print("\n## SAPs Needing Equivalent Support (Missing One File)")

    missing_agents = coverage["claude_only"]
    missing_claude = coverage["agents_only"]

    if missing_claude:
        print(f"\n  Missing CLAUDE.md ({len(missing_claude)} SAPs):")
        for sap_id in missing_claude:
            print(f"    {sap_id}")

    if missing_agents:
        print(f"\n  Missing AGENTS.md ({len(missing_agents)} SAPs):")
        for sap_id in missing_agents:
            print(f"    {sap_id}")

    print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(description="Batch evaluate all SAPs")
    parser.add_argument(
        "--output",
        type=str,
        help="Output JSON file path (optional)"
    )
    args = parser.parse_args()

    # Determine repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    print(f"Repository Root: {repo_root}")
    print(f"Starting batch evaluation...\n")

    # Run evaluations
    results = evaluate_all_saps(repo_root)

    # Print summary
    print_summary(results)

    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to: {output_path}")


if __name__ == "__main__":
    main()
