#!/usr/bin/env python3
"""
A-MEM Knowledge Graph Auto-Indexer

Generates links.json and tags.json from knowledge note frontmatter.

Usage:
    python scripts/a-mem-index.py                    # Generate both indexes
    python scripts/a-mem-index.py --links-only       # Generate links.json only
    python scripts/a-mem-index.py --tags-only        # Generate tags.json only
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown file"""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        return {}

    frontmatter_text = match.group(1)
    frontmatter = {}

    # Parse simple YAML fields
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle lists (tags, linked_to)
            if value.startswith('[') and value.endswith(']'):
                # Parse list: [tag1, tag2, tag3]
                value = value[1:-1]  # Remove brackets
                items = [item.strip().strip('"').strip("'") for item in value.split(',')]
                frontmatter[key] = [item for item in items if item]
            else:
                frontmatter[key] = value.strip('"').strip("'")

    return frontmatter


def generate_links_json(knowledge_dir: Path) -> Dict:
    """
    Generate bidirectional link graph from knowledge notes.

    Returns:
        {
            "notes": {
                "note1.md": ["note2.md", "note3.md"],
                "note2.md": ["note1.md"]
            },
            "backlinks": {
                "note2.md": ["note1.md"],
                "note3.md": ["note1.md"]
            }
        }
    """
    links = {}
    backlinks = {}

    if not knowledge_dir.exists():
        return {"notes": {}, "backlinks": {}}

    for note_path in knowledge_dir.glob("*.md"):
        note_id = note_path.name
        content = note_path.read_text()
        frontmatter = parse_frontmatter(content)

        # Get linked_to field
        linked_to = frontmatter.get("linked_to", [])
        if isinstance(linked_to, str):
            linked_to = [linked_to] if linked_to else []

        links[note_id] = linked_to

        # Build backlinks
        for target in linked_to:
            if target not in backlinks:
                backlinks[target] = []
            if note_id not in backlinks[target]:
                backlinks[target].append(note_id)

    return {
        "notes": links,
        "backlinks": backlinks,
        "total_notes": len(links),
        "total_links": sum(len(v) for v in links.values()),
        "generated": "2025-11-05T22:50:00Z"
    }


def generate_tags_json(knowledge_dir: Path) -> Dict:
    """
    Generate tag index from knowledge notes.

    Returns:
        {
            "tags": {
                "sap-010": ["note1.md", "note2.md"],
                "jinja2": ["note3.md"]
            },
            "notes": {
                "note1.md": ["sap-010", "adoption"],
                "note2.md": ["sap-010", "a-mem"]
            }
        }
    """
    tags_to_notes = {}
    notes_to_tags = {}

    if not knowledge_dir.exists():
        return {"tags": {}, "notes": {}}

    for note_path in knowledge_dir.glob("*.md"):
        note_id = note_path.name
        content = note_path.read_text()
        frontmatter = parse_frontmatter(content)

        # Get tags field
        tags = frontmatter.get("tags", [])
        if isinstance(tags, str):
            tags = [tags] if tags else []

        notes_to_tags[note_id] = tags

        # Build tag index
        for tag in tags:
            if tag not in tags_to_notes:
                tags_to_notes[tag] = []
            if note_id not in tags_to_notes[tag]:
                tags_to_notes[tag].append(note_id)

    return {
        "tags": tags_to_notes,
        "notes": notes_to_tags,
        "total_tags": len(tags_to_notes),
        "total_notes": len(notes_to_tags),
        "generated": "2025-11-05T22:50:00Z"
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM knowledge graph auto-indexer"
    )
    parser.add_argument(
        "--memory-dir",
        default=".chora/memory",
        help="A-MEM directory (default: .chora/memory)"
    )
    parser.add_argument(
        "--links-only",
        action="store_true",
        help="Generate links.json only"
    )
    parser.add_argument(
        "--tags-only",
        action="store_true",
        help="Generate tags.json only"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files"
    )

    args = parser.parse_args()

    # Resolve paths
    memory_dir = Path(args.memory_dir)
    knowledge_dir = memory_dir / "knowledge"

    if not knowledge_dir.exists():
        print(f"⚠️  Knowledge directory not found: {knowledge_dir}", file=sys.stderr)
        print(f"   Creating directory...", file=sys.stderr)
        knowledge_dir.mkdir(parents=True, exist_ok=True)

    # Generate links.json
    if not args.tags_only:
        links_data = generate_links_json(knowledge_dir)
        links_path = knowledge_dir / "links.json"

        if args.dry_run:
            print("📄 links.json (dry-run):")
            print(json.dumps(links_data, indent=2))
        else:
            with open(links_path, "w") as f:
                json.dump(links_data, f, indent=2)
            print(f"✅ Generated: {links_path}")
            print(f"   Total notes: {links_data['total_notes']}")
            print(f"   Total links: {links_data['total_links']}")

    # Generate tags.json
    if not args.links_only:
        tags_data = generate_tags_json(knowledge_dir)
        tags_path = knowledge_dir / "tags.json"

        if args.dry_run:
            print("\n📄 tags.json (dry-run):")
            print(json.dumps(tags_data, indent=2))
        else:
            with open(tags_path, "w") as f:
                json.dump(tags_data, f, indent=2)
            print(f"✅ Generated: {tags_path}")
            print(f"   Total tags: {tags_data['total_tags']}")
            print(f"   Total notes: {tags_data['total_notes']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
