#!/usr/bin/env python3
"""
Generate HTML Adoption Dashboard

Creates an interactive HTML dashboard visualizing SAP adoption progress.

Usage:
    python scripts/generate-dashboard.py --output adoption-dashboard.html
    python scripts/generate-dashboard.py --roadmap project-docs/sap-roadmap-Q1-2026.yaml --output dashboard.html
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

from utils.sap_evaluation import SAPEvaluator, AdoptionRoadmap
from usage_tracker import track_usage


def generate_dashboard_html(roadmap: AdoptionRoadmap, repo_root: Path) -> str:
    """
    Generate HTML dashboard from roadmap data

    Args:
        roadmap: AdoptionRoadmap with SAP adoption data
        repo_root: Path to repository root

    Returns:
        HTML string for dashboard
    """
    # Calculate additional metrics
    total_saps_in_catalog = 30  # Approximate from catalog
    adoption_percentage = (roadmap.total_saps_installed / total_saps_in_catalog) * 100

    # Level distribution percentages
    total = sum(roadmap.adoption_distribution.values())
    level_percentages = {
        level: (count / total * 100) if total > 0 else 0
        for level, count in roadmap.adoption_distribution.items()
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAP Adoption Dashboard - {roadmap.target_quarter}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            color: #2d3748;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            color: #718096;
            font-size: 14px;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .metric-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}

        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}

        .metric-card h3 {{
            color: #718096;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}

        .metric-card .value {{
            color: #2d3748;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .metric-card .description {{
            color: #a0aec0;
            font-size: 13px;
        }}

        .metric-card.highlight {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .metric-card.highlight h3,
        .metric-card.highlight .value,
        .metric-card.highlight .description {{
            color: white;
        }}

        .section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .section h2 {{
            color: #2d3748;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
        }}

        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e2e8f0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }}

        .level-distribution {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 20px;
        }}

        .level-item {{
            text-align: center;
            padding: 15px;
            background: #f7fafc;
            border-radius: 8px;
        }}

        .level-item .level-name {{
            font-size: 12px;
            color: #718096;
            margin-bottom: 5px;
        }}

        .level-item .level-count {{
            font-size: 24px;
            font-weight: bold;
            color: #2d3748;
        }}

        .level-item .level-percentage {{
            font-size: 11px;
            color: #a0aec0;
        }}

        .gaps-list {{
            list-style: none;
        }}

        .gap-item {{
            padding: 15px;
            margin-bottom: 10px;
            background: #f7fafc;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}

        .gap-item .gap-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }}

        .gap-item .gap-title {{
            font-weight: 600;
            color: #2d3748;
        }}

        .gap-item .gap-meta {{
            font-size: 12px;
            color: #718096;
        }}

        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 8px;
        }}

        .badge.current {{
            background: #fc8181;
            color: white;
        }}

        .badge.next {{
            background: #f6ad55;
            color: white;
        }}

        .badge.future {{
            background: #68d391;
            color: white;
        }}

        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            font-size: 14px;
        }}

        .footer a {{
            color: white;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SAP Adoption Dashboard</h1>
            <p class="subtitle">Generated: {roadmap.generated_at.strftime('%Y-%m-%d %H:%M:%S')} | Target Quarter: {roadmap.target_quarter}</p>
            <p class="subtitle">Next Review: {roadmap.next_review_date or 'TBD'}</p>
        </div>

        <div class="metrics-grid">
            <div class="metric-card highlight">
                <h3>Total SAPs Installed</h3>
                <div class="value">{roadmap.total_saps_installed}</div>
                <div class="description">{adoption_percentage:.0f}% of catalog</div>
            </div>

            <div class="metric-card">
                <h3>Average Level</h3>
                <div class="value">{roadmap.average_adoption_level:.2f}</div>
                <div class="description">Target: 2.5</div>
            </div>

            <div class="metric-card">
                <h3>Hours Invested</h3>
                <div class="value">{roadmap.total_hours_invested:.1f}</div>
                <div class="description">Learning & integration</div>
            </div>

            <div class="metric-card">
                <h3>Priority Gaps</h3>
                <div class="value">{len(roadmap.priority_gaps)}</div>
                <div class="description">Identified opportunities</div>
            </div>
        </div>

        <div class="section">
            <h2>Adoption Progress</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {adoption_percentage:.0f}%">
                    {adoption_percentage:.0f}%
                </div>
            </div>
            <p style="color: #718096; font-size: 13px; margin-top: 10px;">
                {roadmap.total_saps_installed} of {total_saps_in_catalog} SAPs adopted
            </p>
        </div>

        <div class="section">
            <h2>Distribution by Level</h2>
            <div class="level-distribution">
                <div class="level-item">
                    <div class="level-name">Level 0</div>
                    <div class="level-count">{roadmap.adoption_distribution.get('level_0', 0)}</div>
                    <div class="level-percentage">{level_percentages.get('level_0', 0):.0f}%</div>
                </div>
                <div class="level-item">
                    <div class="level-name">Level 1</div>
                    <div class="level-count">{roadmap.adoption_distribution.get('level_1', 0)}</div>
                    <div class="level-percentage">{level_percentages.get('level_1', 0):.0f}%</div>
                </div>
                <div class="level-item">
                    <div class="level-name">Level 2</div>
                    <div class="level-count">{roadmap.adoption_distribution.get('level_2', 0)}</div>
                    <div class="level-percentage">{level_percentages.get('level_2', 0):.0f}%</div>
                </div>
                <div class="level-item">
                    <div class="level-name">Level 3</div>
                    <div class="level-count">{roadmap.adoption_distribution.get('level_3', 0)}</div>
                    <div class="level-percentage">{level_percentages.get('level_3', 0):.0f}%</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Priority Gaps (Top 10)</h2>
            <ul class="gaps-list">
"""

    # Add top 10 priority gaps
    for gap in roadmap.priority_gaps[:10]:
        badge_class = gap.sprint if gap.sprint in ['current', 'next', 'future'] else 'future'
        html += f"""
                <li class="gap-item">
                    <div class="gap-header">
                        <span class="gap-title">#{gap.rank}. {gap.sap_id}: {gap.gap.title}</span>
                        <span class="badge {badge_class}">{gap.sprint.upper()}</span>
                    </div>
                    <div class="gap-meta">
                        Impact: {gap.gap.impact.capitalize()} |
                        Effort: {gap.gap.effort.capitalize()} |
                        Priority: {gap.gap.priority} |
                        Score: {gap.priority_score:.2f}
                    </div>
                </li>
"""

    # Close HTML
    html += """
            </ul>
        </div>

        <div class="footer">
            <p>Generated by <strong>SAP-019 Self-Evaluation</strong></p>
            <p><a href="https://github.com/liminalcommons/chora-base">chora-base Repository</a></p>
        </div>
    </div>
</body>
</html>
"""

    return html


@track_usage
def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML SAP adoption dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--roadmap",
        type=Path,
        help="Path to existing roadmap YAML (will generate if not provided)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("adoption-dashboard.html"),
        help="Output HTML file path (default: adoption-dashboard.html)"
    )

    args = parser.parse_args()

    try:
        # Get roadmap data
        if args.roadmap and args.roadmap.exists():
            # Load from YAML (would need PyYAML)
            print(f"Loading roadmap from {args.roadmap}...")
            # For now, generate fresh roadmap
            evaluator = SAPEvaluator(repo_root=repo_root)
            roadmap = evaluator.strategic_analysis()
        else:
            # Generate fresh roadmap
            print("Generating strategic analysis...")
            evaluator = SAPEvaluator(repo_root=repo_root)
            roadmap = evaluator.strategic_analysis()

        # Generate HTML
        print("Generating dashboard HTML...")
        html = generate_dashboard_html(roadmap, repo_root)

        # Write to file
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Dashboard generated: {args.output}")
        print(f"\nOpen in browser:")
        print(f"  macOS:   open {args.output}")
        print(f"  Linux:   xdg-open {args.output}")
        print(f"  Windows: start {args.output}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
