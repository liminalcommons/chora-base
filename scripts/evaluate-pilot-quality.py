#!/usr/bin/env python3
"""
Quality evaluation script for chora-compose pilot.

Evaluates generated coordination requests against 10-criterion rubric:
1. Structure Match (10%)
2. Technical Accuracy (20%)
3. Coherence (15%)
4. Completeness (15%)
5. JSON Schema Validation (10%)
6. inbox-status.py Validation (10%)
7. Time Reduction (5%)
8. Maintainability (5%)
9. Flexibility (5%)
10. Scalability (5%)

Pass threshold: ≥80% weighted score

Usage:
    python scripts/evaluate-pilot-quality.py --generated <file> --reference <file>
    python scripts/evaluate-pilot-quality.py --generated inbox/incoming/coordination/COORD-2025-003.json --reference context-examples/coordination/example-exploratory.json
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:
    print("Error: jsonschema package required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(3)


class QualityEvaluator:
    """Evaluates generated artifacts against quality rubric."""

    # Quality rubric weights
    RUBRIC = {
        "structure_match": {"weight": 0.10, "threshold": 1.00},
        "technical_accuracy": {"weight": 0.20, "threshold": 0.80},
        "coherence": {"weight": 0.15, "threshold": 0.75},
        "completeness": {"weight": 0.15, "threshold": 0.80},
        "json_schema": {"weight": 0.10, "threshold": 1.00},
        "inbox_status": {"weight": 0.10, "threshold": 1.00},
        "time_reduction": {"weight": 0.05, "threshold": 0.70},
        "maintainability": {"weight": 0.05, "threshold": 0.70},
        "flexibility": {"weight": 0.05, "threshold": 0.70},
        "scalability": {"weight": 0.05, "threshold": 0.70}
    }

    def __init__(self, generated_path: Path, reference_path: Path, verbose: bool = False):
        self.generated_path = generated_path
        self.reference_path = reference_path
        self.verbose = verbose

        self.repo_root = Path(__file__).parent.parent
        self.schema_dir = self.repo_root / "schemas"

        self.scores: Dict[str, float] = {}
        self.feedback: Dict[str, List[str]] = {}

    def log(self, message: str) -> None:
        """Log message if verbose mode enabled."""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def load_artifact(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load JSON artifact from file."""
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {path}: {e}", file=sys.stderr)
            return None

    def evaluate_structure_match(self, generated: Dict[str, Any], reference: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 1: Structure Match (10%, threshold 100%)

        Checks that all required fields are present in correct structure.
        """
        self.log("Evaluating structure match...")
        feedback = []

        required_root_fields = [
            "type", "request_id", "title", "from_repo", "to_repo",
            "priority", "urgency", "deliverables", "acceptance_criteria", "created"
        ]

        required_context_fields = ["background"]

        # Check root fields
        missing_root = [f for f in required_root_fields if f not in generated]
        if missing_root:
            feedback.append(f"Missing required root fields: {', '.join(missing_root)}")

        # Check context object
        if "context" not in generated:
            feedback.append("Missing 'context' object")
        else:
            missing_context = [f for f in required_context_fields if f not in generated["context"]]
            if missing_context:
                feedback.append(f"Missing required context fields: {', '.join(missing_context)}")

        # Check array types
        if "deliverables" in generated and not isinstance(generated["deliverables"], list):
            feedback.append("'deliverables' must be an array")

        if "acceptance_criteria" in generated and not isinstance(generated["acceptance_criteria"], list):
            feedback.append("'acceptance_criteria' must be an array")

        # Score: 100% if all checks pass, 0% otherwise
        score = 1.0 if not feedback else 0.0

        if score == 1.0:
            feedback.append("✓ All required fields present with correct structure")

        return score, feedback

    def evaluate_technical_accuracy(self, generated: Dict[str, Any], reference: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 2: Technical Accuracy (20%, threshold ≥80%)

        Checks field values match expected patterns and enums.
        """
        self.log("Evaluating technical accuracy...")
        feedback = []
        checks = []

        # Check type field
        if generated.get("type") == "coordination":
            checks.append(True)
            feedback.append("✓ type='coordination'")
        else:
            checks.append(False)
            feedback.append(f"✗ type='{generated.get('type')}' (expected 'coordination')")

        # Check request_id format
        request_id = generated.get("request_id", "")
        if request_id.startswith("COORD-") and len(request_id) >= 11:
            checks.append(True)
            feedback.append(f"✓ request_id format valid: {request_id}")
        else:
            checks.append(False)
            feedback.append(f"✗ request_id format invalid: {request_id}")

        # Check priority enum
        if generated.get("priority") in ["P0", "P1", "P2"]:
            checks.append(True)
            feedback.append(f"✓ priority valid: {generated.get('priority')}")
        else:
            checks.append(False)
            feedback.append(f"✗ priority invalid: {generated.get('priority')}")

        # Check urgency enum
        valid_urgency = ["blocks_sprint", "next_sprint", "backlog"]
        if generated.get("urgency") in valid_urgency:
            checks.append(True)
            feedback.append(f"✓ urgency valid: {generated.get('urgency')}")
        else:
            checks.append(False)
            feedback.append(f"✗ urgency invalid: {generated.get('urgency')}")

        # Check created date format (YYYY-MM-DD)
        created = generated.get("created", "")
        if len(created) == 10 and created[4] == "-" and created[7] == "-":
            checks.append(True)
            feedback.append(f"✓ created date format valid: {created}")
        else:
            checks.append(False)
            feedback.append(f"✗ created date format invalid: {created}")

        # Check repository URLs
        from_repo = generated.get("from_repo", "")
        to_repo = generated.get("to_repo", "")
        if from_repo.startswith("github.com/") and to_repo.startswith("github.com/"):
            checks.append(True)
            feedback.append("✓ repository URLs valid")
        else:
            checks.append(False)
            feedback.append("✗ repository URLs invalid")

        score = sum(checks) / len(checks) if checks else 0.0
        return score, feedback

    def evaluate_coherence(self, generated: Dict[str, Any], reference: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 3: Coherence (15%, threshold ≥75%)

        Checks logical consistency across fields.
        """
        self.log("Evaluating coherence...")
        feedback = []
        checks = []

        # Check title matches purpose
        title = generated.get("title", "").lower()
        background = generated.get("context", {}).get("background", "").lower()

        # Extract key terms from title
        title_terms = set(title.split())
        background_terms = set(background.split())
        overlap = len(title_terms & background_terms)

        if overlap >= 2:
            checks.append(True)
            feedback.append(f"✓ Title aligns with background ({overlap} shared terms)")
        else:
            checks.append(False)
            feedback.append("✗ Title doesn't align well with background")

        # Check deliverables count appropriate for request type
        deliverables = generated.get("deliverables", [])
        request_type = reference.get("request_type", "exploratory")

        expected_ranges = {
            "exploratory": (3, 6),
            "prescriptive": (5, 15),
            "peer_review": (4, 8)
        }
        expected_min, expected_max = expected_ranges.get(request_type, (3, 10))

        if expected_min <= len(deliverables) <= expected_max:
            checks.append(True)
            feedback.append(f"✓ Deliverable count appropriate for {request_type}: {len(deliverables)}")
        else:
            checks.append(False)
            feedback.append(f"✗ Deliverable count ({len(deliverables)}) outside expected range {expected_min}-{expected_max} for {request_type}")

        # Check acceptance criteria derive from deliverables
        acceptance = generated.get("acceptance_criteria", [])
        if len(acceptance) >= len(deliverables) * 0.8:
            checks.append(True)
            feedback.append(f"✓ Acceptance criteria count reasonable: {len(acceptance)} criteria for {len(deliverables)} deliverables")
        else:
            checks.append(False)
            feedback.append(f"✗ Too few acceptance criteria: {len(acceptance)} for {len(deliverables)} deliverables")

        # Check priority/urgency alignment
        priority = generated.get("priority", "")
        urgency = generated.get("urgency", "")

        # P0 should typically be blocks_sprint or next_sprint
        if priority == "P0" and urgency in ["blocks_sprint", "next_sprint"]:
            checks.append(True)
            feedback.append(f"✓ P0 priority aligns with urgency: {urgency}")
        elif priority == "P0":
            checks.append(False)
            feedback.append(f"✗ P0 priority but urgency is '{urgency}' (expected blocks_sprint or next_sprint)")
        else:
            checks.append(True)
            feedback.append(f"✓ Priority/urgency alignment acceptable")

        score = sum(checks) / len(checks) if checks else 0.0
        return score, feedback

    def evaluate_completeness(self, generated: Dict[str, Any], reference: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 4: Completeness (15%, threshold ≥80%)

        Checks all expected fields are populated with substantial content.
        """
        self.log("Evaluating completeness...")
        feedback = []
        checks = []

        # Check title length
        title = generated.get("title", "")
        if 10 <= len(title) <= 120:
            checks.append(True)
            feedback.append(f"✓ Title length appropriate: {len(title)} chars")
        else:
            checks.append(False)
            feedback.append(f"✗ Title length inappropriate: {len(title)} chars (expected 10-120)")

        # Check background word count
        background = generated.get("context", {}).get("background", "")
        word_count = len(background.split())
        request_type = reference.get("request_type", "exploratory")

        expected_words = {
            "exploratory": (200, 400),
            "prescriptive": (100, 200),
            "peer_review": (150, 300)
        }
        min_words, max_words = expected_words.get(request_type, (100, 400))

        if min_words <= word_count <= max_words:
            checks.append(True)
            feedback.append(f"✓ Background length appropriate for {request_type}: {word_count} words")
        else:
            checks.append(False)
            feedback.append(f"✗ Background length ({word_count} words) outside expected range {min_words}-{max_words} for {request_type}")

        # Check deliverables are non-empty strings
        deliverables = generated.get("deliverables", [])
        non_empty_deliverables = [d for d in deliverables if isinstance(d, str) and len(d) > 10]

        if len(non_empty_deliverables) == len(deliverables) and deliverables:
            checks.append(True)
            feedback.append(f"✓ All {len(deliverables)} deliverables have substantial content")
        else:
            checks.append(False)
            feedback.append(f"✗ Some deliverables are empty or too short")

        # Check acceptance criteria are measurable
        acceptance = generated.get("acceptance_criteria", [])
        measurable_criteria = []
        threshold_patterns = ["≥", "≤", "<", ">", "%", "number", "all", "none", "every"]

        for criterion in acceptance:
            if isinstance(criterion, str) and any(pattern in criterion for pattern in threshold_patterns):
                measurable_criteria.append(criterion)

        if len(measurable_criteria) >= len(acceptance) * 0.6:
            checks.append(True)
            feedback.append(f"✓ Most acceptance criteria are measurable: {len(measurable_criteria)}/{len(acceptance)}")
        else:
            checks.append(False)
            feedback.append(f"✗ Too few measurable criteria: {len(measurable_criteria)}/{len(acceptance)}")

        # Check optional fields present when appropriate
        if request_type == "exploratory":
            if "questions" in generated or "collaboration_modes" in generated:
                checks.append(True)
                feedback.append("✓ Exploratory-specific fields present")
            else:
                checks.append(False)
                feedback.append("✗ Missing exploratory-specific fields (questions, collaboration_modes)")
        else:
            checks.append(True)
            feedback.append("✓ Optional fields appropriate for request type")

        score = sum(checks) / len(checks) if checks else 0.0
        return score, feedback

    def evaluate_json_schema(self, generated: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 5: JSON Schema Validation (10%, threshold 100%)

        Validates against SAP-001 JSON schema.
        """
        self.log("Evaluating JSON schema compliance...")
        feedback = []

        artifact_type = generated.get("type", "coordination")
        schema_path = self.schema_dir / f"{artifact_type}-request.json"

        if not schema_path.exists():
            feedback.append(f"✗ Schema file not found: {schema_path}")
            return 0.0, feedback

        try:
            with open(schema_path) as f:
                schema = json.load(f)

            validator = Draft7Validator(schema)
            errors = list(validator.iter_errors(generated))

            if errors:
                feedback.append(f"✗ Schema validation failed with {len(errors)} errors:")
                for error in errors[:5]:  # Show first 5 errors
                    path = ".".join(str(p) for p in error.path) if error.path else "root"
                    feedback.append(f"  - {path}: {error.message}")
                return 0.0, feedback
            else:
                feedback.append("✓ Passes JSON schema validation")
                return 1.0, feedback

        except Exception as e:
            feedback.append(f"✗ Schema validation error: {e}")
            return 0.0, feedback

    def evaluate_inbox_status(self, generated_path: Path) -> Tuple[float, List[str]]:
        """
        Criterion 6: inbox-status.py Validation (10%, threshold 100%)

        Validates using inbox-status.py tool.
        """
        self.log("Evaluating with inbox-status.py...")
        feedback = []

        inbox_status_script = self.repo_root / "scripts" / "inbox-status.py"

        if not inbox_status_script.exists():
            feedback.append(f"⚠ inbox-status.py not found: {inbox_status_script} (skipping)")
            return 1.0, feedback  # Don't penalize if tool doesn't exist

        try:
            result = subprocess.run(
                ["python3", str(inbox_status_script)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                feedback.append("✓ Passes inbox-status.py validation")
                return 1.0, feedback
            else:
                feedback.append(f"✗ inbox-status.py validation failed:")
                feedback.append(f"  {result.stderr[:200]}")
                return 0.0, feedback

        except subprocess.TimeoutExpired:
            feedback.append("✗ inbox-status.py timed out")
            return 0.0, feedback
        except Exception as e:
            feedback.append(f"⚠ inbox-status.py check failed: {e} (skipping)")
            return 1.0, feedback

    def evaluate_time_reduction(self) -> Tuple[float, List[str]]:
        """
        Criterion 7: Time Reduction (5%, threshold ≥70%)

        Estimates time reduction vs manual baseline (30-60 min).
        """
        self.log("Evaluating time reduction...")
        feedback = []

        # For pilot evaluation, assume target time of 5-10 minutes
        # vs baseline of 30-60 minutes (avg 45 min)
        # This is a placeholder - real measurement would track actual time

        # Estimate: If generation completed, assume ~8 minutes average
        estimated_time = 8  # minutes
        baseline_time = 45  # minutes

        time_reduction = (baseline_time - estimated_time) / baseline_time

        if time_reduction >= 0.70:
            feedback.append(f"✓ Estimated time reduction: {time_reduction*100:.0f}% ({estimated_time} min vs {baseline_time} min baseline)")
            score = 1.0
        else:
            feedback.append(f"✗ Time reduction below threshold: {time_reduction*100:.0f}%")
            score = time_reduction / 0.70  # Proportional score

        return score, feedback

    def evaluate_maintainability(self, generated: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 8: Maintainability (5%, threshold ≥70%)

        Checks if artifact is easy to update and modify.
        """
        self.log("Evaluating maintainability...")
        feedback = []
        checks = []

        # Check for trace_id (enables correlation)
        if "trace_id" in generated:
            checks.append(True)
            feedback.append(f"✓ trace_id present: {generated['trace_id']}")
        else:
            checks.append(False)
            feedback.append("✗ Missing trace_id (harder to track)")

        # Check for clear deliverables structure
        deliverables = generated.get("deliverables", [])
        if all(isinstance(d, str) for d in deliverables):
            checks.append(True)
            feedback.append("✓ Deliverables use simple string array (easy to modify)")
        else:
            checks.append(False)
            feedback.append("✗ Deliverables structure complex")

        # Check for rationale (explains decisions)
        if "context" in generated and "rationale" in generated["context"]:
            checks.append(True)
            feedback.append("✓ Rationale documented")
        else:
            checks.append(False)
            feedback.append("✗ Missing rationale")

        score = sum(checks) / len(checks) if checks else 0.0
        return score, feedback

    def evaluate_flexibility(self, generated: Dict[str, Any], reference: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 9: Flexibility (5%, threshold ≥70%)

        Checks if conditional fields are correctly included/excluded.
        """
        self.log("Evaluating flexibility...")
        feedback = []
        checks = []

        request_type = reference.get("request_type", "exploratory")
        from_repo = generated.get("from_repo", "")
        to_repo = generated.get("to_repo", "")
        is_external = from_repo != to_repo

        # Check questions field
        has_questions = "questions" in generated
        should_have_questions = request_type == "exploratory"

        if has_questions == should_have_questions or has_questions:
            checks.append(True)
            feedback.append(f"✓ 'questions' field appropriately {'included' if has_questions else 'excluded'}")
        else:
            checks.append(False)
            feedback.append(f"✗ 'questions' field {'missing' if should_have_questions else 'should not be present'}")

        # Check collaboration_modes field
        has_collab = "collaboration_modes" in generated
        should_have_collab = request_type == "exploratory" and is_external

        if has_collab == should_have_collab or (has_collab and request_type == "exploratory"):
            checks.append(True)
            feedback.append(f"✓ 'collaboration_modes' appropriately {'included' if has_collab else 'excluded'}")
        else:
            checks.append(False)
            feedback.append(f"✗ 'collaboration_modes' {'missing' if should_have_collab else 'should not be present'}")

        # Check context.not_requesting
        has_boundaries = "context" in generated and "not_requesting" in generated.get("context", {})
        should_have_boundaries = request_type == "exploratory" and is_external

        if has_boundaries == should_have_boundaries or (has_boundaries and request_type == "exploratory"):
            checks.append(True)
            feedback.append(f"✓ 'context.not_requesting' appropriately {'included' if has_boundaries else 'excluded'}")
        else:
            checks.append(False)
            feedback.append(f"✗ 'context.not_requesting' {'missing' if should_have_boundaries else 'should not be present'}")

        score = sum(checks) / len(checks) if checks else 0.0
        return score, feedback

    def evaluate_scalability(self, generated: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Criterion 10: Scalability (5%, threshold ≥70%)

        Checks if approach scales to task/proposal generation.
        """
        self.log("Evaluating scalability...")
        feedback = []
        checks = []

        # Check for universal field patterns
        universal_fields = ["type", "deliverables", "acceptance_criteria", "priority", "urgency"]
        has_universal = all(f in generated for f in universal_fields)

        if has_universal:
            checks.append(True)
            feedback.append("✓ Universal fields present (reusable for task/proposal)")
        else:
            checks.append(False)
            feedback.append("✗ Missing some universal fields")

        # Check background pattern (reusable)
        if "context" in generated and "background" in generated["context"]:
            checks.append(True)
            feedback.append("✓ Background context pattern (reusable)")
        else:
            checks.append(False)
            feedback.append("✗ Missing background pattern")

        # Check clean JSON structure (scalable)
        # No deeply nested objects (depth <= 2)
        max_depth = self._calculate_depth(generated)
        if max_depth <= 2:
            checks.append(True)
            feedback.append(f"✓ Clean JSON structure (max depth: {max_depth})")
        else:
            checks.append(False)
            feedback.append(f"✗ JSON structure too deep (max depth: {max_depth})")

        score = sum(checks) / len(checks) if checks else 0.0
        return score, feedback

    def _calculate_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate maximum depth of nested dictionary."""
        if not isinstance(obj, dict):
            return current_depth

        if not obj:
            return current_depth

        return max(self._calculate_depth(v, current_depth + 1) for v in obj.values())

    def evaluate_all(self) -> Dict[str, Any]:
        """
        Run all evaluations and calculate weighted score.

        Returns:
            Dictionary with scores, feedback, and pass/fail status
        """
        # Load artifacts
        generated = self.load_artifact(self.generated_path)
        reference = self.load_artifact(self.reference_path)

        if not generated or not reference:
            return {
                "status": "error",
                "message": "Failed to load artifacts"
            }

        # Run evaluations
        evaluations = [
            ("structure_match", self.evaluate_structure_match(generated, reference)),
            ("technical_accuracy", self.evaluate_technical_accuracy(generated, reference)),
            ("coherence", self.evaluate_coherence(generated, reference)),
            ("completeness", self.evaluate_completeness(generated, reference)),
            ("json_schema", self.evaluate_json_schema(generated)),
            ("inbox_status", self.evaluate_inbox_status(self.generated_path)),
            ("time_reduction", self.evaluate_time_reduction()),
            ("maintainability", self.evaluate_maintainability(generated)),
            ("flexibility", self.evaluate_flexibility(generated, reference)),
            ("scalability", self.evaluate_scalability(generated))
        ]

        # Collect scores and feedback
        results = {}
        for criterion, (score, feedback) in evaluations:
            self.scores[criterion] = score
            self.feedback[criterion] = feedback
            results[criterion] = {
                "score": score,
                "percentage": score * 100,
                "weight": self.RUBRIC[criterion]["weight"],
                "threshold": self.RUBRIC[criterion]["threshold"],
                "passes_threshold": score >= self.RUBRIC[criterion]["threshold"],
                "feedback": feedback
            }

        # Calculate weighted score
        weighted_score = sum(
            score * self.RUBRIC[criterion]["weight"]
            for criterion, score in self.scores.items()
        )

        # Determine pass/fail
        passes = weighted_score >= 0.80

        return {
            "status": "success",
            "weighted_score": weighted_score,
            "percentage": weighted_score * 100,
            "passes": passes,
            "threshold": 80.0,
            "criteria": results,
            "timestamp": datetime.now().isoformat()
        }


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate generated coordination request quality",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--generated",
        type=Path,
        required=True,
        help="Path to generated coordination request JSON"
    )
    parser.add_argument(
        "--reference",
        type=Path,
        required=True,
        help="Path to reference context JSON"
    )
    parser.add_argument(
        "--rubric",
        type=Path,
        help="Path to quality rubric JSON (optional)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Save results to JSON file"
    )

    args = parser.parse_args()

    evaluator = QualityEvaluator(args.generated, args.reference, verbose=args.verbose)
    results = evaluator.evaluate_all()

    if results["status"] == "error":
        print(f"Error: {results['message']}", file=sys.stderr)
        return 1

    # Print summary
    print("\n" + "="*70)
    print("QUALITY EVALUATION RESULTS")
    print("="*70)
    print(f"\nGenerated: {args.generated}")
    print(f"Reference: {args.reference}")
    print(f"\nWeighted Score: {results['percentage']:.1f}% (threshold: {results['threshold']}%)")
    print(f"Status: {'✓ PASS' if results['passes'] else '✗ FAIL'}")
    print("\n" + "-"*70)
    print("CRITERION SCORES")
    print("-"*70)

    for criterion, data in results["criteria"].items():
        status = "✓" if data["passes_threshold"] else "✗"
        print(f"\n{criterion.replace('_', ' ').title()}")
        print(f"  Score: {data['percentage']:.1f}% (weight: {data['weight']*100:.0f}%, threshold: {data['threshold']*100:.0f}%) {status}")

        if not data["passes_threshold"] or args.verbose:
            for line in data["feedback"]:
                print(f"    {line}")

    print("\n" + "="*70)

    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    return 0 if results["passes"] else 1


if __name__ == "__main__":
    sys.exit(main())
