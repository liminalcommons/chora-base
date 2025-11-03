#!/usr/bin/env python3
"""
Analyze intrinsic SAP documentation quality.

Focus on documentation completeness, clarity, and structural quality
rather than adoption metrics.
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class QualityIssue:
    """A quality issue found in SAP documentation"""
    severity: str  # critical, warning, info
    category: str  # completeness, clarity, structure, examples
    artifact: str  # which file has the issue
    description: str
    location: Optional[str] = None  # line number or section if known

@dataclass
class SAPQualityReport:
    """Quality assessment for a single SAP"""
    sap_id: str
    sap_name: str
    overall_score: float  # 0-100
    completeness_score: float  # 0-100
    clarity_score: float  # 0-100
    examples_score: float  # 0-100
    structure_score: float  # 0-100
    issues: list[QualityIssue]
    strengths: list[str]

    def to_dict(self):
        return {
            **asdict(self),
            'issues': [asdict(i) for i in self.issues]
        }


class SAPQualityAnalyzer:
    """Analyzes intrinsic SAP documentation quality"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.catalog = self.load_catalog()

    def load_catalog(self) -> dict:
        """Load SAP catalog"""
        catalog_path = self.repo_root / "sap-catalog.json"
        with open(catalog_path) as f:
            data = json.load(f)
            if isinstance(data, dict) and "saps" in data:
                return {sap["id"]: sap for sap in data["saps"]}
            return data

    def analyze_sap(self, sap_id: str) -> SAPQualityReport:
        """Analyze a single SAP's documentation quality"""
        sap = self.catalog.get(sap_id)
        if not sap:
            return self._create_missing_sap_report(sap_id)

        sap_name = sap.get("name", "unknown")
        location = sap.get("location")

        if not location:
            return self._create_missing_sap_report(sap_id, sap_name)

        sap_dir = self.repo_root / location
        if not sap_dir.exists():
            return self._create_missing_sap_report(sap_id, sap_name)

        issues = []
        strengths = []

        # Check each required artifact
        artifacts = {
            "capability-charter.md": "charter",
            "protocol-spec.md": "protocol",
            "awareness-guide.md": "awareness",
            "adoption-blueprint.md": "adoption",
            "ledger.md": "ledger"
        }

        artifact_scores = {}

        for filename, artifact_type in artifacts.items():
            file_path = sap_dir / filename
            if not file_path.exists():
                issues.append(QualityIssue(
                    severity="critical",
                    category="completeness",
                    artifact=filename,
                    description=f"Required artifact {filename} is missing"
                ))
                artifact_scores[artifact_type] = 0
            else:
                score, file_issues, file_strengths = self._analyze_artifact(
                    file_path, artifact_type, filename
                )
                artifact_scores[artifact_type] = score
                issues.extend(file_issues)
                strengths.extend(file_strengths)

        # Calculate scores
        completeness_score = self._calculate_completeness_score(artifact_scores)
        clarity_score = self._calculate_clarity_score(issues)
        examples_score = self._calculate_examples_score(sap_dir, issues, strengths)
        structure_score = self._calculate_structure_score(issues)

        overall_score = (
            completeness_score * 0.35 +
            clarity_score * 0.25 +
            examples_score * 0.20 +
            structure_score * 0.20
        )

        return SAPQualityReport(
            sap_id=sap_id,
            sap_name=sap_name,
            overall_score=overall_score,
            completeness_score=completeness_score,
            clarity_score=clarity_score,
            examples_score=examples_score,
            structure_score=structure_score,
            issues=issues,
            strengths=strengths
        )

    def _analyze_artifact(self, file_path: Path, artifact_type: str, filename: str):
        """Analyze a single artifact file"""
        issues = []
        strengths = []
        score = 100.0

        content = file_path.read_text()
        lines = content.split('\n')
        line_count = len(lines)
        word_count = len(content.split())

        # Check for emptiness
        if line_count < 10:
            issues.append(QualityIssue(
                severity="critical",
                category="completeness",
                artifact=filename,
                description=f"File is too short ({line_count} lines) - likely a stub"
            ))
            return 20.0, issues, strengths

        # Artifact-specific checks
        if artifact_type == "charter":
            score, charter_issues, charter_strengths = self._check_charter(content, filename)
            issues.extend(charter_issues)
            strengths.extend(charter_strengths)

        elif artifact_type == "protocol":
            score, protocol_issues, protocol_strengths = self._check_protocol(content, filename)
            issues.extend(protocol_issues)
            strengths.extend(protocol_strengths)

        elif artifact_type == "awareness":
            score, awareness_issues, awareness_strengths = self._check_awareness(content, filename)
            issues.extend(awareness_issues)
            strengths.extend(awareness_strengths)

        elif artifact_type == "adoption":
            score, adoption_issues, adoption_strengths = self._check_adoption(content, filename)
            issues.extend(adoption_issues)
            strengths.extend(adoption_strengths)

        elif artifact_type == "ledger":
            score, ledger_issues, ledger_strengths = self._check_ledger(content, filename)
            issues.extend(ledger_issues)
            strengths.extend(ledger_strengths)

        # Check for basic markdown structure
        if not re.search(r'^#\s+', content, re.MULTILINE):
            issues.append(QualityIssue(
                severity="warning",
                category="structure",
                artifact=filename,
                description="No H1 heading found - should have a main title"
            ))
            score -= 5

        # Check for reasonable length (not too short or too long)
        if word_count < 200:
            issues.append(QualityIssue(
                severity="warning",
                category="completeness",
                artifact=filename,
                description=f"Very short content ({word_count} words) - may lack detail"
            ))
            score -= 10
        elif word_count > 5000:
            issues.append(QualityIssue(
                severity="info",
                category="clarity",
                artifact=filename,
                description=f"Very long content ({word_count} words) - consider splitting"
            ))

        return max(0, score), issues, strengths

    def _check_charter(self, content: str, filename: str):
        """Check capability charter quality"""
        issues = []
        strengths = []
        score = 100.0

        # Expected sections
        expected_sections = [
            ("problem", "Problem Statement|Problem|What Problem"),
            ("scope", "Scope|What's Included"),
            ("outcome", "Outcomes|Success Criteria|Expected Results"),
            ("stakeholder", "Stakeholders|Who|Users")
        ]

        for section_id, patterns in expected_sections:
            if not re.search(patterns, content, re.IGNORECASE):
                issues.append(QualityIssue(
                    severity="warning",
                    category="completeness",
                    artifact=filename,
                    description=f"Missing or unclear {section_id} section"
                ))
                score -= 15

        # Check for concrete examples
        if re.search(r'```|`\w+`', content):
            strengths.append(f"{filename}: Includes code examples")

        return score, issues, strengths

    def _check_protocol(self, content: str, filename: str):
        """Check protocol specification quality"""
        issues = []
        strengths = []
        score = 100.0

        # Should have technical details
        if not re.search(r'```|class |def |interface |type ', content):
            issues.append(QualityIssue(
                severity="warning",
                category="completeness",
                artifact=filename,
                description="No code blocks or technical definitions found"
            ))
            score -= 20
        else:
            strengths.append(f"{filename}: Contains technical specifications")

        # Should have data models or schemas
        if re.search(r'@dataclass|interface|schema|model', content, re.IGNORECASE):
            strengths.append(f"{filename}: Defines data models")
        else:
            issues.append(QualityIssue(
                severity="info",
                category="completeness",
                artifact=filename,
                description="No explicit data models defined"
            ))
            score -= 10

        # Should have validation commands
        if re.search(r'validation|verify|test|check', content, re.IGNORECASE):
            strengths.append(f"{filename}: Includes validation guidance")
        else:
            issues.append(QualityIssue(
                severity="warning",
                category="completeness",
                artifact=filename,
                description="No validation commands specified"
            ))
            score -= 15

        return score, issues, strengths

    def _check_awareness(self, content: str, filename: str):
        """Check awareness guide quality"""
        issues = []
        strengths = []
        score = 100.0

        # Should mention tools (Read, Write, Edit, Bash, etc.)
        tools = ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
        tool_mentions = sum(1 for tool in tools if tool in content)

        if tool_mentions == 0:
            issues.append(QualityIssue(
                severity="critical",
                category="clarity",
                artifact=filename,
                description="No tool usage instructions (Read, Write, Edit, etc.)"
            ))
            score -= 30
        elif tool_mentions >= 3:
            strengths.append(f"{filename}: Clear tool usage instructions")

        # Should have step-by-step instructions
        numbered_steps = len(re.findall(r'^\d+\.|^- Step|^\d+\)', content, re.MULTILINE))
        if numbered_steps == 0:
            issues.append(QualityIssue(
                severity="warning",
                category="clarity",
                artifact=filename,
                description="No numbered steps or structured procedures"
            ))
            score -= 20
        elif numbered_steps >= 5:
            strengths.append(f"{filename}: Detailed step-by-step instructions")

        return score, issues, strengths

    def _check_adoption(self, content: str, filename: str):
        """Check adoption blueprint quality"""
        issues = []
        strengths = []
        score = 100.0

        # Should have prerequisites
        if not re.search(r'prerequisite|requirement|before you begin|dependencies', content, re.IGNORECASE):
            issues.append(QualityIssue(
                severity="warning",
                category="completeness",
                artifact=filename,
                description="No prerequisites section"
            ))
            score -= 15
        else:
            strengths.append(f"{filename}: Lists prerequisites")

        # Should have numbered installation steps
        numbered_steps = len(re.findall(r'^\d+\.|^## Step \d+', content, re.MULTILINE))
        if numbered_steps < 3:
            issues.append(QualityIssue(
                severity="warning",
                category="clarity",
                artifact=filename,
                description=f"Only {numbered_steps} installation steps - may be incomplete"
            ))
            score -= 15
        elif numbered_steps >= 5:
            strengths.append(f"{filename}: Detailed installation steps")

        # Should have validation
        if not re.search(r'validation|verify|test|confirm', content, re.IGNORECASE):
            issues.append(QualityIssue(
                severity="warning",
                category="completeness",
                artifact=filename,
                description="No validation/verification instructions"
            ))
            score -= 15

        # Should have post-install awareness section (Wave 2 requirement)
        if not re.search(r'post-install.*awareness|awareness.*enablement', content, re.IGNORECASE):
            issues.append(QualityIssue(
                severity="info",
                category="completeness",
                artifact=filename,
                description="No post-install awareness enablement section"
            ))
            score -= 10
        else:
            strengths.append(f"{filename}: Includes post-install awareness enablement")

        return score, issues, strengths

    def _check_ledger(self, content: str, filename: str):
        """Check ledger quality"""
        issues = []
        strengths = []
        score = 100.0

        # Should have version history
        if not re.search(r'version|changelog|history', content, re.IGNORECASE):
            issues.append(QualityIssue(
                severity="warning",
                category="completeness",
                artifact=filename,
                description="No version history section"
            ))
            score -= 20
        else:
            strengths.append(f"{filename}: Maintains version history")

        # Should track adopters
        if not re.search(r'project|adopter|installation|usage', content, re.IGNORECASE):
            issues.append(QualityIssue(
                severity="info",
                category="completeness",
                artifact=filename,
                description="No adoption tracking"
            ))
            score -= 10
        else:
            strengths.append(f"{filename}: Tracks adoption")

        # Should have table format
        if '|' in content and re.search(r'\|.*\|.*\|', content):
            strengths.append(f"{filename}: Uses structured table format")
        else:
            issues.append(QualityIssue(
                severity="info",
                category="structure",
                artifact=filename,
                description="No markdown tables found"
            ))
            score -= 5

        return score, issues, strengths

    def _calculate_completeness_score(self, artifact_scores: dict) -> float:
        """Calculate completeness score from artifact scores"""
        if not artifact_scores:
            return 0.0
        return sum(artifact_scores.values()) / len(artifact_scores)

    def _calculate_clarity_score(self, issues: list) -> float:
        """Calculate clarity score based on clarity issues"""
        clarity_issues = [i for i in issues if i.category == "clarity"]
        critical = sum(1 for i in clarity_issues if i.severity == "critical")
        warnings = sum(1 for i in clarity_issues if i.severity == "warning")

        score = 100.0
        score -= critical * 25
        score -= warnings * 10

        return max(0, score)

    def _calculate_examples_score(self, sap_dir: Path, issues: list, strengths: list) -> float:
        """Calculate examples/templates score"""
        score = 50.0  # Base score

        # Check for templates directory
        if (sap_dir / "templates").exists():
            template_count = len(list((sap_dir / "templates").glob("**/*")))
            score += min(30, template_count * 3)

        # Check for examples in documentation
        example_strengths = [s for s in strengths if "example" in s.lower() or "code" in s.lower()]
        score += len(example_strengths) * 5

        return min(100, score)

    def _calculate_structure_score(self, issues: list) -> float:
        """Calculate structure score"""
        structure_issues = [i for i in issues if i.category == "structure"]
        critical = sum(1 for i in structure_issues if i.severity == "critical")
        warnings = sum(1 for i in structure_issues if i.severity == "warning")

        score = 100.0
        score -= critical * 30
        score -= warnings * 15

        return max(0, score)

    def _create_missing_sap_report(self, sap_id: str, sap_name: str = "unknown") -> SAPQualityReport:
        """Create report for missing SAP"""
        return SAPQualityReport(
            sap_id=sap_id,
            sap_name=sap_name,
            overall_score=0.0,
            completeness_score=0.0,
            clarity_score=0.0,
            examples_score=0.0,
            structure_score=0.0,
            issues=[QualityIssue(
                severity="critical",
                category="completeness",
                artifact="N/A",
                description="SAP not found or not installed"
            )],
            strengths=[]
        )


def main():
    """Analyze all non-React SAPs"""
    repo_root = Path(__file__).parent.parent
    analyzer = SAPQualityAnalyzer(repo_root)

    # Non-React SAPs (SAP-000 through SAP-019, excluding SAP-015 reserved)
    non_react_saps = [f"SAP-{i:03d}" for i in range(20) if i != 15]

    reports = []
    for sap_id in non_react_saps:
        print(f"Analyzing {sap_id}...", end=" ")
        report = analyzer.analyze_sap(sap_id)
        reports.append(report)
        print(f"Score: {report.overall_score:.1f}/100")

    # Output JSON
    output = {
        "analysis_date": "2025-11-02",
        "sap_count": len(reports),
        "reports": [r.to_dict() for r in reports]
    }

    output_file = repo_root / "sap-quality-analysis.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Analysis complete. Results saved to: {output_file}")

    # Print summary
    print("\n" + "="*60)
    print("QUALITY SUMMARY")
    print("="*60)

    avg_score = sum(r.overall_score for r in reports) / len(reports)
    print(f"\nAverage Overall Score: {avg_score:.1f}/100")

    # Group by score ranges
    excellent = [r for r in reports if r.overall_score >= 90]
    good = [r for r in reports if 75 <= r.overall_score < 90]
    fair = [r for r in reports if 60 <= r.overall_score < 75]
    poor = [r for r in reports if r.overall_score < 60]

    print(f"\nExcellent (≥90): {len(excellent)} SAPs")
    print(f"Good (75-89):    {len(good)} SAPs")
    print(f"Fair (60-74):    {len(fair)} SAPs")
    print(f"Poor (<60):      {len(poor)} SAPs")

    # Show SAPs needing attention
    if poor:
        print(f"\n⚠️  SAPs needing attention (score < 60):")
        for r in sorted(poor, key=lambda x: x.overall_score):
            print(f"  - {r.sap_id} ({r.sap_name}): {r.overall_score:.1f}/100")
            critical_issues = [i for i in r.issues if i.severity == "critical"]
            for issue in critical_issues[:2]:  # Show first 2 critical issues
                print(f"    • {issue.description}")

    if fair:
        print(f"\nℹ️  SAPs with room for improvement (score 60-74):")
        for r in sorted(fair, key=lambda x: x.overall_score):
            print(f"  - {r.sap_id} ({r.sap_name}): {r.overall_score:.1f}/100")


if __name__ == "__main__":
    main()
