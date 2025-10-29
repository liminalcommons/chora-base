# How-To: Generate Documentation Status Report Using Chora Compose

**Skill Level:** Intermediate
**Time:** 10 minutes
**Prerequisites:**
- Chora Compose installed
- Understanding of Jinja2 templates
- Python scripting knowledge

## What This Solves

Manually tracking documentation status is tedious and error-prone. Changes include:

1. **Outdated counts**: Adding/removing docs means manually updating counts
2. **Missing files**: Easy to forget to list a new document
3. **Incorrect statistics**: Manual word counts are impractical
4. **No automation**: Status report becomes stale quickly

By using Chora Compose to automatically scan the filesystem and generate the status report, we can:

- Always have accurate document counts
- Never miss a file
- Get automatic word count statistics
- Regenerate the report in seconds
- Track documentation growth over time

This demonstrates **Chora Compose managing Chora Compose** - using our own tools to maintain our project.

## Key Insight: Two-Step Generation

This workflow uses a **two-step process**:

```
Step 1: Scan filesystem → JSON data
Step 2: JSON data + template → Markdown report
```

**Why two steps?**

1. **Separation of concerns**: Data collection vs. presentation
2. **Reusability**: Same data could generate HTML, PDF, or other formats
3. **Debugging**: Can inspect JSON data between steps
4. **Performance**: Only scan when needed, generate reports anytime

## Files Overview

```
scripts/
├── scan_documentation.py              # Step 1: Scan filesystem
└── generate_docs_status.py            # Step 2: Generate report

configs/
├── content/docs/
│   ├── docs-status-data.json         # 🔄 Generated data (Step 1 output)
│   └── docs-status-content.json      # Content config (Step 2 input)
└── templates/docs/
    └── status-report.j2               # Jinja2 template (Step 2 input)

DOCUMENTATION_STATUS-generated.md      # 📄 Final report (Step 2 output)
```

## Step 1: Create Documentation Scanner

Create a Python script that scans the `docs/` directory and extracts metadata:

**File:** `scripts/scan_documentation.py`

```python
#!/usr/bin/env python3
"""Scan documentation directory and generate structured data for status report."""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def categorize_doc(file_path: Path, docs_root: Path) -> dict[str, str] | None:
    """Categorize a documentation file by its Diátaxis type."""
    relative_path = file_path.relative_to(docs_root)
    parts = relative_path.parts

    # Skip meta, templates, and status files
    if parts[0] in ("meta", "templates") or "STATUS" in file_path.name:
        return None

    # Determine category
    category = None
    if parts[0] == "tutorials":
        category = "tutorial"
    elif parts[0] == "how-to":
        category = "how-to"
    elif parts[0] == "reference":
        category = "reference"
    elif parts[0] == "explanation":
        category = "explanation"
    else:
        return None

    # Extract topic from subdirectory
    topic = parts[1] if len(parts) > 1 else None

    return {
        "path": str(relative_path),
        "category": category,
        "topic": topic,
        "name": file_path.stem,
        "full_path": str(file_path),
        "word_count": count_words(file_path),
    }


def count_words(file_path: Path) -> int:
    """Count words in a markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        return len(content.split())
    except Exception:
        return 0


def scan_docs(docs_root: Path = Path("docs")) -> dict[str, Any]:
    """Scan documentation directory and return structured data."""
    md_files = list(docs_root.rglob("*.md"))

    categorized = defaultdict(list)
    by_topic = defaultdict(lambda: defaultdict(list))

    for md_file in md_files:
        doc_info = categorize_doc(md_file, docs_root)
        if doc_info:
            category = doc_info["category"]
            topic = doc_info["topic"]

            categorized[category].append(doc_info)
            if topic:
                by_topic[topic][category].append(doc_info)

    # Calculate statistics
    total_docs = sum(len(docs) for docs in categorized.values())
    total_words = sum(
        doc["word_count"]
        for docs in categorized.values()
        for doc in docs
    )

    return {
        "scan_date": datetime.now().isoformat(),
        "total_documents": total_docs,
        "total_words": total_words,
        "average_words_per_doc": total_words // total_docs if total_docs > 0 else 0,
        "counts_by_category": {
            "tutorials": len(categorized.get("tutorial", [])),
            "how_to_guides": len(categorized.get("how-to", [])),
            "reference": len(categorized.get("reference", [])),
            "explanation": len(categorized.get("explanation", [])),
        },
        "documents_by_category": dict(categorized),
        "documents_by_topic": dict(by_topic),
        "framework": "Diátaxis",
    }


def main() -> None:
    """Scan documentation and save structured data."""
    data = scan_docs()

    # Write JSON data
    output_dir = Path("configs/content/docs")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "docs-status-data.json"
    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"✅ Documentation scan complete!")
    print(f"📄 Output: {output_path}")
    print(f"📊 Total: {data['total_documents']} documents, {data['total_words']:,} words")


if __name__ == "__main__":
    main()
```

**Key Features:**
- Automatically categorizes files by directory structure
- Counts words in each file
- Groups documents by category and topic
- Calculates statistics
- Outputs structured JSON

## Step 2: Create Jinja2 Template

Create a template for the status report:

**File:** `configs/templates/docs/status-report.j2`

```jinja2
# Documentation Status Report

**Date:** {{ scan_data.scan_date[:10] }} (Auto-generated)
**Framework:** {{ scan_data.framework }}
**Total Documents:** {{ scan_data.total_documents }}
**Total Words:** {{ "{:,}".format(scan_data.total_words) }}

---

## Overview

This document tracks the completion status of {{ scan_data.framework }} documentation for all Chora Compose features.

---

## Overall Progress

### By Documentation Type

| Type | Count | Percentage |
|------|-------|------------|
| Tutorials | {{ scan_data.counts_by_category.tutorials }} | {{ "%.0f"|format((scan_data.counts_by_category.tutorials / scan_data.total_documents * 100)) }}% |
| How-To Guides | {{ scan_data.counts_by_category.how_to_guides }} | {{ "%.0f"|format((scan_data.counts_by_category.how_to_guides / scan_data.total_documents * 100)) }}% |
| Reference | {{ scan_data.counts_by_category.reference }} | {{ "%.0f"|format((scan_data.counts_by_category.reference / scan_data.total_documents * 100)) }}% |
| Explanation | {{ scan_data.counts_by_category.explanation }} | {{ "%.0f"|format((scan_data.counts_by_category.explanation / scan_data.total_documents * 100)) }}% |
| **Total** | **{{ scan_data.total_documents }}** | **100%** |

---

## Documentation by Category

### Tutorials ({{ scan_data.counts_by_category.tutorials }} documents)

{% for doc in scan_data.documents_by_category.tutorial | sort(attribute='full_path') %}
- [{{ doc.name | replace('-', ' ') | title }}]({{ doc.full_path }}) - {{ "{:,}".format(doc.word_count) }} words
{% endfor %}

[... similar sections for How-To, Reference, Explanation ...]

---

**Status:** ✅ Documentation scan complete
**Last Scan:** {{ scan_data.scan_date }}
**Generated:** Auto-generated using Chora Compose dogfooding
```

**Template Features:**
- Dynamic counts and percentages
- Sorted lists of documents
- Word count formatting
- Auto-generated timestamp

## Step 3: Create Content Config

**File:** `configs/content/docs/docs-status-content.json`

```json
{
  "type": "content",
  "id": "docs-status-report",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Auto-generated documentation status report from filesystem scan",
    "version": "1.0.0",
    "generation_frequency": "on_demand",
    "output_format": "markdown"
  },
  "generation": {
    "patterns": [
      {
        "id": "docs-status-generation",
        "type": "jinja2",
        "template": "status-report.j2",
        "generation_config": {
          "context": {
            "scan_data": {
              "source": "file",
              "path": "configs/content/docs/docs-status-data.json"
            }
          }
        }
      }
    ]
  }
}
```

## Step 4: Create Generation Script

**File:** `scripts/generate_docs_status.py`

```python
#!/usr/bin/env python3
"""Generate documentation status report from scanned data using Jinja2Generator."""

from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator


def main() -> None:
    """Generate documentation status report from scanned data."""
    config_path = Path("configs/content/docs/docs-status-content.json")
    loader = ConfigLoader()
    config = loader.load_config(config_path)

    template_dir = Path("configs/templates/docs")
    generator = Jinja2Generator(template_dir=template_dir)
    status_report = generator.generate(config)

    output_path = Path("DOCUMENTATION_STATUS-generated.md")
    output_path.write_text(status_report, encoding="utf-8")

    print(f"✅ Documentation status report generated!")
    print(f"📄 Output: {output_path}")


if __name__ == "__main__":
    main()
```

## Step 5: Generate the Report

Run both steps:

```bash
# Step 1: Scan documentation
poetry run python scripts/scan_documentation.py

# Step 2: Generate report
poetry run python scripts/generate_docs_status.py
```

**Expected Output:**

```
Step 1 output:
✅ Documentation scan complete!
📄 Output written to: configs/content/docs/docs-status-data.json

📊 Statistics:
   Total documents: 27
   Total words: 43,868
   Average words per doc: 1,624

📚 By Category:
   tutorials: 5
   how_to_guides: 14
   reference: 4
   explanation: 4

Step 2 output:
✅ Documentation status report generated successfully!
📄 Output written to: DOCUMENTATION_STATUS-generated.md
📊 Generated 7201 characters
📝 Generated 315 lines
```

## Step 6: Review and Use

Preview the generated report:

```bash
head -50 DOCUMENTATION_STATUS-generated.md
```

Compare with existing manual report:

```bash
diff docs/DOCUMENTATION_STATUS.md DOCUMENTATION_STATUS-generated.md
```

Replace manual version:

```bash
mv DOCUMENTATION_STATUS-generated.md docs/DOCUMENTATION_STATUS.md
```

## Benefits

### 1. Always Up-to-Date
- Scans filesystem directly
- No manual counting or listing
- Regenerate anytime in seconds

### 2. Accurate Statistics
- Automatic word counts
- Correct document counts
- Precise percentages

### 3. No Human Error
- Never miss a file
- Never miscategorize
- Never miscount words

### 4. Tracks Growth
- Save scan data with timestamps
- Compare scans over time
- Track documentation velocity

### 5. Demonstrates Chora Compose Value
- Real dogfooding example
- Shows automation benefits
- Validates Jinja2Generator

## Workflow Integration

### During Development

When you add new documentation:

```bash
# 1. Write your new doc
vim docs/how-to/new-feature.md

# 2. Regenerate status report
poetry run python scripts/scan_documentation.py
poetry run python scripts/generate_docs_status.py
mv DOCUMENTATION_STATUS-generated.md docs/DOCUMENTATION_STATUS.md

# 3. Commit both
git add docs/how-to/new-feature.md docs/DOCUMENTATION_STATUS.md
git commit -m "docs: add how-to for new feature"
```

### Before Releases

Update documentation status before each release:

```bash
# Part of release checklist
poetry run python scripts/scan_documentation.py
poetry run python scripts/generate_docs_status.py
mv DOCUMENTATION_STATUS-generated.md docs/DOCUMENTATION_STATUS.md
git add docs/DOCUMENTATION_STATUS.md
git commit -m "docs: update documentation status for v0.3.0"
```

### CI/CD Integration

Automate in GitHub Actions:

```yaml
- name: Generate documentation status report
  run: |
    poetry run python scripts/scan_documentation.py
    poetry run python scripts/generate_docs_status.py

- name: Check for changes
  run: |
    if ! diff docs/DOCUMENTATION_STATUS.md DOCUMENTATION_STATUS-generated.md; then
      echo "❌ Documentation status is out of date!"
      echo "Run: poetry run python scripts/scan_documentation.py"
      echo "Run: poetry run python scripts/generate_docs_status.py"
      exit 1
    fi
```

## Advanced: Tracking Over Time

Save scan data with timestamps:

```python
# Modified scanner to save timestamped data
def main():
    data = scan_docs()

    # Save timestamped version
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    history_dir = Path("configs/content/docs/history")
    history_dir.mkdir(parents=True, exist_ok=True)

    history_path = history_dir / f"scan-{timestamp}.json"
    history_path.write_text(json.dumps(data, indent=2))

    # Also save as current
    current_path = Path("configs/content/docs/docs-status-data.json")
    current_path.write_text(json.dumps(data, indent=2))
```

Then analyze growth:

```python
# Analyze documentation growth over time
def analyze_growth():
    history_dir = Path("configs/content/docs/history")
    scans = []

    for scan_file in sorted(history_dir.glob("scan-*.json")):
        data = json.loads(scan_file.read_text())
        scans.append({
            "date": data["scan_date"],
            "docs": data["total_documents"],
            "words": data["total_words"],
        })

    for scan in scans:
        print(f"{scan['date'][:10]}: {scan['docs']} docs, {scan['words']:,} words")
```

## Troubleshooting

**Scanner finds too few docs:**
- Check if files are in correct directories
- Verify `.md` extension
- Check if being filtered by `categorize_doc()`

**Template rendering errors:**
- Verify JSON data structure matches template
- Check for typos in variable names
- Test template with minimal data first

**Word counts seem wrong:**
- Word count uses simple whitespace split
- Code blocks count as words
- Front matter included in count

**Missing documents in output:**
- Scanner skips `meta/` and `templates/` directories
- Files with `STATUS` or `TEMPLATE` in name are skipped
- Root-level docs excluded (not categorized)

## Next Steps

1. **Automate in CI/CD**: Add to GitHub Actions
2. **Track history**: Save timestamped scans
3. **Generate charts**: Visualize documentation growth
4. **Multi-format output**: Generate HTML or PDF versions
5. **Coverage analysis**: Identify documentation gaps

## Related Documentation

- [How-To: Generate CHANGELOG](generate-changelog.md) - Similar dogfooding example
- [How-To: Generate Release Notes](generate-release-notes.md) - Data reuse pattern
- [Jinja2Generator API Reference](../../reference/api/generators/jinja2.md)
- [Tutorial: Dynamic Content with Jinja2](../../tutorials/intermediate/01-dynamic-content-with-jinja2.md)

## Success Criteria

You've successfully set up documentation status report generation when:

- ✅ Scanner successfully categorizes all documentation files
- ✅ Word counts are calculated correctly
- ✅ JSON data structure matches template expectations
- ✅ Generated report includes all documents
- ✅ Statistics (counts, percentages) are accurate
- ✅ Report can be regenerated in under 10 seconds
- ✅ Process is documented and repeatable

## Metadata

**Category:** Dogfooding
**Tags:** documentation, automation, filesystem, jinja2, status-tracking
**Last Updated:** 2025-10-11
**Chora Compose Version:** 0.2.0+
