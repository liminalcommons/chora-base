# Tutorial: Create a Custom Generator

**Goal**: Learn how to create a custom content generator from scratch, test it, and integrate it with chora-compose.

**Time**: 45-60 minutes

**Level**: Advanced

**Prerequisites**:
- Completed [Generate Your First Content](../getting-started/03-generate-your-first-content.md)
- Python programming experience
- Understanding of abstract base classes (ABC)
- Familiar with chora-compose config structure

---

## What You'll Build

A custom `markdown_table` generator that creates formatted Markdown tables from structured data.

**Example input** (context):
```json
{
  "headers": ["Name", "Age", "City"],
  "rows": [
    ["Alice", 30, "NYC"],
    ["Bob", 25, "LA"],
    ["Charlie", 35, "SF"]
  ]
}
```

**Example output**:
```markdown
| Name    | Age | City |
|---------|-----|------|
| Alice   | 30  | NYC  |
| Bob     | 25  | LA   |
| Charlie | 35  | SF   |
```

**Why this example?**
- Simple enough to understand quickly
- Complex enough to demonstrate key concepts
- Useful in real-world scenarios (documentation, reports)
- Shows pattern for data transformation generators

---

## Step 1: Understand the Generator Interface

### The GeneratorStrategy Base Class

All generators in chora-compose must implement the `GeneratorStrategy` interface.

From [src/chora_compose/generators/base.py:9-29](../../../src/chora_compose/generators/base.py#L9-L29):

```python
from abc import ABC, abstractmethod
from typing import Any
from chora_compose.core.models import ContentConfig

class GeneratorStrategy(ABC):
    """Abstract base class for content generation strategies."""

    @abstractmethod
    def generate(
        self, config: ContentConfig, context: dict[str, Any] | None = None
    ) -> str:
        """
        Generate content based on the provided configuration.

        Args:
            config: Content configuration containing elements and generation patterns
            context: Optional additional context data for generation

        Returns:
            Generated content as a string

        Raises:
            ValueError: If configuration is invalid or generation fails
        """
        pass
```

**Key requirements**:
1. **Inherit from `GeneratorStrategy`** (ABC)
2. **Implement `generate()` method** (signature must match)
3. **Return a string** (generated content)
4. **Accept `ContentConfig` and optional `context`**

### Helper Method Available

The base class provides `_extract_element_data()`:

```python
def _extract_element_data(self, config: ContentConfig) -> dict[str, str]:
    """
    Extract element data into a dictionary for easy access.

    Returns:
        Dictionary mapping element names to their example_output
    """
    return {
        element.name: element.example_output or ""
        for element in config.elements
    }
```

**Use case**: Access `elements[*].example_output` as a dict.

---

## Step 2: Create Your Generator Class

### Create the File

```bash
# Create a new generator file
mkdir -p src/my_generators
touch src/my_generators/markdown_table_generator.py
```

### Implement the Generator

```python
# src/my_generators/markdown_table_generator.py
"""Markdown table generator for structured data."""

from typing import Any
from chora_compose.core.models import ContentConfig
from chora_compose.generators.base import GeneratorStrategy


class MarkdownTableError(Exception):
    """Raised when table generation fails."""
    pass


class MarkdownTableGenerator(GeneratorStrategy):
    """
    Generate Markdown tables from structured data.

    Expects context with:
    - headers: list[str] - Column headers
    - rows: list[list[Any]] - Table rows
    - alignment: list[str] (optional) - Column alignment ("left", "center", "right")

    Example context:
        {
            "headers": ["Name", "Age", "City"],
            "rows": [
                ["Alice", 30, "NYC"],
                ["Bob", 25, "LA"]
            ],
            "alignment": ["left", "right", "left"]
        }

    Output:
        | Name  | Age | City |
        |-------|-----|------|
        | Alice |  30 | NYC  |
        | Bob   |  25 | LA   |
    """

    def __init__(self, default_alignment: str = "left"):
        """
        Initialize the markdown table generator.

        Args:
            default_alignment: Default column alignment ("left", "center", "right")
        """
        if default_alignment not in ("left", "center", "right"):
            raise ValueError(
                f"Invalid default_alignment: {default_alignment}. "
                "Must be 'left', 'center', or 'right'."
            )

        self.default_alignment = default_alignment
        self.version = "1.0.0"
        self.description = "Generate Markdown tables from structured data"
        self.capabilities = ["table", "markdown", "formatting"]

    def generate(
        self, config: ContentConfig, context: dict[str, Any] | None = None
    ) -> str:
        """
        Generate Markdown table from context data.

        Args:
            config: Content configuration (not used, but required by interface)
            context: Dictionary with 'headers' and 'rows' keys

        Returns:
            Formatted Markdown table as string

        Raises:
            MarkdownTableError: If context is invalid or missing required fields
        """
        # Validate context
        if not context:
            raise MarkdownTableError("Context is required for markdown_table generator")

        if "headers" not in context:
            raise MarkdownTableError("Context must include 'headers' key")

        if "rows" not in context:
            raise MarkdownTableError("Context must include 'rows' key")

        headers = context["headers"]
        rows = context["rows"]
        alignment = context.get("alignment", [])

        # Validate headers
        if not isinstance(headers, list) or not headers:
            raise MarkdownTableError("headers must be a non-empty list")

        # Validate rows
        if not isinstance(rows, list):
            raise MarkdownTableError("rows must be a list")

        # Validate alignment (optional)
        num_cols = len(headers)
        if alignment:
            if len(alignment) != num_cols:
                raise MarkdownTableError(
                    f"alignment length ({len(alignment)}) must match "
                    f"headers length ({num_cols})"
                )
            for align in alignment:
                if align not in ("left", "center", "right"):
                    raise MarkdownTableError(
                        f"Invalid alignment value: {align}. "
                        "Must be 'left', 'center', or 'right'."
                    )
        else:
            # Use default alignment for all columns
            alignment = [self.default_alignment] * num_cols

        # Build table
        return self._build_markdown_table(headers, rows, alignment)

    def _build_markdown_table(
        self, headers: list[str], rows: list[list[Any]], alignment: list[str]
    ) -> str:
        """
        Build the Markdown table string.

        Args:
            headers: Column headers
            rows: Table rows
            alignment: Column alignments

        Returns:
            Formatted Markdown table
        """
        # Convert all values to strings
        str_headers = [str(h) for h in headers]
        str_rows = [[str(cell) for cell in row] for row in rows]

        # Calculate column widths (max of header width and all cell widths)
        col_widths = []
        for col_idx in range(len(str_headers)):
            max_width = len(str_headers[col_idx])
            for row in str_rows:
                if col_idx < len(row):
                    max_width = max(max_width, len(row[col_idx]))
            col_widths.append(max(max_width, 3))  # Minimum width of 3

        # Build header row
        header_cells = []
        for idx, (header, width) in enumerate(zip(str_headers, col_widths)):
            header_cells.append(self._pad_cell(header, width, alignment[idx]))
        header_line = "| " + " | ".join(header_cells) + " |"

        # Build separator row
        separator_cells = []
        for width, align in zip(col_widths, alignment):
            separator_cells.append(self._create_separator(width, align))
        separator_line = "| " + " | ".join(separator_cells) + " |"

        # Build data rows
        data_lines = []
        for row in str_rows:
            row_cells = []
            for col_idx, width in enumerate(col_widths):
                # Handle rows with fewer cells than headers
                cell_value = row[col_idx] if col_idx < len(row) else ""
                row_cells.append(self._pad_cell(cell_value, width, alignment[col_idx]))
            data_lines.append("| " + " | ".join(row_cells) + " |")

        # Combine all lines
        return "\n".join([header_line, separator_line] + data_lines)

    def _pad_cell(self, value: str, width: int, alignment: str) -> str:
        """
        Pad cell value to specified width with alignment.

        Args:
            value: Cell value
            width: Target width
            alignment: "left", "center", or "right"

        Returns:
            Padded cell value
        """
        if alignment == "left":
            return value.ljust(width)
        elif alignment == "right":
            return value.rjust(width)
        else:  # center
            return value.center(width)

    def _create_separator(self, width: int, alignment: str) -> str:
        """
        Create separator line for a column.

        Args:
            width: Column width
            alignment: "left", "center", or "right"

        Returns:
            Separator string (e.g., ":---", "---:", ":---:")
        """
        dashes = "-" * width

        if alignment == "left":
            return ":" + dashes[1:]
        elif alignment == "right":
            return dashes[:-1] + ":"
        else:  # center
            return ":" + dashes[1:-1] + ":"
```

**Key features implemented**:
1. ✅ Inherits from `GeneratorStrategy`
2. ✅ Implements `generate()` with correct signature
3. ✅ Returns string (Markdown table)
4. ✅ Validates input (raises `MarkdownTableError`)
5. ✅ Handles edge cases (empty rows, mismatched columns)
6. ✅ Configurable (default alignment)
7. ✅ Well-documented (docstrings)

---

## Step 3: Write Tests

### Create Test File

```bash
touch tests/test_markdown_table_generator.py
```

### Write Comprehensive Tests

```python
# tests/test_markdown_table_generator.py
"""Tests for MarkdownTableGenerator."""

import pytest
from chora_compose.core.models import (
    ContentConfig,
    ContentElement,
    Generation,
    GenerationPattern,
)
from my_generators.markdown_table_generator import (
    MarkdownTableError,
    MarkdownTableGenerator,
)


def create_test_config() -> ContentConfig:
    """Helper to create a minimal test content config."""
    return ContentConfig(
        type="content",
        id="test-markdown-table",
        schemaRef={"id": "content-schema", "version": "3.1"},
        metadata={
            "description": "Test config",
            "version": "1.0.0",
            "generation_frequency": "manual",
            "output_format": "markdown",
        },
        instructions={
            "global": "Test",
            "system_prompt": "Test",
            "user_prompt": "Test",
        },
        elements=[
            ContentElement(
                name="placeholder",
                format="markdown",
                example_output="",
            )
        ],
        generation=Generation(
            patterns=[
                GenerationPattern(
                    id="main",
                    type="markdown_table",
                    template="",
                )
            ]
        ),
    )


class TestBasicTableGeneration:
    """Test basic table generation functionality."""

    def test_simple_table(self):
        """Test generating a simple 3x2 table."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Name", "Age", "City"],
            "rows": [
                ["Alice", 30, "NYC"],
                ["Bob", 25, "LA"],
            ],
        }

        result = generator.generate(config, context)

        # Verify structure
        lines = result.split("\n")
        assert len(lines) == 4  # header + separator + 2 data rows
        assert all(line.startswith("|") and line.endswith("|") for line in lines)

        # Verify content
        assert "Alice" in result
        assert "Bob" in result
        assert "30" in result

    def test_empty_table(self):
        """Test table with headers but no rows."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Column1", "Column2"],
            "rows": [],
        }

        result = generator.generate(config, context)

        lines = result.split("\n")
        assert len(lines) == 2  # header + separator only
        assert "Column1" in result
        assert "Column2" in result

    def test_single_column_table(self):
        """Test table with single column."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Name"],
            "rows": [["Alice"], ["Bob"], ["Charlie"]],
        }

        result = generator.generate(config, context)

        lines = result.split("\n")
        assert len(lines) == 5  # header + separator + 3 rows
        assert "Alice" in result
        assert "Bob" in result
        assert "Charlie" in result


class TestAlignment:
    """Test column alignment features."""

    def test_left_alignment(self):
        """Test left-aligned columns."""
        generator = MarkdownTableGenerator(default_alignment="left")
        config = create_test_config()
        context = {
            "headers": ["Name", "Age"],
            "rows": [["Alice", 30]],
        }

        result = generator.generate(config, context)

        # Left alignment uses :--- separator
        assert ":---" in result
        assert "---:" not in result

    def test_right_alignment(self):
        """Test right-aligned columns."""
        generator = MarkdownTableGenerator(default_alignment="right")
        config = create_test_config()
        context = {
            "headers": ["Name", "Age"],
            "rows": [["Alice", 30]],
        }

        result = generator.generate(config, context)

        # Right alignment uses ---: separator
        assert "---:" in result

    def test_center_alignment(self):
        """Test center-aligned columns."""
        generator = MarkdownTableGenerator(default_alignment="center")
        config = create_test_config()
        context = {
            "headers": ["Name", "Age"],
            "rows": [["Alice", 30]],
        }

        result = generator.generate(config, context)

        # Center alignment uses :---: separator
        assert ":---:" in result

    def test_mixed_alignment(self):
        """Test custom alignment per column."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Name", "Age", "City"],
            "rows": [["Alice", 30, "NYC"]],
            "alignment": ["left", "right", "center"],
        }

        result = generator.generate(config, context)

        lines = result.split("\n")
        separator = lines[1]

        # Verify alignment markers
        assert ":---" in separator  # left
        assert "---:" in separator  # right
        assert ":---:" in separator  # center


class TestErrorHandling:
    """Test error handling and validation."""

    def test_missing_context(self):
        """Test error when context is None."""
        generator = MarkdownTableGenerator()
        config = create_test_config()

        with pytest.raises(MarkdownTableError) as exc_info:
            generator.generate(config, None)

        assert "required" in str(exc_info.value).lower()

    def test_missing_headers(self):
        """Test error when headers key missing."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {"rows": [["Alice", 30]]}  # Missing headers

        with pytest.raises(MarkdownTableError) as exc_info:
            generator.generate(config, context)

        assert "headers" in str(exc_info.value).lower()

    def test_missing_rows(self):
        """Test error when rows key missing."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {"headers": ["Name", "Age"]}  # Missing rows

        with pytest.raises(MarkdownTableError) as exc_info:
            generator.generate(config, context)

        assert "rows" in str(exc_info.value).lower()

    def test_empty_headers(self):
        """Test error when headers list is empty."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {"headers": [], "rows": []}

        with pytest.raises(MarkdownTableError) as exc_info:
            generator.generate(config, context)

        assert "non-empty" in str(exc_info.value).lower()

    def test_invalid_alignment_length(self):
        """Test error when alignment doesn't match headers."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Name", "Age"],
            "rows": [["Alice", 30]],
            "alignment": ["left"],  # Should be 2 items
        }

        with pytest.raises(MarkdownTableError) as exc_info:
            generator.generate(config, context)

        assert "alignment length" in str(exc_info.value).lower()

    def test_invalid_alignment_value(self):
        """Test error when alignment has invalid value."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Name", "Age"],
            "rows": [["Alice", 30]],
            "alignment": ["left", "invalid"],  # "invalid" not allowed
        }

        with pytest.raises(MarkdownTableError) as exc_info:
            generator.generate(config, context)

        assert "Invalid alignment value" in str(exc_info.value)


class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_uneven_rows(self):
        """Test table with rows having different lengths."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Name", "Age", "City"],
            "rows": [
                ["Alice", 30, "NYC"],
                ["Bob", 25],  # Missing "City"
                ["Charlie"],  # Missing "Age" and "City"
            ],
        }

        result = generator.generate(config, context)

        # Should not crash, missing cells filled with empty strings
        lines = result.split("\n")
        assert len(lines) == 5  # header + separator + 3 rows

    def test_very_long_cell_values(self):
        """Test table with very long cell values."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        long_text = "A" * 100
        context = {
            "headers": ["Name", "Description"],
            "rows": [["Alice", long_text]],
        }

        result = generator.generate(config, context)

        # Should handle long values without crashing
        assert long_text in result

    def test_special_characters(self):
        """Test table with special Markdown characters."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Name", "Symbol"],
            "rows": [
                ["Alice", "**bold**"],
                ["Bob", "|pipe|"],
                ["Charlie", "`code`"],
            ],
        }

        result = generator.generate(config, context)

        # Special characters should be preserved
        assert "**bold**" in result
        assert "|pipe|" in result
        assert "`code`" in result

    def test_numeric_types(self):
        """Test table with various numeric types."""
        generator = MarkdownTableGenerator()
        config = create_test_config()
        context = {
            "headers": ["Integer", "Float", "Bool"],
            "rows": [
                [42, 3.14, True],
                [0, -2.5, False],
            ],
        }

        result = generator.generate(config, context)

        # All types should be converted to strings
        assert "42" in result
        assert "3.14" in result
        assert "True" in result
        assert "False" in result
```

**Run tests**:

```bash
pytest tests/test_markdown_table_generator.py -v
```

**Expected output**:
```
tests/test_markdown_table_generator.py::TestBasicTableGeneration::test_simple_table PASSED
tests/test_markdown_table_generator.py::TestBasicTableGeneration::test_empty_table PASSED
tests/test_markdown_table_generator.py::TestBasicTableGeneration::test_single_column_table PASSED
tests/test_markdown_table_generator.py::TestAlignment::test_left_alignment PASSED
tests/test_markdown_table_generator.py::TestAlignment::test_right_alignment PASSED
tests/test_markdown_table_generator.py::TestAlignment::test_center_alignment PASSED
tests/test_markdown_table_generator.py::TestAlignment::test_mixed_alignment PASSED
tests/test_markdown_table_generator.py::TestErrorHandling::test_missing_context PASSED
tests/test_markdown_table_generator.py::TestErrorHandling::test_missing_headers PASSED
tests/test_markdown_table_generator.py::TestErrorHandling::test_missing_rows PASSED
tests/test_markdown_table_generator.py::TestErrorHandling::test_empty_headers PASSED
tests/test_markdown_table_generator.py::TestErrorHandling::test_invalid_alignment_length PASSED
tests/test_markdown_table_generator.py::TestErrorHandling::test_invalid_alignment_value PASSED
tests/test_markdown_table_generator.py::TestEdgeCases::test_uneven_rows PASSED
tests/test_markdown_table_generator.py::TestEdgeCases::test_very_long_cell_values PASSED
tests/test_markdown_table_generator.py::TestEdgeCases::test_special_characters PASSED
tests/test_markdown_table_generator.py::TestEdgeCases::test_numeric_types PASSED

================ 17 passed in 0.12s ================
```

---

## Step 4: Register Your Generator

### Option 1: Programmatic Registration (Recommended for Libraries)

```python
# src/my_generators/__init__.py
"""Custom generators for chora-compose."""

from chora_compose.generators.registry import GeneratorRegistry
from my_generators.markdown_table_generator import MarkdownTableGenerator


def register_generators():
    """Register custom generators with the global registry."""
    registry = GeneratorRegistry()
    registry.register("markdown_table", MarkdownTableGenerator())


# Auto-register when module is imported
register_generators()
```

**Usage**:

```python
# In your application
import my_generators  # Automatically registers markdown_table

from chora_compose.generators.registry import GeneratorRegistry

registry = GeneratorRegistry()
generator = registry.get("markdown_table")  # ✅ Available
```

### Option 2: Plugin Discovery (Recommended for User Extensions)

**Create plugin file**:

```bash
# User's local plugins directory
mkdir -p ~/.chora-compose/generators
```

```python
# ~/.chora-compose/generators/markdown_table_generator.py
"""Markdown table generator plugin."""

from typing import Any
from chora_compose.core.models import ContentConfig
from chora_compose.generators.base import GeneratorStrategy


class MarkdownTableError(Exception):
    """Raised when table generation fails."""
    pass


class MarkdownTableGenerator(GeneratorStrategy):
    # ... (same implementation as above)
    pass


# Specify generator type for auto-discovery
GENERATOR_TYPE = "markdown_table"
```

**Auto-discovery**:

```python
from chora_compose.generators.registry import GeneratorRegistry

registry = GeneratorRegistry()  # Automatically discovers ~/.chora-compose/generators/*.py
generator = registry.get("markdown_table")  # ✅ Available
```

**How plugin discovery works** (from [registry.py:151-204](../../../src/chora_compose/generators/registry.py#L151-L204)):
1. Scans `~/.chora-compose/generators/` and `.chora-compose/generators/`
2. Finds files matching `*_generator.py`
3. Imports modules
4. Looks for `GeneratorStrategy` subclass
5. Reads `GENERATOR_TYPE` attribute (or derives from filename)
6. Instantiates and registers

### Option 3: Direct Registration (Testing/Prototyping)

```python
from chora_compose.generators.registry import GeneratorRegistry
from my_generators.markdown_table_generator import MarkdownTableGenerator

registry = GeneratorRegistry()
registry.register("markdown_table", MarkdownTableGenerator())

# Now available
generator = registry.get("markdown_table")
```

**Recommendation**: Use Option 1 for libraries, Option 2 for user extensions, Option 3 for testing.

---

## Step 5: Create a Content Configuration

### Create Config File

```bash
mkdir -p configs/content
```

```json
{
  "type": "content",
  "id": "team-roster-table",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Team roster as Markdown table",
    "version": "1.0.0",
    "generation_frequency": "on_demand",
    "output_format": "markdown"
  },
  "instructions": {
    "global": "Generate team roster table",
    "system_prompt": "Format team data as Markdown table",
    "user_prompt": "Create a table of team members with their roles and locations"
  },
  "elements": [
    {
      "name": "roster_table",
      "description": "Team roster table",
      "format": "markdown",
      "review_status": "approved"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "table-pattern",
        "type": "markdown_table",
        "template": "",
        "generation_config": {}
      }
    ]
  }
}
```

**Save as**: `configs/content/team-roster-table.json`

---

## Step 6: Use Your Custom Generator

### Programmatic Usage

```python
# test_custom_generator.py
"""Test custom markdown_table generator."""

from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.registry import GeneratorRegistry
import my_generators  # Register custom generators


def main():
    # Load config
    loader = ConfigLoader()
    config = loader.load_content_config("team-roster-table")

    # Prepare context
    context = {
        "headers": ["Name", "Role", "Location"],
        "rows": [
            ["Alice Johnson", "Engineering Lead", "San Francisco"],
            ["Bob Smith", "Product Manager", "New York"],
            ["Charlie Brown", "UX Designer", "Remote"],
            ["Diana Prince", "Data Scientist", "Boston"],
        ],
        "alignment": ["left", "left", "center"],
    }

    # Get generator from registry
    registry = GeneratorRegistry()
    generator = registry.get("markdown_table")

    # Generate content
    output = generator.generate(config, context)

    print("Generated Markdown Table:")
    print("=" * 60)
    print(output)
    print("=" * 60)

    # Save to file
    with open("team_roster.md", "w") as f:
        f.write(output)
    print("\nSaved to: team_roster.md")


if __name__ == "__main__":
    main()
```

**Run**:

```bash
python test_custom_generator.py
```

**Output**:

```
Generated Markdown Table:
============================================================
| Name           | Role             | Location      |
|:---------------|:-----------------|:-------------:|
| Alice Johnson  | Engineering Lead | San Francisco |
| Bob Smith      | Product Manager  |   New York    |
| Charlie Brown  | UX Designer      |    Remote     |
| Diana Prince   | Data Scientist   |    Boston     |
============================================================

Saved to: team_roster.md
```

### MCP Tool Usage

If you want to use your custom generator via MCP tools, it must be registered before the MCP server starts.

**Approach 1: Register in your main module**:

```python
# src/my_app/__init__.py
import my_generators  # Registers markdown_table on import

# Start MCP server
from chora_compose.mcp.server import main
main()
```

**Approach 2: Use plugin discovery**:

```bash
# Copy generator to user plugins directory
cp src/my_generators/markdown_table_generator.py ~/.chora-compose/generators/

# Restart MCP server (will auto-discover)
chora-compose-mcp
```

Then use via MCP tools:

```python
# Via Claude Desktop or other MCP client
result = await tools.generate_content(
    content_config_id="team-roster-table",
    context={
        "headers": ["Name", "Role", "Location"],
        "rows": [["Alice", "Lead", "SF"], ["Bob", "PM", "NYC"]]
    }
)
```

---

## Step 7: Add Advanced Features (Optional)

### Feature 1: Telemetry Events

Track generator usage with event emission:

```python
# Add to MarkdownTableGenerator.generate()
import time
from chora_compose.telemetry import ContentGeneratedEvent, emit_event

def generate(self, config: ContentConfig, context: dict[str, Any] | None = None) -> str:
    start_time = time.time()
    status = "success"
    error_message = None

    try:
        # ... existing generation logic ...
        result = self._build_markdown_table(headers, rows, alignment)
        return result
    except Exception as e:
        status = "error"
        error_message = str(e)
        raise
    finally:
        # Emit telemetry event
        duration_ms = int((time.time() - start_time) * 1000)
        emit_event(
            ContentGeneratedEvent(
                content_config_id=config.id,
                generator_type="markdown_table",
                status=status,
                duration_ms=duration_ms,
                error_message=error_message,
            )
        )
```

**Benefit**: Track usage, performance, errors in telemetry logs.

### Feature 2: Upstream Dependencies Metadata

Document external dependencies:

```python
from chora_compose.models import UpstreamDependencies

class MarkdownTableGenerator(GeneratorStrategy):
    def __init__(self, default_alignment: str = "left"):
        # ... existing __init__ ...

        # Add metadata
        self.upstream_dependencies = UpstreamDependencies(
            services=[],  # No external services
            credentials_required=[],  # No credentials
            concurrency_safe=True,  # Safe for concurrent use
            stability="stable",
        )
```

**Benefit**: Expose capabilities to MCP clients (see `capabilities` resource).

### Feature 3: CSV Input Support

Extend generator to accept CSV file path:

```python
import csv
from pathlib import Path

def generate(self, config: ContentConfig, context: dict[str, Any] | None = None) -> str:
    # ... existing validation ...

    # Support CSV file input
    if "csv_file" in context:
        csv_path = Path(context["csv_file"])
        if not csv_path.exists():
            raise MarkdownTableError(f"CSV file not found: {csv_path}")

        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            rows_list = list(reader)
            if not rows_list:
                raise MarkdownTableError("CSV file is empty")

            headers = rows_list[0]
            rows = rows_list[1:]

            # Use CSV data instead of context data
            context = {"headers": headers, "rows": rows}

    # ... rest of existing logic ...
```

**Usage**:

```python
context = {"csv_file": "team_roster.csv"}
output = generator.generate(config, context)
```

---

## Troubleshooting

### Issue: Generator not found in registry

**Symptom**:
```python
RegistryError: Generator type 'markdown_table' not found.
Available types: demonstration, jinja2, template_fill
```

**Cause**: Generator not registered.

**Fix**:
```python
# Ensure registration happens before usage
import my_generators  # Registers generators
from chora_compose.generators.registry import GeneratorRegistry

registry = GeneratorRegistry()
print(registry.list_types())  # Should include 'markdown_table'
```

### Issue: `generate()` signature doesn't match

**Symptom**:
```python
TypeError: generate() missing 1 required positional argument: 'context'
```

**Cause**: Method signature doesn't match base class.

**Fix**: Ensure signature matches exactly:
```python
def generate(
    self, config: ContentConfig, context: dict[str, Any] | None = None
) -> str:
    # context must be optional (default None)
```

### Issue: Tests failing with "Config validation error"

**Symptom**:
```python
ConfigValidationError: ['metadata' is a required property]
```

**Cause**: Test config missing required fields.

**Fix**: Use helper function to create valid config:
```python
def create_test_config() -> ContentConfig:
    return ContentConfig(
        type="content",
        id="test-config",
        schemaRef={"id": "content-schema", "version": "3.1"},
        metadata={...},  # ← All required fields
        instructions={...},
        elements=[...],
        generation=Generation(patterns=[...])
    )
```

### Issue: Plugin not auto-discovered

**Symptom**: Plugin file in `~/.chora-compose/generators/` but not loaded.

**Cause**: Filename doesn't match `*_generator.py` pattern or class doesn't inherit `GeneratorStrategy`.

**Fix**:
1. Rename file to `markdown_table_generator.py` (must end with `_generator.py`)
2. Ensure class inherits from `GeneratorStrategy`
3. Add `GENERATOR_TYPE` attribute:
   ```python
   GENERATOR_TYPE = "markdown_table"
   ```

---

## Best Practices

### Do ✅

1. **Implement comprehensive error handling**
   ```python
   if not context:
       raise YourGeneratorError("Context is required")
   ```

2. **Write tests for edge cases**
   ```python
   def test_empty_rows(self):
       # Test behavior with edge case data
   ```

3. **Document your generator**
   ```python
   class MyGenerator(GeneratorStrategy):
       """
       One-line summary.

       Detailed description of what this generator does,
       expected context structure, and example output.
       """
   ```

4. **Validate inputs early**
   ```python
   # Validate at start of generate()
   if "required_key" not in context:
       raise MyGeneratorError("Missing required_key")
   ```

5. **Use helper methods**
   ```python
   def generate(self, config, context):
       validated_data = self._validate_and_prepare(context)
       return self._build_output(validated_data)
   ```

### Don't ❌

1. **Don't modify the config object**
   ```python
   # ❌ Bad: Mutating config
   config.metadata["generated_at"] = datetime.now()

   # ✅ Good: Read-only access
   description = config.metadata.get("description", "")
   ```

2. **Don't rely on global state**
   ```python
   # ❌ Bad: Global state
   global_cache = {}

   # ✅ Good: Instance attributes
   self._cache = {}
   ```

3. **Don't catch exceptions silently**
   ```python
   # ❌ Bad: Silent failure
   try:
       result = dangerous_operation()
   except:
       return ""  # User doesn't know what failed

   # ✅ Good: Explicit error
   try:
       result = dangerous_operation()
   except SpecificError as e:
       raise MyGeneratorError(f"Operation failed: {e}") from e
   ```

4. **Don't skip type hints**
   ```python
   # ❌ Bad: No type hints
   def helper(data):
       return data["key"]

   # ✅ Good: Full type hints
   def helper(data: dict[str, Any]) -> str:
       return data["key"]
   ```

---

## Summary

**What You Learned**:
1. ✅ How to implement the `GeneratorStrategy` interface
2. ✅ How to write comprehensive generator tests
3. ✅ How to register generators (3 different methods)
4. ✅ How to create configs for custom generators
5. ✅ How to use custom generators programmatically and via MCP
6. ✅ Best practices for generator development

**Next Steps**:
- Try creating generators for other use cases (JSON, YAML, SQL, etc.)
- Explore existing generators: [jinja2](../../how-to/generation/debug-jinja2-templates.md), [template_fill](../../how-to/generators/use-template-fill-generator.md)
- Read [When to Use Which Generator](../../explanation/generators/when-to-use-which.md)
- Contribute your generator to chora-compose (see [CONTRIBUTING.md](../../../CONTRIBUTING.md))

**Example Use Cases for Custom Generators**:
- **JSON/YAML formatters** (structured data output)
- **SQL query builders** (from schema definitions)
- **Diagram generators** (Mermaid, PlantUML from data)
- **Report formatters** (custom layouts)
- **API client code** (from OpenAPI specs)

---

**Last Updated**: 2025-10-21 | **Phase**: Sprint 3 - Advanced Tutorials
