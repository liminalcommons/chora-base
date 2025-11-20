#!/usr/bin/env python3
"""
unified-discovery.py

Intelligent discovery routing system for chora-workspace.
Routes queries to optimal discovery method based on query type.

Part of FEAT-002 (Unified Traceability & Discovery System).

Usage:
    python scripts/unified-discovery.py "show me authentication code"
    python scripts/unified-discovery.py "how do we handle async testing?" --format json
    python scripts/unified-discovery.py "when did we complete SAP-015 L4?"
    python scripts/unified-discovery.py "how do I run SAP metrics?"

Query Types:
    1. Code/Feature: "show me X code", "implementation of Y"
       → Routes to feature manifest (5-8k tokens)

    2. Pattern/Concept: "how do we X", "best practice for Y"
       → Routes to knowledge graph (10-15k tokens)

    3. Historical/Event: "when did X", "previous work on Y"
       → Routes to event logs (8-12k tokens)

    4. Automation/Recipe: "how do I run X", "recipe for Y"
       → Routes to justfile (1-5k tokens)
"""

import argparse
import yaml
import json
import re
import subprocess
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from difflib import SequenceMatcher
import sys

# Windows UTF-8 console support (chora-base cross-platform requirement)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# --- Synonym Mappings and Fuzzy Matching ---

# Synonym mappings for SAP vocabulary (expanded from OPP-2025-003)
SAP_SYNONYMS = {
    # Core concepts
    "testing": ["test", "tests", "tdd", "bdd", "coverage", "jest", "pytest", "validation"],
    "automation": ["automate", "script", "recipe", "justfile", "workflow", "pipeline"],
    "docker": ["container", "containerization", "dockerfile", "compose"],
    "documentation": ["docs", "doc", "readme", "guide", "how-to", "reference"],
    "memory": ["event", "events", "logging", "amem", "trace", "history"],
    "knowledge": ["note", "notes", "wikilink", "pattern", "concept"],
    "ci": ["cicd", "ci/cd", "github-actions", "workflow", "pipeline", "continuous"],
    "quality": ["lint", "linting", "format", "formatting", "gate", "husky", "standard"],
    "traceability": ["trace", "link", "manifest", "requirement", "tracking"],
    "governance": ["proposal", "amendment", "permission", "approval", "sap"],
    # Actions
    "debug": ["fix", "bug", "troubleshoot", "diagnose", "repair"],
    "implement": ["add", "create", "build", "develop", "code"],
    "check": ["verify", "validate", "inspect", "status", "query"],
    "run": ["execute", "start", "launch", "invoke"],
    # Packages
    "castalia": ["game", "multiplayer", "colyseus", "phaser"],
    "compose": ["chora-compose", "orchestration", "content", "mcp"],
    "beads": ["task", "issue", "tracking", "todo"],
}

# Minimum fuzzy match ratio (0.0 - 1.0)
FUZZY_THRESHOLD = 0.8  # Stricter than 0.7 for better precision

# Confidence threshold for routing (OPP-2025-005 Priority 1)
# If max pattern score < threshold, route to UNKNOWN
CONFIDENCE_THRESHOLD = 0.3

# Negative patterns for UNKNOWN routing (OPP-2025-005 Priority 1)
# Queries matching these patterns should route to UNKNOWN
NEGATIVE_PATTERNS = {
    # Gibberish detection
    r'^[a-z]{3,}[0-9]{3,}$',  # e.g., "xyz123", "abc456"
    r'\b(asdf|qwerty|lorem|ipsum|gibberish|random)\b',

    # Philosophical queries
    r'\b(meaning of life|what is truth|purpose of existence|why are we here)\b',
    r'\b(philosophy|existential|metaphysical)\b.*\b(question|query|answer)\b',

    # Destructive commands
    r'\b(delete everything|remove all|destroy|wipe|erase all)\b',
    r'\brm\s+-rf\b',
    r'\b(drop|truncate)\s+(database|table|all)\b',
}

def fuzzy_match_keyword(keyword: str, text: str) -> Tuple[bool, float]:
    """
    Check if keyword fuzzy matches any word in text.

    Returns:
        (matched, ratio): Whether match found and best ratio
    """
    words = set(re.findall(r'\w+', text.lower()))

    # Exact match
    if keyword in words:
        return (True, 1.0)

    # Fuzzy match
    best_ratio = 0.0
    for word in words:
        ratio = SequenceMatcher(None, keyword, word).ratio()
        if ratio >= FUZZY_THRESHOLD:
            return (True, ratio)
        best_ratio = max(best_ratio, ratio)

    return (False, best_ratio)

def expand_keywords(keywords: Set[str]) -> Set[str]:
    """Expand keywords using SAP synonym mappings."""
    expanded = set(keywords)

    for kw in keywords:
        # Check if keyword is a key in synonyms
        if kw in SAP_SYNONYMS:
            expanded.update(SAP_SYNONYMS[kw])

        # Check if keyword matches any synonym values
        for key, synonyms in SAP_SYNONYMS.items():
            if kw in synonyms:
                expanded.add(key)
                expanded.update(synonyms)

    return expanded

# --- Query Type Classification ---

class QueryType(Enum):
    """Types of discovery queries."""
    CODE_FEATURE = "code_feature"
    PATTERN_CONCEPT = "pattern_concept"
    HISTORICAL_EVENT = "historical_event"
    AUTOMATION_RECIPE = "automation_recipe"
    UNKNOWN = "unknown"

# Query patterns for classification
# OPP-2025-005 Priority 2: Added weighted patterns for better disambiguation
# Format: (pattern, weight)
# - Weight 3.0: Strong signals (definitive intent)
# - Weight 2.0: Medium signals (likely intent)
# - Weight 1.0: Weak signals (possible intent)
QUERY_PATTERNS = {
    QueryType.CODE_FEATURE: [
        # Strong CODE signals (show me X code/docs/file)
        (r'\b(show me|where is|find|locate|get)\b.*\b(code|implementation|file|documentation|docs)\b', 3.0),
        # Medium CODE signals (feature keywords)
        (r'\b(feature|code|implementation|function|class|API|module|component|file)\b', 2.0),
        (r'\b(documentation|docs|readme)\b', 2.0),  # Documentation is often about code
        (r'\b(metrics|statistics|stats|dashboard)\b', 2.0),  # Metrics often refer to code features
        (r'\bauth(entication|orization)?\b', 2.0),
        (r'\b(login|signup|database|api|endpoint)\b', 2.0),
    ],
    QueryType.PATTERN_CONCEPT: [
        # Strong PATTERN signals (OPP-2025-005 Priority 2)
        (r'\b(how do we|what patterns|best practice)\b', 3.0),
        (r'\b(explain|understand) (?:our|the) \w+\b', 3.0),
        # Medium PATTERN signals
        (r'\b(pattern|approach|strategy|guideline)\b', 2.0),
        (r'\b(design|architecture|methodology|workflow)\b', 2.0),
        (r'\b(explain|understand|learn|concept)\b', 2.0),
    ],
    QueryType.HISTORICAL_EVENT: [
        # Strong HISTORICAL signals (OPP-2025-005 Priority 3)
        (r'\b(when did|when was)\b', 3.0),  # Increased from 2.0
        (r'\b(history|previous work|timeline|chronology)\b', 2.0),
        # Past tense verbs (OPP-2025-005 Priority 3)
        (r'\b(completed|delivered|fixed|deployed|finished|implemented|adopted|merged)\b', 2.5),
        (r'\b(past|sprint|sequence|progress)\b', 2.0),
        (r'\b(last time|previously|earlier)\b', 2.0),
    ],
    QueryType.AUTOMATION_RECIPE: [
        (r'\bhow do I (run|execute|validate|check|generate|create|build)\b', 3.0),
        (r'\b(how to run|command|script)\b', 3.0),
        (r'\b(automation|recipe|justfile|just|make)\b', 2.0),
        (r'\b(validate|test|build|deploy|lint)\b', 1.5),  # Weaken test/build keywords
    ],
}

# --- Data Models ---

@dataclass
class DiscoveryResult:
    """Result of a discovery query."""
    query: str
    query_type: QueryType
    method_used: str
    results: List[Dict[str, Any]]
    token_estimate: int
    time_seconds: float
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "query_type": self.query_type.value,
            "method_used": self.method_used,
            "results": self.results,
            "token_estimate": self.token_estimate,
            "time_seconds": round(self.time_seconds, 2),
            "suggestions": self.suggestions,
        }

# --- Query Classifier ---

class QueryClassifier:
    """Classify queries into discovery types with fuzzy matching and synonym expansion."""

    def classify(self, query: str) -> QueryType:
        """
        Classify query based on pattern matching with fuzzy matching and synonyms.

        OPP-2025-005 Priority 1: Added confidence threshold and negative pattern detection.
        """
        query_lower = query.lower()

        # Step 1: Check for negative patterns (OPP-2025-005 Priority 1)
        # Queries matching negative patterns should route to UNKNOWN immediately
        for neg_pattern in NEGATIVE_PATTERNS:
            if re.search(neg_pattern, query_lower):
                return QueryType.UNKNOWN

        # Extract keywords and expand with synonyms
        keywords = self._extract_keywords(query_lower)
        expanded_keywords = expand_keywords(keywords)

        # Create enhanced query text with expanded keywords
        enhanced_query = query_lower + " " + " ".join(expanded_keywords)

        scores = {}

        # OPP-2025-005 Priority 2: Use weighted pattern matching
        for query_type, patterns in QUERY_PATTERNS.items():
            score = 0
            for pattern_tuple in patterns:
                # Extract pattern and weight (OPP-2025-005 Priority 2)
                if isinstance(pattern_tuple, tuple):
                    pattern, weight = pattern_tuple
                else:
                    # Backwards compatibility (shouldn't happen, but safe)
                    pattern = pattern_tuple
                    weight = 2.0

                # Try exact pattern match first
                if re.search(pattern, enhanced_query):
                    score += weight  # Use pattern weight (OPP-2025-005 Priority 2)
                # Try fuzzy match on pattern keywords
                else:
                    # Extract pattern keywords (words in pattern, excluding regex syntax)
                    pattern_words = set(re.findall(r'\b([a-z]{3,})\b', pattern))
                    for pw in pattern_words:
                        matched, ratio = fuzzy_match_keyword(pw, enhanced_query)
                        if matched:
                            score += ratio * (weight / 2.0)  # Scale fuzzy by weight
            scores[query_type] = score

        # Step 2: Apply disambiguation rules (OPP-2025-005 Priority 2)
        # Rule: "how do we X" → PATTERN (unless "run" or "execute" present)
        if re.search(r'\bhow do we\b', query_lower):
            # Check for automation override keywords
            has_automation_override = re.search(r'\b(run|execute)\b', query_lower)
            if not has_automation_override:
                # Boost PATTERN score to ensure it wins
                scores[QueryType.PATTERN_CONCEPT] += 5.0

        # Rule: "workflow for X" → PATTERN (unless "run" or "command" present)
        if re.search(r'workflow for', query_lower):
            has_automation_override = re.search(r'\b(run|command)\b', query_lower)
            if not has_automation_override:
                scores[QueryType.PATTERN_CONCEPT] += 5.0  # Increased to match "how do we"

        # Rule: "when did/was X" → HISTORICAL (OPP-2025-005 Priority 3)
        # Temporal signals should override domain keywords
        if re.search(r'\b(when did|when was)\b', query_lower):
            scores[QueryType.HISTORICAL_EVENT] += 5.0

        # Rule: "show me X and run Y" → CODE (OPP-2025-005 CODE regression fix)
        # Compound queries should prioritize first intent (CODE) over second (AUTOMATION)
        if re.search(r'\b(show me|find|locate)\b', query_lower) and re.search(r'\band\b.*\b(run|execute)\b', query_lower):
            # "show me X and run Y" - prioritize CODE intent over AUTOMATION
            scores[QueryType.CODE_FEATURE] += 3.0

        # Rule: "documentation" or "docs" → CODE (OPP-2025-005 CODE regression fix)
        # Documentation queries should route to CODE even if "workflow" expands to "automation"
        if re.search(r'\b(documentation|docs|readme)\b', query_lower):
            # Strong signal that this is about code documentation, not automation
            scores[QueryType.CODE_FEATURE] += 2.0

        # Rule: "X code" → CODE (OPP-2025-005 CODE regression fix)
        # Queries ending in "code" are asking for code implementation, not automation
        if re.search(r'\w+\s+code\b', query_lower) and not re.search(r'\b(run|execute)\b', query_lower):
            # "authentiction code", "login code", etc. - clear CODE intent
            scores[QueryType.CODE_FEATURE] += 2.0

        # Step 3: Check confidence threshold (OPP-2025-005 Priority 1)
        # If max score is below threshold, route to UNKNOWN (low confidence)
        max_score = max(scores.values()) if scores else 0

        if max_score < CONFIDENCE_THRESHOLD:
            return QueryType.UNKNOWN

        # Step 4: Return type with highest score (high confidence)
        return max(scores, key=scores.get)

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract keywords from query."""
        stopwords = {"how", "do", "i", "we", "the", "a", "an", "is", "to", "for", "with", "show", "me"}
        words = re.findall(r'\w+', query.lower())
        return {w for w in words if w not in stopwords and len(w) > 2}

# --- Discovery Methods ---

class FeatureManifestDiscovery:
    """Discover code/features via feature-manifest.yaml."""

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.manifest_path = self.root / "feature-manifest.yaml"

    def discover(self, query: str) -> DiscoveryResult:
        """Search feature manifest for matching features."""
        import time
        start_time = time.time()

        results = []
        keywords = self._extract_keywords(query)

        if not self.manifest_path.exists():
            # Fallback to glob-based code discovery
            return self._fallback_discover(query, keywords, start_time)

        # Load manifest
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            features = data.get("features", [])

        # Search features
        for feature in features:
            score = self._score_feature(feature, keywords)
            if score > 0:
                result = {
                    "id": feature.get("id", "unknown"),
                    "name": feature.get("name", "unknown"),
                    "status": feature.get("status", "unknown"),
                    "score": score,
                    "artifacts": self._extract_artifacts(feature),
                }
                results.append(result)

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Token estimate: 2k for feature metadata + 1k per code file
        token_estimate = 2000
        if results:
            top_feature = results[0]
            code_count = len(top_feature.get("artifacts", {}).get("code", []))
            token_estimate += code_count * 1000

        suggestions = self._generate_suggestions(results)

        return DiscoveryResult(
            query=query,
            query_type=QueryType.CODE_FEATURE,
            method_used="feature_manifest",
            results=results[:5],  # Top 5
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract keywords from query."""
        stopwords = {"show", "me", "where", "is", "the", "a", "an", "find", "get", "for"}
        words = re.findall(r'\w+', query.lower())
        return {w for w in words if w not in stopwords and len(w) > 2}

    def _score_feature(self, feature: Dict, keywords: Set[str]) -> float:
        """Score feature relevance to keywords."""
        score = 0.0

        # Search in ID, name, tags
        searchable = [
            feature.get("id", "").lower(),
            feature.get("name", "").lower(),
        ]
        searchable.extend([t.lower() for t in feature.get("metadata", {}).get("tags", [])])

        for kw in keywords:
            for text in searchable:
                if kw in text:
                    score += 1.0

        return score

    def _extract_artifacts(self, feature: Dict) -> Dict[str, List]:
        """Extract code, tests, docs from feature."""
        return {
            "code": feature.get("code") or [],
            "tests": feature.get("tests") or [],
            "documentation": feature.get("documentation") or [],
            "knowledge": feature.get("knowledge") or [],
        }

    def _generate_suggestions(self, results: List[Dict]) -> List[str]:
        """Generate actionable suggestions."""
        if not results:
            return ["No features found. Try broader keywords or use grep fallback."]

        suggestions = []
        top = results[0]

        # Suggest loading specific artifacts
        artifacts = top.get("artifacts", {})
        if artifacts.get("code"):
            code_files = [c.get("path") for c in artifacts["code"] if isinstance(c, dict)]
            if code_files:
                suggestions.append(f"Load code: {code_files[0]}")

        if artifacts.get("knowledge"):
            suggestions.append(f"Read knowledge: {artifacts['knowledge'][0]}")

        if artifacts.get("documentation"):
            doc = artifacts["documentation"][0]
            if isinstance(doc, dict):
                suggestions.append(f"Read docs: {doc.get('path')}")

        return suggestions

    def _fallback_discover(self, query: str, keywords: Set[str], start_time: float) -> DiscoveryResult:
        """
        Fallback to glob-based code discovery when feature-manifest.yaml is missing.

        Searches common code directories for files matching keywords.
        Provides guidance to adopt SAP-056 (Lifecycle Traceability) for better results.
        """
        import time

        results = []

        # Common code directories to search
        code_dirs = ["src", "lib", "packages", "scripts"]
        # Common code extensions
        code_extensions = ["*.py", "*.ts", "*.js", "*.tsx", "*.jsx"]

        for code_dir in code_dirs:
            dir_path = self.root / code_dir
            if not dir_path.exists():
                continue

            for ext in code_extensions:
                for file_path in dir_path.glob(f"**/{ext}"):
                    # Check if any keyword matches the file path or name
                    file_str = str(file_path).lower()
                    score = sum(1 for kw in keywords if kw in file_str)

                    if score > 0:
                        results.append({
                            "path": str(file_path.relative_to(self.root)),
                            "name": file_path.name,
                            "score": score,
                        })

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Token estimate: ~1.5k per file (conservative estimate)
        token_estimate = min(len(results[:5]) * 1500, 10000)

        suggestions = [
            "⚠️  Using fallback glob search (less accurate than feature manifest)",
            "💡 Adopt SAP-056 (Lifecycle Traceability) for 50-70% token savings",
            "📖 See: docs/user-docs/how-to/use-unified-discovery.md"
        ]

        if results:
            suggestions.append(f"Found {len(results)} potential files")
            suggestions.append(f"Top match: {results[0]['path']}")
        else:
            suggestions.append("No code files found. Try different keywords.")

        return DiscoveryResult(
            query=query,
            query_type=QueryType.CODE_FEATURE,
            method_used="fallback_glob",
            results=results[:5],
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )


class KnowledgeGraphDiscovery:
    """Discover patterns/concepts via knowledge graph."""

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.notes_dir = self.root / ".chora" / "memory" / "knowledge" / "notes"

    def discover(self, query: str) -> DiscoveryResult:
        """Search knowledge notes for matching patterns."""
        import time
        start_time = time.time()

        results = []
        keywords = self._extract_keywords(query)

        if not self.notes_dir.exists():
            # Fallback to docs/ directory search
            return self._fallback_discover(query, keywords, start_time)

        # Search notes
        for note_path in self.notes_dir.glob("**/*.md"):
            try:
                content = note_path.read_text(encoding="utf-8")
                score = self._score_note(content, keywords)

                if score > 0:
                    results.append({
                        "path": str(note_path.relative_to(self.root)),
                        "title": self._extract_title(content, note_path),
                        "score": score,
                    })
            except Exception:
                continue

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Token estimate: ~2k per note
        token_estimate = min(len(results[:5]) * 2000, 15000)

        suggestions = self._generate_suggestions(results)

        return DiscoveryResult(
            query=query,
            query_type=QueryType.PATTERN_CONCEPT,
            method_used="knowledge_graph",
            results=results[:5],
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract keywords from query."""
        stopwords = {"how", "do", "we", "what", "is", "the", "a", "an", "for", "best", "practice"}
        words = re.findall(r'\w+', query.lower())
        return {w for w in words if w not in stopwords and len(w) > 2}

    def _score_note(self, content: str, keywords: Set[str]) -> float:
        """Score note relevance."""
        score = 0.0
        content_lower = content.lower()

        for kw in keywords:
            # Count occurrences (capped at 5 per keyword)
            count = min(content_lower.count(kw), 5)
            score += count * 0.5

        return score

    def _extract_title(self, content: str, note_path: Path) -> str:
        """Extract title from frontmatter or filename."""
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)', content)
        if title_match:
            return title_match.group(1)
        return note_path.stem

    def _generate_suggestions(self, results: List[Dict]) -> List[str]:
        """Generate suggestions."""
        if not results:
            return ["No knowledge notes found. Try different keywords."]

        suggestions = [f"Read: {results[0]['path']}"]
        if len(results) > 1:
            suggestions.append(f"Also relevant: {results[1]['path']}")

        return suggestions

    def _fallback_discover(self, query: str, keywords: Set[str], start_time: float) -> DiscoveryResult:
        """
        Fallback to docs/ directory search when knowledge notes are missing.

        Searches documentation files for patterns and concepts.
        Provides guidance to adopt SAP-010 (Memory System) for better results.
        """
        import time

        results = []

        # Search docs/ directory for markdown files
        docs_dir = self.root / "docs"
        if docs_dir.exists():
            for doc_path in docs_dir.glob("**/*.md"):
                try:
                    content = doc_path.read_text(encoding="utf-8")
                    score = self._score_note(content, keywords)

                    if score > 0:
                        results.append({
                            "path": str(doc_path.relative_to(self.root)),
                            "title": self._extract_title(content, doc_path),
                            "score": score,
                        })
                except Exception:
                    continue

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Token estimate: ~2k per doc
        token_estimate = min(len(results[:5]) * 2000, 15000)

        suggestions = [
            "⚠️  Using fallback docs/ search (less organized than knowledge notes)",
            "💡 Adopt SAP-010 (Memory System) for curated knowledge patterns",
            "📖 See: docs/user-docs/how-to/use-unified-discovery.md"
        ]

        if results:
            suggestions.append(f"Found {len(results)} docs")
            suggestions.append(f"Read: {results[0]['path']}")
        else:
            suggestions.append("No documentation found. Try different keywords.")

        return DiscoveryResult(
            query=query,
            query_type=QueryType.PATTERN_CONCEPT,
            method_used="fallback_docs",
            results=results[:5],
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )


class EventLogDiscovery:
    """Discover historical events via event logs."""

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.events_dir = self.root / ".chora" / "memory" / "events"

    def discover(self, query: str) -> DiscoveryResult:
        """Search event logs for matching events."""
        import time
        start_time = time.time()

        results = []
        keywords = self._extract_keywords(query)

        if not self.events_dir.exists():
            # Fallback to git log search
            return self._fallback_discover(query, keywords, start_time)

        # Search recent logs
        log_files = sorted(list(self.events_dir.glob("*.jsonl")), reverse=True)

        for log_file in log_files[:2]:  # Last 2 months
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            event = json.loads(line)
                            if self._matches_query(event, keywords):
                                results.append({
                                    "timestamp": event.get("timestamp", "unknown"),
                                    "event_type": event.get("event_type", "unknown"),
                                    "trace_id": event.get("trace_id", "unknown"),
                                    "message": event.get("message", "")[:100],  # Truncate
                                })
                        except Exception:
                            continue
            except Exception:
                continue

        # Token estimate: ~1.5k per event
        token_estimate = min(len(results[:5]) * 1500, 12000)

        suggestions = self._generate_suggestions(results)

        return DiscoveryResult(
            query=query,
            query_type=QueryType.HISTORICAL_EVENT,
            method_used="event_logs",
            results=results[:10],  # More events for timeline
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract keywords from query."""
        stopwords = {"when", "did", "was", "we", "the", "a", "an"}
        words = re.findall(r'\w+', query.lower())
        return {w for w in words if w not in stopwords and len(w) > 2}

    def _matches_query(self, event: Dict, keywords: Set[str]) -> bool:
        """Check if event matches query."""
        event_str = json.dumps(event).lower()
        return any(kw in event_str for kw in keywords)

    def _generate_suggestions(self, results: List[Dict]) -> List[str]:
        """Generate suggestions."""
        if not results:
            return ["No matching events found. Try broader time range or keywords."]

        suggestions = [f"Found {len(results)} events"]
        if results:
            latest = results[0]
            suggestions.append(f"Latest: {latest['timestamp']} - {latest['event_type']}")

        return suggestions

    def _fallback_discover(self, query: str, keywords: Set[str], start_time: float) -> DiscoveryResult:
        """
        Fallback to git log search when event logs are missing.

        Searches recent git commits for historical context.
        Provides guidance to adopt SAP-010 (Memory System) for better results.
        """
        import time

        results = []

        # Try to get git log (last 50 commits)
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-50"],
                capture_output=True,
                text=True,
                cwd=self.root,
                timeout=5
            )

            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if not line.strip():
                        continue

                    # Parse git log line: "commit_hash commit_message"
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        commit_hash, message = parts

                        # Check if any keyword matches the commit message
                        message_lower = message.lower()
                        if any(kw in message_lower for kw in keywords):
                            results.append({
                                "commit": commit_hash,
                                "message": message,
                                "timestamp": "unknown",  # git log --oneline doesn't include dates
                                "event_type": "git_commit",
                            })

        except Exception:
            pass  # Git not available or error occurred

        # Token estimate: ~1k per commit
        token_estimate = min(len(results[:10]) * 1000, 10000)

        suggestions = [
            "⚠️  Using fallback git log search (less structured than event logs)",
            "💡 Adopt SAP-010 (Memory System) for structured event tracking",
            "📖 See: docs/user-docs/how-to/use-unified-discovery.md"
        ]

        if results:
            suggestions.append(f"Found {len(results)} matching commits")
            suggestions.append(f"Recent: {results[0]['commit']} - {results[0]['message']}")
        else:
            suggestions.append("No matching commits found. Try different keywords.")

        return DiscoveryResult(
            query=query,
            query_type=QueryType.HISTORICAL_EVENT,
            method_used="fallback_git_log",
            results=results[:10],
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )


class JustfileDiscovery:
    """Discover automation recipes via justfile."""

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.justfile_path = self.root / "justfile"

    def discover(self, query: str) -> DiscoveryResult:
        """Search justfile for matching recipes."""
        import time
        start_time = time.time()

        results = []
        keywords = self._extract_keywords(query)

        if not self.justfile_path.exists():
            # Fallback to scripts/ directory search
            return self._fallback_discover(query, keywords, start_time)

        # Run just --list to get recipes
        try:
            result = subprocess.run(
                ["just", "--list"],
                capture_output=True,
                text=True,
                cwd=self.root,
                timeout=5
            )

            if result.returncode == 0:
                recipes = self._parse_recipes(result.stdout, keywords)
                results = recipes
        except Exception as e:
            return DiscoveryResult(
                query=query,
                query_type=QueryType.AUTOMATION_RECIPE,
                method_used="justfile",
                results=[],
                token_estimate=0,
                time_seconds=time.time() - start_time,
                suggestions=[f"Error running just: {e}"]
            )

        # Token estimate: ~500 per recipe
        token_estimate = min(len(results) * 500, 5000)

        suggestions = self._generate_suggestions(results)

        return DiscoveryResult(
            query=query,
            query_type=QueryType.AUTOMATION_RECIPE,
            method_used="justfile",
            results=results[:5],
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract keywords from query."""
        stopwords = {"how", "do", "i", "run", "the", "a", "an"}
        words = re.findall(r'\w+', query.lower())
        return {w for w in words if w not in stopwords and len(w) > 2}

    def _parse_recipes(self, just_output: str, keywords: Set[str]) -> List[Dict]:
        """Parse just --list output and filter by keywords."""
        recipes = []

        for line in just_output.split('\n'):
            # Skip headers and empty lines
            if not line.strip() or line.startswith("Available recipes"):
                continue

            # Parse recipe line: "  recipe-name  # description"
            match = re.match(r'\s+(\S+)\s+(?:#\s*(.+))?', line)
            if match:
                name = match.group(1)
                description = match.group(2) or ""

                # Score based on keyword matches
                score = 0
                for kw in keywords:
                    if kw in name.lower():
                        score += 2
                    if kw in description.lower():
                        score += 1

                if score > 0 or not keywords:  # Include all if no keywords
                    recipes.append({
                        "recipe": name,
                        "description": description,
                        "score": score,
                    })

        # Sort by score
        recipes.sort(key=lambda x: x["score"], reverse=True)
        return recipes

    def _generate_suggestions(self, results: List[Dict]) -> List[str]:
        """Generate suggestions."""
        if not results:
            return ["No matching recipes found. Run 'just --list' to see all."]

        top = results[0]
        suggestions = [f"Run: just {top['recipe']}"]

        if len(results) > 1:
            suggestions.append(f"Also: just {results[1]['recipe']}")

        return suggestions

    def _fallback_discover(self, query: str, keywords: Set[str], start_time: float) -> DiscoveryResult:
        """
        Fallback to scripts/ directory search when justfile is missing.

        Searches automation scripts (Python, Shell) for matching keywords.
        Provides guidance to adopt SAP-008 (Automation Dashboard) for better results.
        """
        import time

        results = []

        # Search scripts/ directory
        scripts_dir = self.root / "scripts"
        if scripts_dir.exists():
            for script_path in scripts_dir.glob("*.*"):
                # Only include Python and Shell scripts
                if script_path.suffix not in [".py", ".sh", ".bash"]:
                    continue

                # Check if any keyword matches the script name
                script_name = script_path.stem.lower()
                score = sum(1 for kw in keywords if kw in script_name)

                if score > 0:
                    # Try to extract description from first line of file
                    description = ""
                    try:
                        with open(script_path, "r", encoding="utf-8") as f:
                            first_line = f.readline()
                            # Extract description from shebang comment or docstring
                            if first_line.startswith("#"):
                                description = first_line.strip("# \n")
                    except Exception:
                        pass

                    results.append({
                        "script": script_path.name,
                        "path": str(script_path.relative_to(self.root)),
                        "description": description,
                        "score": score,
                    })

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Token estimate: ~500 per script
        token_estimate = min(len(results[:5]) * 500, 5000)

        suggestions = [
            "⚠️  Using fallback scripts/ search (less organized than justfile)",
            "💡 Adopt SAP-008 (Automation Dashboard) with justfile for centralized recipes",
            "📖 See: docs/user-docs/how-to/use-unified-discovery.md"
        ]

        if results:
            suggestions.append(f"Found {len(results)} scripts")
            suggestions.append(f"Run: python {results[0]['path']}")
        else:
            suggestions.append("No automation scripts found. Try different keywords.")

        return DiscoveryResult(
            query=query,
            query_type=QueryType.AUTOMATION_RECIPE,
            method_used="fallback_scripts",
            results=results[:5],
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )


class IntentionGraphDiscovery:
    """
    Discover via intention graph with BFS traversal (SAP-009 v1.4.0 Phase 2 Component 3).

    Combines keyword search with graph traversal for deep discovery:
    1. Find seed nodes via keyword matching
    2. Traverse graph (2-hop BFS) to discover related nodes
    3. Merge and deduplicate results
    """

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        # Import here to avoid circular dependencies
        sys.path.insert(0, str(self.root / "scripts"))
        try:
            from intention_graph_library import IntentionGraph
            self.IntentionGraph = IntentionGraph
        except (ImportError, ModuleNotFoundError) as e:
            raise ImportError(
                "intention_graph_library not available. "
                "IntentionGraphDiscovery requires SAP-009 v1.4.0 Phase 2 (Intention Graph). "
                "Discovery will work without this optional feature."
            ) from e

    def discover(self, query: str, max_depth: int = 2, max_results: int = 20) -> DiscoveryResult:
        """
        Discover nodes via graph traversal.

        Args:
            query: Search query
            max_depth: Maximum traversal depth (default: 2 hops)
            max_results: Maximum results to return

        Returns:
            DiscoveryResult with nodes and traversal info
        """
        import time
        start_time = time.time()

        # Load graph
        try:
            graph = self.IntentionGraph.load()
        except Exception as e:
            return DiscoveryResult(
                query=query,
                query_type=QueryType.UNKNOWN,
                method_used="intention_graph",
                results=[],
                token_estimate=0,
                time_seconds=time.time() - start_time,
                suggestions=[f"Error loading graph: {e}"]
            )

        # Extract keywords
        keywords = self._extract_keywords(query)

        # Step 1: Find seed nodes via keyword matching
        seed_nodes = self._find_seed_nodes(graph, keywords)

        if not seed_nodes:
            return DiscoveryResult(
                query=query,
                query_type=QueryType.UNKNOWN,
                method_used="intention_graph",
                results=[],
                token_estimate=0,
                time_seconds=time.time() - start_time,
                suggestions=["No matching nodes found. Try different keywords."]
            )

        # Step 2: Traverse graph from seed nodes (BFS, max_depth hops)
        traversed_nodes = self._traverse_graph(graph, seed_nodes, max_depth=max_depth)

        # Step 3: Merge seed nodes and traversed nodes, deduplicate
        all_nodes = self._merge_and_deduplicate(seed_nodes, traversed_nodes)

        # Step 4: Sort by relevance score
        all_nodes.sort(key=lambda x: x["score"], reverse=True)

        # Format results
        results = []
        for node_data in all_nodes[:max_results]:
            node = node_data["node"]
            results.append({
                "id": node["id"],
                "type": node["node_type"],
                "title": node["title"],
                "status": node.get("status", "unknown"),
                "lifecycle_stage": node.get("lifecycle_stage", "unknown"),
                "score": node_data["score"],
                "discovery_path": node_data.get("path", "direct"),  # direct or via relationship
                "created_by": node.get("metadata", {}).get("created_by", "unknown"),  # SAP-009 v1.4.0 Phase 2
            })

        # Token estimate: ~1.5k per node
        token_estimate = min(len(results) * 1500, 30000)

        suggestions = self._generate_suggestions(results, seed_nodes, traversed_nodes)

        return DiscoveryResult(
            query=query,
            query_type=QueryType.UNKNOWN,  # Generic for graph discovery
            method_used="intention_graph",
            results=results,
            token_estimate=token_estimate,
            time_seconds=time.time() - start_time,
            suggestions=suggestions
        )

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract keywords from query."""
        stopwords = {"show", "me", "find", "get", "what", "how", "when", "where", "is", "the", "a", "an", "for", "with", "to"}
        words = re.findall(r'\w+', query.lower())
        return {w for w in words if w not in stopwords and len(w) > 2}

    def _find_seed_nodes(self, graph, keywords: Set[str]) -> List[Dict]:
        """
        Find seed nodes via keyword matching in node id, title, description.

        Returns:
            List of dicts with {node, score}
        """
        seed_nodes = []

        for node in graph.nodes:
            score = self._score_node(node, keywords)
            if score > 0:
                seed_nodes.append({
                    "node": node,
                    "score": score,
                    "path": "direct",
                })

        return seed_nodes

    def _score_node(self, node: Dict, keywords: Set[str]) -> float:
        """Score node relevance to keywords."""
        score = 0.0

        # Search in ID (exact match gets high score)
        node_id = node.get("id", "").lower()
        for kw in keywords:
            if kw in node_id:
                score += 3.0  # ID match is very relevant

        # Search in title
        title = node.get("title", "").lower()
        for kw in keywords:
            if kw in title:
                score += 2.0

        # Search in description (truncated)
        description = node.get("description", "")[:500].lower()
        for kw in keywords:
            count = min(description.count(kw), 3)  # Cap at 3
            score += count * 0.5

        # Search in tags
        tags = [t.lower() for t in node.get("tags", [])]
        for kw in keywords:
            if kw in tags:
                score += 1.5

        return score

    def _traverse_graph(self, graph, seed_nodes: List[Dict], max_depth: int = 2) -> List[Dict]:
        """
        Traverse graph from seed nodes using BFS (max_depth hops).

        Returns:
            List of dicts with {node, score, path}
        """
        traversed = []
        visited = set(node_data["node"]["id"] for node_data in seed_nodes)

        # BFS queue: (node_id, depth, path_description)
        queue = [(node_data["node"]["id"], 0, f"seed:{node_data['node']['id']}")
                 for node_data in seed_nodes]

        while queue:
            current_id, depth, path = queue.pop(0)

            if depth >= max_depth:
                continue

            # Find edges from current node
            outgoing_edges = [e for e in graph.edges if e.get("source") == current_id]

            for edge in outgoing_edges:
                target_id = edge.get("target")

                if target_id not in visited:
                    visited.add(target_id)

                    # Get target node
                    target_node = graph.nodes_by_id.get(target_id)
                    if target_node:
                        relationship = edge.get("relationship", "relates_to")
                        new_path = f"{path}-[{relationship}]->{target_id}"

                        # Score decays with depth
                        score = 1.0 / (depth + 2)  # Depth 0: 1.0, Depth 1: 0.5, Depth 2: 0.33

                        traversed.append({
                            "node": target_node,
                            "score": score,
                            "path": new_path,
                        })

                        # Add to queue for further traversal
                        queue.append((target_id, depth + 1, new_path))

        return traversed

    def _merge_and_deduplicate(self, seed_nodes: List[Dict], traversed_nodes: List[Dict]) -> List[Dict]:
        """Merge seed and traversed nodes, keeping highest score for duplicates."""
        merged = {}

        for node_data in seed_nodes + traversed_nodes:
            node_id = node_data["node"]["id"]

            if node_id not in merged or node_data["score"] > merged[node_id]["score"]:
                merged[node_id] = node_data

        return list(merged.values())

    def _generate_suggestions(self, results: List[Dict], seed_nodes: List[Dict], traversed_nodes: List[Dict]) -> List[str]:
        """Generate actionable suggestions."""
        suggestions = []

        if not results:
            return ["No nodes found. Try different keywords or use direct query tools."]

        suggestions.append(f"Found {len(seed_nodes)} direct matches, {len(traversed_nodes)} related nodes")

        if results:
            top = results[0]
            suggestions.append(f"Top result: {top['id']} ({top['type']}) - score {top['score']:.2f}")

        # Suggest related queries
        node_types = set(r["type"] for r in results[:5])
        if len(node_types) > 1:
            suggestions.append(f"Results span multiple types: {', '.join(sorted(node_types))}")

        return suggestions


# --- Discovery Router ---

class DiscoveryRouter:
    """Route queries to optimal discovery method."""

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.classifier = QueryClassifier()

        # Initialize discovery methods
        self.feature_discovery = FeatureManifestDiscovery(workspace_root)
        self.knowledge_discovery = KnowledgeGraphDiscovery(workspace_root)
        self.event_discovery = EventLogDiscovery(workspace_root)
        self.justfile_discovery = JustfileDiscovery(workspace_root)

        # SAP-009 v1.4.0 Phase 2: Intention graph discovery (optional)
        # Only available when intention_graph_library is installed
        try:
            self.graph_discovery = IntentionGraphDiscovery(workspace_root)
        except (ImportError, ModuleNotFoundError):
            self.graph_discovery = None  # Graceful degradation without intention graph

    def route(self, query: str) -> DiscoveryResult:
        """
        Route query to optimal discovery method.

        OPP-2025-005 Priority 1: Updated to properly handle UNKNOWN queries.
        """
        import time
        query_type = self.classifier.classify(query)

        if query_type == QueryType.CODE_FEATURE:
            return self.feature_discovery.discover(query)
        elif query_type == QueryType.PATTERN_CONCEPT:
            return self.knowledge_discovery.discover(query)
        elif query_type == QueryType.HISTORICAL_EVENT:
            return self.event_discovery.discover(query)
        elif query_type == QueryType.AUTOMATION_RECIPE:
            return self.justfile_discovery.discover(query)
        elif query_type == QueryType.UNKNOWN:
            # OPP-2025-005 Priority 1: Return UNKNOWN result instead of fallback
            # Queries classified as UNKNOWN (negative patterns or low confidence) should not route to discovery
            return DiscoveryResult(
                query=query,
                query_type=QueryType.UNKNOWN,
                method_used="none",
                results=[],
                token_estimate=0,
                time_seconds=0.0,
                suggestions=[
                    "Query could not be classified with confidence.",
                    "Try rephrasing with more specific terms:",
                    "  - 'show me CODE for X' (code/feature query)",
                    "  - 'how do we PATTERN for X' (pattern/concept query)",
                    "  - 'when did EVENT X' (historical query)",
                    "  - 'how do I RUN X' (automation recipe)",
                ]
            )
        else:
            # Should never reach here, but fallback just in case
            result = self.feature_discovery.discover(query)
            if not result.results:
                result = self.knowledge_discovery.discover(query)
            return result

    def route_deep(self, query: str, max_depth: int = 2, max_results: int = 20) -> DiscoveryResult:
        """
        Route query to intention graph for deep discovery with traversal (SAP-009 v1.4.0 Phase 2).

        Uses graph traversal to discover related nodes beyond keyword matching.

        Args:
            query: Search query
            max_depth: Maximum traversal depth (default: 2 hops)
            max_results: Maximum results to return

        Returns:
            DiscoveryResult with graph-based discovery
        """
        return self.graph_discovery.discover(query, max_depth=max_depth, max_results=max_results)


# --- Output Formatting ---

def format_text_output(result: DiscoveryResult):
    """Format discovery result as human-readable text."""
    print("\n" + "="*60)
    print("UNIFIED DISCOVERY SYSTEM")
    print("="*60)

    print(f"\n[QUERY] {result.query}")
    print(f"[TYPE] {result.query_type.value}")
    print(f"[METHOD] {result.method_used}")
    print(f"[TIME] {result.time_seconds:.2f}s")
    print(f"[TOKEN EST] ~{result.token_estimate:,} tokens")

    print(f"\n[RESULTS] Found {len(result.results)} match(es):")
    print("-" * 60)

    for i, res in enumerate(result.results, 1):
        print(f"{i}. ", end="")

        # Format based on result type
        if "type" in res and "discovery_path" in res:  # Graph discovery result (SAP-009 v1.4.0 Phase 2)
            print(f"[{res['type'].upper()}] {res['id']}")
            print(f"   {res['title']}")
            print(f"   Status: {res['status']} | Stage: {res['lifecycle_stage']} | Score: {res['score']:.2f}")
            if res.get("discovery_path") != "direct":
                print(f"   Path: {res['discovery_path'][:80]}...")
            if res.get("created_by") != "unknown":
                print(f"   Created by: {res['created_by']}")
        elif "name" in res:  # Feature result
            print(f"[{res['id']}] {res['name']} ({res['status']})")
            if "artifacts" in res:
                artifacts = res["artifacts"]
                if artifacts.get("code"):
                    print(f"   Code: {len(artifacts['code'])} file(s)")
                if artifacts.get("knowledge"):
                    print(f"   Knowledge: {artifacts['knowledge']}")
        elif "path" in res:  # Knowledge note result
            print(f"{res['title']}")
            print(f"   Path: {res['path']}")
        elif "timestamp" in res:  # Event result
            print(f"{res['timestamp']} - {res['event_type']}")
            if res.get("message"):
                print(f"   {res['message']}")
        elif "recipe" in res:  # Justfile recipe result
            print(f"just {res['recipe']}")
            if res.get("description"):
                print(f"   {res['description']}")
        print()

    print("[SUGGESTIONS]")
    for suggestion in result.suggestions:
        print(f"   - {suggestion}")

    print("\n" + "="*60)


def format_json_output(result: DiscoveryResult):
    """Format discovery result as JSON."""
    print(json.dumps(result.to_dict(), indent=2, default=str))


# --- Main ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Unified Discovery System - Intelligent query routing for chora-workspace"
    )
    parser.add_argument("query", nargs="+", help="Discovery query")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "deep"],
        default="auto",
        help="Discovery mode: auto (intelligent routing) or deep (graph traversal) [SAP-009 v1.4.0 Phase 2]"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum traversal depth for deep mode (default: 2 hops)"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=20,
        help="Maximum results to return for deep mode (default: 20)"
    )

    args = parser.parse_args()
    query_str = " ".join(args.query)

    # Route and discover
    router = DiscoveryRouter(Path("."))

    if args.mode == "deep":
        result = router.route_deep(query_str, max_depth=args.max_depth, max_results=args.max_results)
    else:
        result = router.route(query_str)

    # Output
    if args.format == "json":
        format_json_output(result)
    else:
        format_text_output(result)
