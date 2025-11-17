#!/usr/bin/env python3
"""
Traceability Dashboard Generator for SAP-056 (Lifecycle Traceability)

Generates an HTML dashboard visualizing:
- Overall traceability metrics
- Feature coverage by status
- Validation rule pass rates
- Artifact distribution (code, tests, docs)
- Traceability gaps and recommendations

Usage:
    python traceability-dashboard.py [--manifest feature-manifest.yaml] [--output dashboard.html]

Options:
    --manifest PATH     Path to feature-manifest.yaml (default: ./feature-manifest.yaml)
    --output FILE       Output HTML file (default: traceability-dashboard.html)
    --validation PATH   Path to validation report JSON (from validate-traceability.py --json)
    --title TITLE       Dashboard title (default: "Traceability Dashboard")

Exit Codes:
    0 - Success
    2 - Fatal error
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}

        .subtitle {{
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .metric-card.success {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}

        .metric-card.warning {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}

        .metric-card.info {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}

        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}

        .metric-value {{
            font-size: 3em;
            font-weight: bold;
            line-height: 1;
        }}

        .metric-subtitle {{
            font-size: 0.85em;
            opacity: 0.8;
            margin-top: 5px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        .chart {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .bar-item {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .bar-label {{
            min-width: 150px;
            font-weight: 500;
            color: #555;
        }}

        .bar-container {{
            flex: 1;
            background: #e0e0e0;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }}

        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            transition: width 0.5s ease;
        }}

        .bar-fill.success {{
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        }}

        .bar-fill.warning {{
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        }}

        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}

        .feature-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .feature-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .feature-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }}

        .feature-id {{
            font-weight: bold;
            color: #667eea;
            font-size: 0.9em;
        }}

        .feature-status {{
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .status-implemented {{
            background: #d4edda;
            color: #155724;
        }}

        .status-in_progress {{
            background: #fff3cd;
            color: #856404;
        }}

        .status-planned {{
            background: #d1ecf1;
            color: #0c5460;
        }}

        .feature-name {{
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #333;
        }}

        .feature-stats {{
            display: flex;
            gap: 10px;
            font-size: 0.85em;
            color: #666;
        }}

        .stat-badge {{
            background: #f0f0f0;
            padding: 3px 8px;
            border-radius: 4px;
        }}

        .recommendations {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 4px;
        }}

        .recommendations h3 {{
            color: #856404;
            margin-bottom: 15px;
        }}

        .recommendations ul {{
            list-style: none;
            padding-left: 0;
        }}

        .recommendations li {{
            padding: 8px 0;
            border-bottom: 1px solid #ffe69c;
        }}

        .recommendations li:last-child {{
            border-bottom: none;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}

        .validation-rules {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 15px;
        }}

        .rule-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
        }}

        .rule-card.passed {{
            border-color: #28a745;
            background: #f8fff9;
        }}

        .rule-card.failed {{
            border-color: #dc3545;
            background: #fff8f8;
        }}

        .rule-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .rule-name {{
            font-weight: bold;
            font-size: 1.1em;
        }}

        .rule-status {{
            font-size: 1.5em;
        }}

        .rule-rate {{
            font-size: 1.2em;
            font-weight: bold;
            margin: 10px 0;
        }}

        .rule-rate.high {{
            color: #28a745;
        }}

        .rule-rate.medium {{
            color: #ffc107;
        }}

        .rule-rate.low {{
            color: #dc3545;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="subtitle">Generated on {timestamp}</div>

        <div class="metrics-grid">
            {metrics_cards}
        </div>

        {validation_section}

        <div class="section">
            <h2 class="section-title">Feature Coverage</h2>
            {feature_coverage_chart}
        </div>

        <div class="section">
            <h2 class="section-title">Features Overview</h2>
            <div class="feature-grid">
                {features_cards}
            </div>
        </div>

        {recommendations_section}

        <div class="footer">
            Generated by SAP-056 Traceability Dashboard | Manifest: {manifest_path}
        </div>
    </div>
</body>
</html>
"""


class DashboardGenerator:
    """Generator for HTML traceability dashboard."""

    def __init__(self, manifest_path: str):
        self.manifest_path = Path(manifest_path)

        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Manifest not found: {manifest_path}", file=sys.stderr)
            sys.exit(2)
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML: {e}", file=sys.stderr)
            sys.exit(2)

        self.validation = None

    def load_validation_report(self, validation_path: str):
        """Load validation report JSON."""
        try:
            with open(validation_path, 'r', encoding='utf-8') as f:
                self.validation = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load validation report: {e}", file=sys.stderr)

    def calculate_metrics(self) -> Dict:
        """Calculate dashboard metrics."""
        features = self.manifest.get("features", [])

        total_features = len(features)
        total_code = sum(len(f.get("code", [])) for f in features)
        total_tests = sum(len(f.get("tests", [])) for f in features)
        total_docs = sum(len(f.get("documentation", [])) for f in features)
        total_requirements = sum(len(f.get("requirements", [])) for f in features)

        # Count features by status
        status_counts = {}
        for feature in features:
            status = feature.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        # Calculate completeness
        features_with_vision = sum(1 for f in features if f.get("vision_ref"))
        features_with_tests = sum(1 for f in features if f.get("tests"))
        features_with_docs = sum(1 for f in features if f.get("documentation"))

        completeness = 0
        if total_features > 0:
            completeness = (
                (features_with_vision / total_features) * 0.3 +
                (features_with_tests / total_features) * 0.35 +
                (features_with_docs / total_features) * 0.35
            ) * 100

        return {
            "total_features": total_features,
            "total_code": total_code,
            "total_tests": total_tests,
            "total_docs": total_docs,
            "total_requirements": total_requirements,
            "status_counts": status_counts,
            "completeness": completeness,
            "features_with_vision": features_with_vision,
            "features_with_tests": features_with_tests,
            "features_with_docs": features_with_docs
        }

    def generate_metrics_cards(self, metrics: Dict) -> str:
        """Generate metric cards HTML."""
        completeness = metrics["completeness"]

        # Determine card class based on completeness
        if completeness >= 80:
            card_class = "success"
        elif completeness >= 50:
            card_class = "warning"
        else:
            card_class = "info"

        cards = [
            f"""
            <div class="metric-card {card_class}">
                <div class="metric-label">Traceability Completeness</div>
                <div class="metric-value">{completeness:.0f}%</div>
                <div class="metric-subtitle">Overall coverage score</div>
            </div>
            """,
            f"""
            <div class="metric-card info">
                <div class="metric-label">Total Features</div>
                <div class="metric-value">{metrics['total_features']}</div>
                <div class="metric-subtitle">{metrics['status_counts'].get('implemented', 0)} implemented</div>
            </div>
            """,
            f"""
            <div class="metric-card info">
                <div class="metric-label">Code Files</div>
                <div class="metric-value">{metrics['total_code']}</div>
                <div class="metric-subtitle">Tracked in manifest</div>
            </div>
            """,
            f"""
            <div class="metric-card info">
                <div class="metric-label">Test Cases</div>
                <div class="metric-value">{metrics['total_tests']}</div>
                <div class="metric-subtitle">Linked to features</div>
            </div>
            """,
            f"""
            <div class="metric-card info">
                <div class="metric-label">Documentation</div>
                <div class="metric-value">{metrics['total_docs']}</div>
                <div class="metric-subtitle">Feature docs</div>
            </div>
            """,
            f"""
            <div class="metric-card info">
                <div class="metric-label">Requirements</div>
                <div class="metric-value">{metrics['total_requirements']}</div>
                <div class="metric-subtitle">Defined requirements</div>
            </div>
            """
        ]

        return "\n".join(cards)

    def generate_feature_coverage_chart(self, metrics: Dict) -> str:
        """Generate feature coverage bar chart."""
        total = metrics["total_features"]
        if total == 0:
            return "<p>No features found in manifest.</p>"

        bars = [
            ("Vision Linkage", metrics["features_with_vision"], total),
            ("Test Coverage", metrics["features_with_tests"], total),
            ("Documentation", metrics["features_with_docs"], total)
        ]

        bar_html = []
        for label, count, total_count in bars:
            percentage = (count / total_count * 100) if total_count > 0 else 0
            bar_class = "success" if percentage >= 80 else "warning" if percentage >= 50 else ""

            bar_html.append(f"""
            <div class="bar-item">
                <div class="bar-label">{label}</div>
                <div class="bar-container">
                    <div class="bar-fill {bar_class}" style="width: {percentage}%">
                        {count}/{total_count} ({percentage:.0f}%)
                    </div>
                </div>
            </div>
            """)

        return f'<div class="chart"><div class="bar-chart">{"".join(bar_html)}</div></div>'

    def generate_features_cards(self) -> str:
        """Generate feature cards HTML."""
        features = self.manifest.get("features", [])

        if not features:
            return "<p>No features found in manifest.</p>"

        cards = []
        for feature in features:
            feature_id = feature.get("id", "UNKNOWN")
            name = feature.get("name", "Unnamed Feature")
            status = feature.get("status", "unknown")
            code_count = len(feature.get("code", []))
            test_count = len(feature.get("tests", []))
            doc_count = len(feature.get("documentation", []))

            cards.append(f"""
            <div class="feature-card">
                <div class="feature-header">
                    <span class="feature-id">{feature_id}</span>
                    <span class="feature-status status-{status}">{status}</span>
                </div>
                <div class="feature-name">{name}</div>
                <div class="feature-stats">
                    <span class="stat-badge">📄 {code_count} files</span>
                    <span class="stat-badge">🧪 {test_count} tests</span>
                    <span class="stat-badge">📚 {doc_count} docs</span>
                </div>
            </div>
            """)

        return "\n".join(cards)

    def generate_validation_section(self) -> str:
        """Generate validation rules section."""
        if not self.validation:
            return ""

        rules = self.validation.get("rules", [])
        if not rules:
            return ""

        rule_cards = []
        for rule in rules:
            passed = rule.get("passed", False)
            pass_rate = rule.get("pass_rate", 0)
            card_class = "passed" if passed else "failed"
            status_icon = "✅" if passed else "❌"

            rate_class = "high" if pass_rate >= 80 else "medium" if pass_rate >= 50 else "low"

            rule_cards.append(f"""
            <div class="rule-card {card_class}">
                <div class="rule-header">
                    <span class="rule-name">Rule {rule['rule_number']}: {rule['rule_name']}</span>
                    <span class="rule-status">{status_icon}</span>
                </div>
                <div class="rule-rate {rate_class}">{pass_rate:.0f}% ({rule['passed_items']}/{rule['total_items']})</div>
            </div>
            """)

        overall_passed = self.validation.get("overall_passed", False)
        overall_rate = self.validation.get("pass_rate", 0)
        overall_status = "✅ ALL RULES PASS" if overall_passed else "❌ SOME RULES FAIL"

        return f"""
        <div class="section">
            <h2 class="section-title">Validation Rules ({overall_rate:.0f}%)</h2>
            <p style="margin-bottom: 20px; font-size: 1.1em;"><strong>{overall_status}</strong></p>
            <div class="validation-rules">
                {"".join(rule_cards)}
            </div>
        </div>
        """

    def generate_recommendations(self, metrics: Dict) -> str:
        """Generate recommendations section."""
        recommendations = []

        total = metrics["total_features"]
        if total == 0:
            recommendations.append("Start by creating your first feature entry in feature-manifest.yaml")
            return self._wrap_recommendations(recommendations)

        if metrics["features_with_vision"] < total:
            missing = total - metrics["features_with_vision"]
            recommendations.append(f"Add vision_ref to {missing} feature(s) without vision linkage")

        if metrics["features_with_tests"] < total:
            missing = total - metrics["features_with_tests"]
            recommendations.append(f"Add tests to {missing} feature(s) without test coverage")

        if metrics["features_with_docs"] < total:
            missing = total - metrics["features_with_docs"]
            recommendations.append(f"Add documentation to {missing} feature(s) without docs")

        if metrics["completeness"] < 80:
            recommendations.append("Work towards 80%+ completeness for L2 compliance")

        if not recommendations:
            recommendations.append("Great work! All features have complete traceability.")

        return self._wrap_recommendations(recommendations)

    def _wrap_recommendations(self, recommendations: List[str]) -> str:
        """Wrap recommendations in HTML."""
        items = "\n".join(f"<li>• {rec}</li>" for rec in recommendations)
        return f"""
        <div class="section recommendations">
            <h3>Recommendations</h3>
            <ul>
                {items}
            </ul>
        </div>
        """

    def generate(self, title: str = "Traceability Dashboard") -> str:
        """Generate complete HTML dashboard."""
        metrics = self.calculate_metrics()

        return HTML_TEMPLATE.format(
            title=title,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            manifest_path=str(self.manifest_path),
            metrics_cards=self.generate_metrics_cards(metrics),
            validation_section=self.generate_validation_section(),
            feature_coverage_chart=self.generate_feature_coverage_chart(metrics),
            features_cards=self.generate_features_cards(),
            recommendations_section=self.generate_recommendations(metrics)
        )


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML traceability dashboard from feature-manifest.yaml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--manifest",
        metavar="PATH",
        default="feature-manifest.yaml",
        help="Path to feature-manifest.yaml (default: ./feature-manifest.yaml)"
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default="traceability-dashboard.html",
        help="Output HTML file (default: traceability-dashboard.html)"
    )
    parser.add_argument(
        "--validation",
        metavar="PATH",
        help="Path to validation report JSON (from validate-traceability.py --json)"
    )
    parser.add_argument(
        "--title",
        metavar="TITLE",
        default="Traceability Dashboard",
        help="Dashboard title (default: 'Traceability Dashboard')"
    )

    args = parser.parse_args()

    # Generate dashboard
    generator = DashboardGenerator(args.manifest)

    if args.validation:
        generator.load_validation_report(args.validation)

    html = generator.generate(title=args.title)

    # Write output
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Dashboard generated: {args.output}")
    sys.exit(0)


if __name__ == "__main__":
    main()
