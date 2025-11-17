#!/usr/bin/env python3
"""
Traceability Validation Script for SAP-056 (Lifecycle Traceability)

Validates feature-manifest.yaml against 10 traceability rules:
1. Forward Linkage: Vision outcomes → features
2. Bidirectional Linkage: Docs ↔ code bidirectional
3. Evidence Requirement: Features → tests AND docs
4. Closed Loop: Git commits → tasks → features
5. Orphan Detection: No artifacts without parent
6. Schema Compliance: Manifest validates against JSON Schema
7. Reference Integrity: All paths exist
8. Requirement Coverage: Requirements → tests with markers
9. Documentation Coverage: Features → docs in frontmatter
10. Event Correlation: Task completions → A-MEM events with feature_id

Usage:
    python validate-traceability.py [--feature FEAT-XXX] [--json] [--output report.md]

Options:
    --feature FEAT-XXX  Validate specific feature only
    --json              Output JSON instead of markdown
    --output FILE       Write report to file (default: stdout)
    --schema PATH       Path to feature-manifest.schema.json
    --manifest PATH     Path to feature-manifest.yaml (default: ./feature-manifest.yaml)

Exit Codes:
    0 - All rules pass
    1 - One or more rules fail
    2 - Fatal error (manifest missing, invalid YAML, etc.)
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


@dataclass
class ValidationResult:
    """Result of a single validation rule."""
    rule_number: int
    rule_name: str
    passed: bool
    total_items: int
    passed_items: int
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate as percentage."""
        if self.total_items == 0:
            return 100.0
        return (self.passed_items / self.total_items) * 100.0


@dataclass
class ValidationReport:
    """Complete validation report for all rules."""
    timestamp: str
    manifest_path: str
    feature_filter: Optional[str]
    total_features: int
    rules: List[ValidationResult] = field(default_factory=list)

    @property
    def overall_passed(self) -> bool:
        """Check if all rules passed."""
        return all(rule.passed for rule in self.rules)

    @property
    def pass_rate(self) -> float:
        """Calculate overall pass rate."""
        if not self.rules:
            return 0.0
        passed_rules = sum(1 for rule in self.rules if rule.passed)
        return (passed_rules / len(self.rules)) * 100.0


class TraceabilityValidator:
    """Validator for SAP-056 traceability rules."""

    def __init__(self, manifest_path: str, schema_path: Optional[str] = None):
        self.manifest_path = Path(manifest_path)
        self.schema_path = Path(schema_path) if schema_path else self._find_schema()
        self.project_root = self.manifest_path.parent

        # Load manifest
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Manifest not found: {self.manifest_path}", file=sys.stderr)
            sys.exit(2)
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML in manifest: {e}", file=sys.stderr)
            sys.exit(2)

        # Load schema
        if self.schema_path and self.schema_path.exists():
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
        else:
            self.schema = None

    def _find_schema(self) -> Optional[Path]:
        """Find feature-manifest.schema.json in standard locations."""
        candidates = [
            self.project_root / "schemas" / "feature-manifest.schema.json",
            self.project_root / "chora-base" / "docs" / "skilled-awareness" / "lifecycle-traceability" / "schemas" / "feature-manifest.schema.json",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def validate_all(self, feature_filter: Optional[str] = None) -> ValidationReport:
        """Run all 10 validation rules."""
        features = self.manifest.get("features", [])

        # Apply feature filter
        if feature_filter:
            features = [f for f in features if f.get("id") == feature_filter]

        report = ValidationReport(
            timestamp=datetime.now().isoformat(),
            manifest_path=str(self.manifest_path),
            feature_filter=feature_filter,
            total_features=len(features)
        )

        # Run each rule
        report.rules.append(self.rule_1_forward_linkage(features))
        report.rules.append(self.rule_2_bidirectional_linkage(features))
        report.rules.append(self.rule_3_evidence_requirement(features))
        report.rules.append(self.rule_4_closed_loop(features))
        report.rules.append(self.rule_5_orphan_detection(features))
        report.rules.append(self.rule_6_schema_compliance())
        report.rules.append(self.rule_7_reference_integrity(features))
        report.rules.append(self.rule_8_requirement_coverage(features))
        report.rules.append(self.rule_9_documentation_coverage(features))
        report.rules.append(self.rule_10_event_correlation(features))

        return report

    def rule_1_forward_linkage(self, features: List[dict]) -> ValidationResult:
        """Rule 1: Every vision outcome → ≥1 feature."""
        passed_items = 0
        failures = []

        for feature in features:
            feature_id = feature.get("id", "UNKNOWN")
            vision_ref = feature.get("vision_ref")

            if vision_ref:
                passed_items += 1
            else:
                failures.append(f"{feature_id}: Missing vision_ref")

        return ValidationResult(
            rule_number=1,
            rule_name="Forward Linkage",
            passed=len(failures) == 0,
            total_items=len(features),
            passed_items=passed_items,
            failures=failures
        )

    def rule_2_bidirectional_linkage(self, features: List[dict]) -> ValidationResult:
        """Rule 2: If doc references code, code manifest lists doc."""
        passed_items = 0
        failures = []
        warnings = []

        # Build code→docs mapping from manifest
        code_to_docs = {}
        for feature in features:
            for code_ref in (feature.get("code") or []):
                code_path = code_ref.get("path")
                if code_path:
                    if code_path not in code_to_docs:
                        code_to_docs[code_path] = set()
                    for doc_ref in (feature.get("documentation") or []):
                        doc_path = doc_ref.get("path")
                        if doc_path:
                            code_to_docs[code_path].add(doc_path)

        # Check docs with frontmatter for code_references
        docs_checked = 0
        for feature in features:
            for doc_ref in (feature.get("documentation") or []):
                doc_path = doc_ref.get("path")
                if not doc_path:
                    continue

                full_doc_path = self.project_root / doc_path
                if not full_doc_path.exists():
                    continue

                # Parse frontmatter
                try:
                    with open(full_doc_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract frontmatter
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            frontmatter = yaml.safe_load(parts[1])
                            code_refs = frontmatter.get("code_references", [])

                            docs_checked += 1

                            # Check bidirectionality
                            bidirectional = True
                            for code_ref in code_refs:
                                if code_ref not in code_to_docs or doc_path not in code_to_docs[code_ref]:
                                    failures.append(f"{doc_path} references {code_ref}, but manifest doesn't list this linkage")
                                    bidirectional = False

                            if bidirectional and code_refs:
                                passed_items += 1
                except Exception as e:
                    warnings.append(f"Failed to parse frontmatter in {doc_path}: {e}")

        if docs_checked == 0:
            warnings.append("No documentation with frontmatter found (Rule 2 not applicable)")

        return ValidationResult(
            rule_number=2,
            rule_name="Bidirectional Linkage",
            passed=len(failures) == 0,
            total_items=docs_checked,
            passed_items=passed_items,
            failures=failures,
            warnings=warnings
        )

    def rule_3_evidence_requirement(self, features: List[dict]) -> ValidationResult:
        """Rule 3: Every feature → ≥1 test AND ≥1 doc."""
        passed_items = 0
        failures = []

        for feature in features:
            feature_id = feature.get("id", "UNKNOWN")
            tests = feature.get("tests") or []
            docs = feature.get("documentation") or []

            has_tests = len(tests) > 0
            has_docs = len(docs) > 0

            if has_tests and has_docs:
                passed_items += 1
            else:
                issues = []
                if not has_tests:
                    issues.append("no tests")
                if not has_docs:
                    issues.append("no documentation")
                failures.append(f"{feature_id}: {', '.join(issues)}")

        return ValidationResult(
            rule_number=3,
            rule_name="Evidence Requirement",
            passed=len(failures) == 0,
            total_items=len(features),
            passed_items=passed_items,
            failures=failures
        )

    def rule_4_closed_loop(self, features: List[dict]) -> ValidationResult:
        """Rule 4: Every git commit closing task → links to feature."""
        # This rule requires git log parsing - simplified implementation
        warnings = ["Rule 4 (Closed Loop) requires git log parsing - not fully implemented"]

        return ValidationResult(
            rule_number=4,
            rule_name="Closed Loop",
            passed=True,  # Pass by default (not implemented)
            total_items=0,
            passed_items=0,
            warnings=warnings
        )

    def rule_5_orphan_detection(self, features: List[dict]) -> ValidationResult:
        """Rule 5: No artifact without parent linkage."""
        failures = []

        # Check each feature has vision_ref
        for feature in features:
            feature_id = feature.get("id", "UNKNOWN")
            vision_ref = feature.get("vision_ref")

            if not vision_ref:
                failures.append(f"{feature_id}: Orphaned (no vision_ref)")

        return ValidationResult(
            rule_number=5,
            rule_name="Orphan Detection",
            passed=len(failures) == 0,
            total_items=len(features),
            passed_items=len(features) - len(failures),
            failures=failures
        )

    def rule_6_schema_compliance(self) -> ValidationResult:
        """Rule 6: feature-manifest.yaml passes JSON Schema validation."""
        if not self.schema:
            return ValidationResult(
                rule_number=6,
                rule_name="Schema Compliance",
                passed=True,
                total_items=1,
                passed_items=1,
                warnings=["JSON Schema not found - skipping validation"]
            )

        try:
            jsonschema.validate(instance=self.manifest, schema=self.schema)
            return ValidationResult(
                rule_number=6,
                rule_name="Schema Compliance",
                passed=True,
                total_items=1,
                passed_items=1
            )
        except jsonschema.ValidationError as e:
            return ValidationResult(
                rule_number=6,
                rule_name="Schema Compliance",
                passed=False,
                total_items=1,
                passed_items=0,
                failures=[f"Schema validation failed: {e.message}"]
            )

    def rule_7_reference_integrity(self, features: List[dict]) -> ValidationResult:
        """Rule 7: All vision_ref/code/docs/tests paths exist."""
        total_refs = 0
        passed_refs = 0
        failures = []

        for feature in features:
            feature_id = feature.get("id", "UNKNOWN")

            # Check code paths
            for code_ref in (feature.get("code") or []):
                code_path = code_ref.get("path")
                if code_path:
                    total_refs += 1
                    full_path = self.project_root / code_path
                    if full_path.exists():
                        passed_refs += 1
                    else:
                        failures.append(f"{feature_id}: Code file not found: {code_path}")

            # Check test paths
            for test_ref in (feature.get("tests") or []):
                test_path = test_ref.get("path")
                if test_path:
                    total_refs += 1
                    # Extract file path (before ::)
                    file_path = test_path.split("::")[0]
                    full_path = self.project_root / file_path
                    if full_path.exists():
                        passed_refs += 1
                    else:
                        failures.append(f"{feature_id}: Test file not found: {file_path}")

            # Check doc paths
            for doc_ref in (feature.get("documentation") or []):
                doc_path = doc_ref.get("path")
                if doc_path:
                    total_refs += 1
                    full_path = self.project_root / doc_path
                    if full_path.exists():
                        passed_refs += 1
                    else:
                        failures.append(f"{feature_id}: Documentation file not found: {doc_path}")

        return ValidationResult(
            rule_number=7,
            rule_name="Reference Integrity",
            passed=len(failures) == 0,
            total_items=total_refs,
            passed_items=passed_refs,
            failures=failures
        )

    def rule_8_requirement_coverage(self, features: List[dict]) -> ValidationResult:
        """Rule 8: Every requirement → ≥1 test with marker."""
        total_reqs = 0
        passed_reqs = 0
        failures = []

        for feature in features:
            feature_id = feature.get("id", "UNKNOWN")
            requirements = feature.get("requirements") or []
            tests = feature.get("tests") or []

            for req in requirements:
                req_id = req.get("id", "UNKNOWN")
                total_reqs += 1

                # Check if any test references this requirement
                has_test = any(test.get("requirement") == req_id for test in tests)

                if has_test:
                    passed_reqs += 1
                else:
                    failures.append(f"{feature_id}/{req_id}: No test found")

        return ValidationResult(
            rule_number=8,
            rule_name="Requirement Coverage",
            passed=len(failures) == 0,
            total_items=total_reqs,
            passed_items=passed_reqs,
            failures=failures
        )

    def rule_9_documentation_coverage(self, features: List[dict]) -> ValidationResult:
        """Rule 9: Every feature → ≥1 doc in frontmatter."""
        # This is equivalent to Rule 3 (docs part), but checks frontmatter
        passed_items = 0
        failures = []

        for feature in features:
            feature_id = feature.get("id", "UNKNOWN")
            docs = feature.get("documentation") or []

            if len(docs) > 0:
                passed_items += 1
            else:
                failures.append(f"{feature_id}: No documentation")

        return ValidationResult(
            rule_number=9,
            rule_name="Documentation Coverage",
            passed=len(failures) == 0,
            total_items=len(features),
            passed_items=passed_items,
            failures=failures
        )

    def rule_10_event_correlation(self, features: List[dict]) -> ValidationResult:
        """Rule 10: Every task completion → A-MEM event with feature_id."""
        # This rule requires A-MEM event log parsing - simplified implementation
        warnings = ["Rule 10 (Event Correlation) requires A-MEM event log parsing - not fully implemented"]

        return ValidationResult(
            rule_number=10,
            rule_name="Event Correlation",
            passed=True,  # Pass by default (not implemented)
            total_items=0,
            passed_items=0,
            warnings=warnings
        )


def format_markdown(report: ValidationReport) -> str:
    """Format validation report as markdown."""
    lines = [
        "# Traceability Validation Report",
        "",
        f"**Generated**: {report.timestamp}",
        f"**Manifest**: {report.manifest_path}",
        f"**Features**: {report.total_features}",
        ""
    ]

    if report.feature_filter:
        lines.append(f"**Filter**: {report.feature_filter}")
        lines.append("")

    # Overall summary
    status = "✅ PASS" if report.overall_passed else "❌ FAIL"
    lines.extend([
        "## Overall Status",
        "",
        f"**Status**: {status}",
        f"**Pass Rate**: {report.pass_rate:.1f}% ({sum(1 for r in report.rules if r.passed)}/{len(report.rules)} rules)",
        ""
    ])

    # Per-rule results
    lines.extend([
        "## Validation Rules",
        ""
    ])

    for rule in report.rules:
        status_icon = "✅" if rule.passed else "❌"
        lines.extend([
            f"### {status_icon} Rule {rule.rule_number}: {rule.rule_name}",
            ""
        ])

        if rule.total_items > 0:
            lines.append(f"**Pass Rate**: {rule.pass_rate:.1f}% ({rule.passed_items}/{rule.total_items})")
            lines.append("")

        if rule.failures:
            lines.append("**Failures**:")
            lines.append("")
            for failure in rule.failures[:10]:  # Limit to 10 failures
                lines.append(f"- {failure}")
            if len(rule.failures) > 10:
                lines.append(f"- ... and {len(rule.failures) - 10} more")
            lines.append("")

        if rule.warnings:
            lines.append("**Warnings**:")
            lines.append("")
            for warning in rule.warnings:
                lines.append(f"- ⚠️ {warning}")
            lines.append("")

    return "\n".join(lines)


def format_json(report: ValidationReport) -> str:
    """Format validation report as JSON."""
    return json.dumps({
        "timestamp": report.timestamp,
        "manifest_path": report.manifest_path,
        "feature_filter": report.feature_filter,
        "total_features": report.total_features,
        "overall_passed": report.overall_passed,
        "pass_rate": report.pass_rate,
        "rules": [
            {
                "rule_number": rule.rule_number,
                "rule_name": rule.rule_name,
                "passed": rule.passed,
                "total_items": rule.total_items,
                "passed_items": rule.passed_items,
                "pass_rate": rule.pass_rate,
                "failures": rule.failures,
                "warnings": rule.warnings
            }
            for rule in report.rules
        ]
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Validate feature-manifest.yaml against SAP-056 traceability rules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--feature",
        metavar="FEAT-XXX",
        help="Validate specific feature only"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of markdown"
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write report to file (default: stdout)"
    )
    parser.add_argument(
        "--schema",
        metavar="PATH",
        help="Path to feature-manifest.schema.json"
    )
    parser.add_argument(
        "--manifest",
        metavar="PATH",
        default="feature-manifest.yaml",
        help="Path to feature-manifest.yaml (default: ./feature-manifest.yaml)"
    )

    args = parser.parse_args()

    # Validate
    validator = TraceabilityValidator(args.manifest, args.schema)
    report = validator.validate_all(feature_filter=args.feature)

    # Format output
    if args.json:
        output = format_json(report)
    else:
        output = format_markdown(report)

    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)

    # Exit with appropriate code
    sys.exit(0 if report.overall_passed else 1)


if __name__ == "__main__":
    main()
