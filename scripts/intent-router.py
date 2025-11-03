#!/usr/bin/env python3
"""
Conversational Intent Router for chora-base

Translates natural language user input into structured ecosystem actions.
Enables mutual ergonomics: user speaks naturally, system executes procedurally.

Usage:
    python scripts/intent-router.py "show me what's in the inbox"
    python scripts/intent-router.py --interactive
    python scripts/intent-router.py --learn "new phrase" --action inbox_status

Core Capabilities:
- Semantic pattern matching (natural language → formal actions)
- Confidence scoring for disambiguation
- Clarification prompts when ambiguous
- Pattern learning from usage
"""

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class IntentMatch:
    """Represents a matched intent with confidence score."""

    action: str
    confidence: float
    parameters: dict
    pattern_id: str
    clarification: Optional[str] = None


@dataclass
class IntentPattern:
    """Defines a pattern for intent recognition."""

    pattern_id: str
    action: str
    triggers: list[str]  # Natural language phrases that trigger this action
    parameters: dict  # Default parameters for this action
    description: str
    examples: list[str]
    sap_reference: Optional[str] = None


class IntentRouter:
    """Route natural language to procedural actions with confidence scoring."""

    def __init__(self, patterns_file: Path):
        """Initialize router with pattern database."""
        self.patterns_file = patterns_file
        self.patterns = self._load_patterns()
        self.usage_log: list[dict] = []

    def _load_patterns(self) -> list[IntentPattern]:
        """Load intent patterns from YAML database."""
        if not self.patterns_file.exists():
            return self._create_default_patterns()

        with open(self.patterns_file) as f:
            data = yaml.safe_load(f)

        patterns = []
        for p in data.get("patterns", []):
            patterns.append(
                IntentPattern(
                    pattern_id=p["pattern_id"],
                    action=p["action"],
                    triggers=p["triggers"],
                    parameters=p.get("parameters", {}),
                    description=p["description"],
                    examples=p["examples"],
                    sap_reference=p.get("sap_reference"),
                )
            )
        return patterns

    def _create_default_patterns(self) -> list[IntentPattern]:
        """Create default pattern set for bootstrapping."""
        return [
            IntentPattern(
                pattern_id="inbox_status",
                action="run_inbox_status",
                triggers=[
                    "show inbox",
                    "what's in the inbox",
                    "inbox status",
                    "check inbox",
                    "coordination queue",
                    "what's pending",
                ],
                parameters={},
                description="Display inbox status dashboard",
                examples=["What's in the inbox?", "Show me pending coordination requests"],
                sap_reference="SAP-001",
            ),
            IntentPattern(
                pattern_id="sap_quick_check",
                action="run_sap_evaluator_quick",
                triggers=[
                    "how are saps",
                    "sap status",
                    "check saps",
                    "sap adoption",
                    "how's our sap adoption",
                ],
                parameters={"mode": "quick"},
                description="Quick SAP adoption status check",
                examples=["How's our SAP adoption?", "Check SAP status"],
                sap_reference="SAP-019",
            ),
            IntentPattern(
                pattern_id="sap_deep_dive",
                action="run_sap_evaluator_deep",
                triggers=[
                    "deep dive sap",
                    "analyze sap",
                    "sap gaps",
                    "how can we improve sap",
                ],
                parameters={"mode": "deep"},
                description="Deep SAP analysis with gap identification",
                examples=["Deep dive on SAP-004", "How can we improve SAP testing?"],
                sap_reference="SAP-019",
            ),
            IntentPattern(
                pattern_id="coordination_review",
                action="review_coordination_requests",
                triggers=[
                    "review coordination",
                    "check coordination requests",
                    "triage coordination",
                    "what coordination requests",
                ],
                parameters={},
                description="Review incoming coordination requests",
                examples=["Review coordination requests", "What coordination is pending?"],
                sap_reference="SAP-001",
            ),
            IntentPattern(
                pattern_id="create_proposal",
                action="create_strategic_proposal",
                triggers=[
                    "create proposal",
                    "suggest big change",
                    "strategic proposal",
                    "propose new direction",
                ],
                parameters={"type": "strategic_proposal"},
                description="Create strategic proposal (Type 1 intake)",
                examples=["I want to propose a big change", "Create strategic proposal"],
                sap_reference="SAP-001",
            ),
            IntentPattern(
                pattern_id="event_timeline",
                action="show_event_timeline",
                triggers=[
                    "event timeline",
                    "show events",
                    "what happened",
                    "trace events",
                    "show history",
                ],
                parameters={},
                description="Display event timeline from JSONL log",
                examples=["Show me what happened with task-005", "Event timeline for this sprint"],
                sap_reference="SAP-001",
            ),
            IntentPattern(
                pattern_id="suggest_next",
                action="suggest_next_action",
                triggers=[
                    "what next",
                    "what should i do",
                    "suggest next step",
                    "recommend action",
                ],
                parameters={},
                description="Context-aware next action suggestions",
                examples=["What should I work on next?", "What's the next step?"],
                sap_reference=None,
            ),
            IntentPattern(
                pattern_id="search_terminology",
                action="search_glossary",
                triggers=[
                    "what is",
                    "what's a",
                    "define",
                    "explain term",
                    "search glossary",
                ],
                parameters={},
                description="Search ecosystem glossary for terminology",
                examples=["What is a coordination request?", "Define strategic proposal"],
                sap_reference=None,
            ),
            IntentPattern(
                pattern_id="start_task",
                action="start_implementation_task",
                triggers=[
                    "start task",
                    "work on task",
                    "begin task",
                    "start work on",
                ],
                parameters={},
                description="Start implementation task (DDD Phase 3)",
                examples=["Start task-005", "Work on inbox/active/task-007"],
                sap_reference="SAP-012",
            ),
            IntentPattern(
                pattern_id="traceability_help",
                action="explain_traceability",
                triggers=[
                    "traceability",
                    "trace requirements",
                    "link validation",
                    "impact analysis",
                ],
                parameters={},
                description="Explain traceability enhancements and current status",
                examples=["How can we enhance traceability?", "Show me traceability status"],
                sap_reference="SAP-016",
            ),
        ]

    def route(self, user_input: str) -> list[IntentMatch]:
        """
        Route natural language input to structured actions.

        Returns list of matches sorted by confidence (highest first).
        """
        user_input_lower = user_input.lower().strip()
        matches: list[IntentMatch] = []

        for pattern in self.patterns:
            confidence = self._calculate_confidence(user_input_lower, pattern)
            if confidence > 0:
                match = IntentMatch(
                    action=pattern.action,
                    confidence=confidence,
                    parameters=self._extract_parameters(user_input, pattern),
                    pattern_id=pattern.pattern_id,
                    clarification=self._generate_clarification(confidence, pattern),
                )
                matches.append(match)

        # Sort by confidence descending
        matches.sort(key=lambda m: m.confidence, reverse=True)

        # Log usage
        self._log_usage(user_input, matches)

        return matches

    def _calculate_confidence(self, user_input: str, pattern: IntentPattern) -> float:
        """Calculate confidence score for pattern match (0.0 to 1.0)."""
        max_score = 0.0

        for trigger in pattern.triggers:
            trigger_lower = trigger.lower()

            # Exact match: 1.0
            if user_input == trigger_lower:
                return 1.0

            # Contains full trigger: 0.9
            if trigger_lower in user_input:
                max_score = max(max_score, 0.9)
                continue

            # Word overlap scoring
            user_words = set(user_input.split())
            trigger_words = set(trigger_lower.split())

            if not trigger_words:
                continue

            overlap = len(user_words & trigger_words)
            overlap_ratio = overlap / len(trigger_words)

            # High overlap: 0.7-0.85
            if overlap_ratio >= 0.8:
                max_score = max(max_score, 0.85)
            elif overlap_ratio >= 0.6:
                max_score = max(max_score, 0.75)
            elif overlap_ratio >= 0.4:
                max_score = max(max_score, 0.65)
            elif overlap_ratio >= 0.2:
                max_score = max(max_score, 0.5)

        return max_score

    def _extract_parameters(self, user_input: str, pattern: IntentPattern) -> dict:
        """Extract parameters from user input based on pattern."""
        params = pattern.parameters.copy()

        # Extract SAP ID if mentioned
        sap_match = re.search(r"sap[- ]?(\d+)", user_input.lower())
        if sap_match:
            params["sap_id"] = f"SAP-{sap_match.group(1).zfill(3)}"

        # Extract task ID if mentioned
        task_match = re.search(r"task[- ]?(\d+)", user_input.lower())
        if task_match:
            params["task_id"] = f"task-{task_match.group(1).zfill(3)}"

        # Extract coordination ID if mentioned
        coord_match = re.search(r"coord[- ]?(\d+)", user_input.lower())
        if coord_match:
            params["coord_id"] = f"coord-{coord_match.group(1).zfill(3)}"

        # Extract trace ID if mentioned
        trace_match = re.search(r"trace[- ]?id:?\s*([a-z0-9-]+)", user_input.lower())
        if trace_match:
            params["trace_id"] = trace_match.group(1)

        return params

    def _generate_clarification(self, confidence: float, pattern: IntentPattern) -> Optional[str]:
        """Generate clarification prompt if confidence is low."""
        if confidence < 0.7:
            return f"Did you mean: {pattern.description}? (Confidence: {confidence:.0%})"
        return None

    def _log_usage(self, user_input: str, matches: list[IntentMatch]) -> None:
        """Log usage for pattern learning."""
        self.usage_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "top_match": asdict(matches[0]) if matches else None,
                "all_matches": len(matches),
            }
        )

    def learn_pattern(self, user_input: str, action: str) -> None:
        """Learn new pattern from user feedback."""
        # Find existing pattern for this action
        pattern = next((p for p in self.patterns if p.action == action), None)

        if pattern:
            # Add trigger if not already present
            if user_input.lower() not in [t.lower() for t in pattern.triggers]:
                pattern.triggers.append(user_input.lower())
                self._save_patterns()
        else:
            print(f"Warning: Action '{action}' not found in pattern database")

    def _save_patterns(self) -> None:
        """Save patterns back to YAML file."""
        data = {
            "patterns": [
                {
                    "pattern_id": p.pattern_id,
                    "action": p.action,
                    "triggers": p.triggers,
                    "parameters": p.parameters,
                    "description": p.description,
                    "examples": p.examples,
                    "sap_reference": p.sap_reference,
                }
                for p in self.patterns
            ]
        }

        with open(self.patterns_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def export_usage_log(self, output_file: Path) -> None:
        """Export usage log for analysis."""
        with open(output_file, "w") as f:
            json.dump(self.usage_log, f, indent=2)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Route natural language input to chora-base actions"
    )
    parser.add_argument("input", nargs="?", help="Natural language input to route")
    parser.add_argument(
        "--patterns",
        type=Path,
        default=Path("docs/dev-docs/patterns/INTENT_PATTERNS.yaml"),
        help="Path to intent patterns database",
    )
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--learn", help="Learn new pattern for phrase")
    parser.add_argument("--action", help="Action to associate with learned phrase")
    parser.add_argument("--export-usage", type=Path, help="Export usage log to file")
    parser.add_argument("--init", action="store_true", help="Initialize pattern database")

    args = parser.parse_args()

    # Initialize pattern database if requested
    if args.init:
        router = IntentRouter(args.patterns)
        router._save_patterns()
        print(f"✅ Initialized pattern database at {args.patterns}")
        print(f"   Patterns: {len(router.patterns)}")
        return

    # Create router
    router = IntentRouter(args.patterns)

    # Learn mode
    if args.learn and args.action:
        router.learn_pattern(args.learn, args.action)
        print(f"✅ Learned: '{args.learn}' → {args.action}")
        return

    # Export usage log
    if args.export_usage:
        router.export_usage_log(args.export_usage)
        print(f"✅ Exported usage log to {args.export_usage}")
        return

    # Interactive mode
    if args.interactive:
        print("Interactive Intent Router (type 'quit' to exit)")
        print("=" * 60)
        while True:
            try:
                user_input = input("\n> ").strip()
                if user_input.lower() in ["quit", "exit", "q"]:
                    break
                if not user_input:
                    continue

                matches = router.route(user_input)
                display_matches(matches)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break
        return

    # Single input mode
    if args.input:
        matches = router.route(args.input)
        display_matches(matches)
    else:
        parser.print_help()


def display_matches(matches: list[IntentMatch]) -> None:
    """Display matched intents in readable format."""
    if not matches:
        print("❌ No matching intent found")
        return

    top_match = matches[0]

    # High confidence: execute suggestion
    if top_match.confidence >= 0.7:
        print(f"✅ Matched: {top_match.action}")
        print(f"   Confidence: {top_match.confidence:.0%}")
        if top_match.parameters:
            print(f"   Parameters: {json.dumps(top_match.parameters, indent=6)}")
        print(f"\n📋 Next: Execute action or type 'help {top_match.action}' for details")

    # Medium confidence: clarification needed
    elif top_match.confidence >= 0.5:
        print(f"⚠️  Possible match: {top_match.action}")
        print(f"   Confidence: {top_match.confidence:.0%}")
        print(f"   {top_match.clarification}")
        if len(matches) > 1:
            print("\n   Other possibilities:")
            for m in matches[1:4]:  # Show top 3 alternatives
                print(f"   - {m.action} ({m.confidence:.0%})")

    # Low confidence: show options
    else:
        print("🤔 Did you mean one of these?")
        for i, m in enumerate(matches[:5], 1):
            print(f"   {i}. {m.action} ({m.confidence:.0%})")
        print("\n   Type number to select or rephrase your request")


if __name__ == "__main__":
    main()
