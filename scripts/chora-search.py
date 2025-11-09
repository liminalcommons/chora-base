#!/usr/bin/env python3
"""
Chora-base Glossary Search Tool

Search ecosystem terminology, find concepts, and discover related patterns.
Supports forward lookup (term → definition) and reverse lookup (description → term).

Usage:
    python scripts/chora-search.py "coordination request"
    python scripts/chora-search.py --reverse "I want to suggest a big change"
    python scripts/chora-search.py --related SAP-001
    python scripts/chora-search.py --fuzzy "coordenation"  # Handles typos
"""

import argparse
import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional




# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

@dataclass
class GlossaryEntry:
    """Represents a single glossary entry."""

    term: str
    definition: str
    category: str
    aliases: list[str]
    related_terms: list[str]
    sap_reference: Optional[str]
    file_reference: Optional[str]
    examples: list[str]


class GlossarySearch:
    """Search and navigate chora-base ecosystem terminology."""

    def __init__(self, glossary_file: Path):
        """Initialize search with glossary database."""
        self.glossary_file = glossary_file
        self.entries = self._load_glossary()

    def _load_glossary(self) -> list[GlossaryEntry]:
        """Load glossary from markdown file."""
        if not self.glossary_file.exists():
            print(f"⚠️  Glossary not found at {self.glossary_file}")
            return []

        with open(self.glossary_file, encoding='utf-8') as f:
            content = f.read()

        # Parse markdown glossary structure
        entries = []
        current_category = "General"

        # Pattern: ## Category or ### Term
        lines = content.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Category header
            if line.startswith("## ") and not line.startswith("###"):
                current_category = line[3:].strip()
                i += 1
                continue

            # Term entry
            if line.startswith("### "):
                term = line[4:].strip()
                definition_lines = []
                aliases = []
                related = []
                sap_ref = None
                file_ref = None
                examples = []

                i += 1
                # Collect definition and metadata
                while i < len(lines) and not lines[i].startswith("###"):
                    metadata_line = lines[i].strip()

                    if metadata_line.startswith("**Aliases:**"):
                        aliases = [
                            a.strip()
                            for a in metadata_line.split("**Aliases:**")[1].split(",")
                        ]
                    elif metadata_line.startswith("**Related:**"):
                        related = [
                            r.strip()
                            for r in metadata_line.split("**Related:**")[1].split(",")
                        ]
                    elif metadata_line.startswith("**SAP:**"):
                        sap_ref = metadata_line.split("**SAP:**")[1].strip()
                    elif metadata_line.startswith("**File:**"):
                        file_ref = metadata_line.split("**File:**")[1].strip()
                    elif metadata_line.startswith("**Example:**"):
                        examples.append(metadata_line.split("**Example:**")[1].strip())
                    elif metadata_line and not metadata_line.startswith("**"):
                        definition_lines.append(metadata_line)

                    i += 1

                definition = " ".join(definition_lines)

                if definition:  # Only add if has definition
                    entries.append(
                        GlossaryEntry(
                            term=term,
                            definition=definition,
                            category=current_category,
                            aliases=aliases,
                            related_terms=related,
                            sap_reference=sap_ref,
                            file_reference=file_ref,
                            examples=examples,
                        )
                    )
                continue

            i += 1

        return entries

    def search(self, query: str, fuzzy: bool = False) -> list[tuple[GlossaryEntry, float]]:
        """
        Search for term in glossary.

        Returns list of (entry, relevance_score) tuples sorted by relevance.
        """
        query_lower = query.lower()
        results = []

        for entry in self.entries:
            score = 0.0

            # Exact term match: 1.0
            if entry.term.lower() == query_lower:
                score = 1.0
            # Exact alias match: 1.0
            elif any(alias.lower() == query_lower for alias in entry.aliases):
                score = 1.0
            # Term contains query: 0.8
            elif query_lower in entry.term.lower():
                score = 0.8
            # Alias contains query: 0.7
            elif any(query_lower in alias.lower() for alias in entry.aliases):
                score = 0.7
            # Definition contains query: 0.6
            elif query_lower in entry.definition.lower():
                score = 0.6
            # Fuzzy match on term: 0.4-0.6
            elif fuzzy:
                similarity = difflib.SequenceMatcher(
                    None, query_lower, entry.term.lower()
                ).ratio()
                if similarity > 0.6:
                    score = 0.4 + (similarity - 0.6) * 0.5

            if score > 0:
                results.append((entry, score))

        # Sort by relevance descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def reverse_search(self, description: str) -> list[tuple[GlossaryEntry, float]]:
        """
        Reverse lookup: find terms matching a natural language description.

        Example: "I want to suggest a big change" → "Strategic Proposal"
        """
        desc_lower = description.lower()
        results = []

        for entry in self.entries:
            score = 0.0

            # Check if description matches definition
            desc_words = set(desc_lower.split())
            def_words = set(entry.definition.lower().split())

            # Calculate word overlap
            overlap = len(desc_words & def_words)
            if len(desc_words) > 0:
                overlap_ratio = overlap / len(desc_words)
                score = overlap_ratio

            # Boost if examples match
            for example in entry.examples:
                example_words = set(example.lower().split())
                example_overlap = len(desc_words & example_words)
                if len(desc_words) > 0:
                    example_ratio = example_overlap / len(desc_words)
                    score = max(score, example_ratio * 1.2)  # Boost examples

            if score > 0.2:  # Threshold for reverse search
                results.append((entry, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_related(self, term: str) -> list[GlossaryEntry]:
        """Find terms related to given term."""
        # First find the term
        results = self.search(term)
        if not results:
            return []

        entry = results[0][0]
        related_entries = []

        # Find entries for related terms
        for related_term in entry.related_terms:
            related_results = self.search(related_term)
            if related_results:
                related_entries.append(related_results[0][0])

        return related_entries

    def by_category(self, category: str) -> list[GlossaryEntry]:
        """Get all terms in a category."""
        return [e for e in self.entries if e.category.lower() == category.lower()]

    def by_sap(self, sap_id: str) -> list[GlossaryEntry]:
        """Get all terms related to a SAP."""
        return [e for e in self.entries if e.sap_reference == sap_id]


def display_entry(entry: GlossaryEntry, score: Optional[float] = None) -> None:
    """Display glossary entry in readable format."""
    print(f"\n{'='*70}")
    print(f"📖 {entry.term}")
    if score:
        print(f"   Relevance: {score:.0%}")
    print(f"{'='*70}")
    print(f"\n{entry.definition}\n")

    if entry.category != "General":
        print(f"Category: {entry.category}")

    if entry.aliases:
        print(f"Aliases: {', '.join(entry.aliases)}")

    if entry.sap_reference:
        print(f"SAP: {entry.sap_reference}")

    if entry.file_reference:
        print(f"File: {entry.file_reference}")

    if entry.examples:
        print("\nExamples:")
        for example in entry.examples:
            print(f"  • {example}")

    if entry.related_terms:
        print(f"\nRelated: {', '.join(entry.related_terms)}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Search chora-base ecosystem terminology"
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument(
        "--glossary",
        type=Path,
        default=Path("docs/GLOSSARY.md"),
        help="Path to glossary file",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Reverse lookup (description → term)",
    )
    parser.add_argument(
        "--fuzzy",
        action="store_true",
        help="Enable fuzzy matching (handles typos)",
    )
    parser.add_argument(
        "--related",
        help="Find terms related to given term",
    )
    parser.add_argument(
        "--category",
        help="List all terms in category",
    )
    parser.add_argument(
        "--sap",
        help="List all terms for a SAP",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all categories",
    )

    args = parser.parse_args()

    # Create search instance
    search = GlossarySearch(args.glossary)

    if not search.entries:
        print("❌ No glossary entries loaded")
        return 1

    # List categories
    if args.list_categories:
        categories = set(e.category for e in search.entries)
        print("📚 Categories:")
        for cat in sorted(categories):
            count = len([e for e in search.entries if e.category == cat])
            print(f"  • {cat} ({count} terms)")
        return 0

    # Related terms
    if args.related:
        related = search.get_related(args.related)
        if not related:
            print(f"❌ No related terms found for '{args.related}'")
            return 1
        print(f"\n🔗 Terms related to '{args.related}':")
        for entry in related:
            print(f"  • {entry.term} - {entry.definition[:60]}...")
        return 0

    # Category listing
    if args.category:
        entries = search.by_category(args.category)
        if not entries:
            print(f"❌ No terms found in category '{args.category}'")
            return 1
        print(f"\n📂 Terms in category '{args.category}':")
        for entry in entries:
            print(f"  • {entry.term} - {entry.definition[:60]}...")
        return 0

    # SAP listing
    if args.sap:
        entries = search.by_sap(args.sap)
        if not entries:
            print(f"❌ No terms found for {args.sap}")
            return 1
        print(f"\n🎯 Terms related to {args.sap}:")
        for entry in entries:
            print(f"  • {entry.term} - {entry.definition[:60]}...")
        return 0

    # Search query
    if args.query:
        if args.reverse:
            results = search.reverse_search(args.query)
            if not results:
                print(f"❌ No terms match description: '{args.query}'")
                return 1
            print(f"\n🔍 Terms matching '{args.query}':")
            for entry, score in results[:5]:  # Top 5
                print(f"\n  {score:.0%} - {entry.term}")
                print(f"       {entry.definition[:70]}...")
            return 0
        else:
            results = search.search(args.query, fuzzy=args.fuzzy)
            if not results:
                print(f"❌ No results found for '{args.query}'")
                if not args.fuzzy:
                    print("💡 Try --fuzzy to handle typos")
                return 1

            # Display top result in detail
            display_entry(results[0][0], results[0][1])

            # Show alternatives if multiple matches
            if len(results) > 1:
                print("\n📋 Other matches:")
                for entry, score in results[1:4]:  # Show top 3 alternatives
                    print(f"  • {entry.term} ({score:.0%})")
            return 0

    # No arguments: show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    exit(main())
