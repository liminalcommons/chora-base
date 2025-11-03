"""
Artifact Assembler - Assembles final artifacts from content configs

Combines all content elements into a complete coordination request JSON.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from .config_loader import ConfigLoader, ArtifactConfig, ContentConfig
from ..generators import get_generator


class ArtifactAssembler:
    """
    Assembles artifacts by generating content from configs and combining them.

    Workflow:
    1. Load artifact config
    2. Load all referenced content configs
    3. Generate each content element using appropriate generator
    4. Combine elements into final artifact structure
    5. Write to output file
    """

    def __init__(
        self,
        config_loader: ConfigLoader,
        ai_model: str = "claude-3-5-sonnet-20241022",
        ai_api_key: Optional[str] = None
    ):
        """
        Initialize assembler.

        Args:
            config_loader: ConfigLoader instance
            ai_model: Model to use for AI-augmented generation
            ai_api_key: API key for AI (defaults to env var)
        """
        self.config_loader = config_loader
        self.ai_model = ai_model
        self.ai_api_key = ai_api_key
        self._generator_cache = {}

    def assemble(
        self,
        artifact_id: str,
        context: Dict[str, Any],
        output_path: Optional[Path] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Assemble an artifact from configs and context.

        Args:
            artifact_id: The artifact config ID
            context: User-provided context data
            output_path: Override output path (uses artifact config default if None)
            dry_run: If True, return artifact without writing to disk

        Returns:
            The assembled artifact as a dictionary

        Raises:
            ValueError: If config is invalid or context is missing
            RuntimeError: If generation fails
        """
        # Load artifact config
        artifact_config = self.config_loader.load_artifact_config(artifact_id)

        # Load all content configs
        content_configs = self.config_loader.load_all_content_for_artifact(artifact_id)

        # Generate all content elements
        artifact_data = {}

        # Add today's date to metadata for timestamp generation
        from datetime import date
        today_date = date.today().isoformat()

        for content_config in content_configs:
            # Generate each element in the content config
            for element in content_config.elements:
                # Get appropriate generator
                generator = self._get_generator(
                    element.generation_pattern,
                    model=self.ai_model,
                    api_key=self.ai_api_key
                )

                # Generate content
                try:
                    # Add today to metadata
                    metadata = content_config.metadata.copy() if content_config.metadata else {}
                    metadata['today'] = today_date

                    value = generator.generate(
                        element,
                        context,
                        metadata
                    )

                    # Parse JSON if element expects structured data
                    if element.example_output and (
                        element.example_output.startswith('[') or
                        element.example_output.startswith('{')
                    ):
                        try:
                            value = json.loads(value)
                        except json.JSONDecodeError:
                            # Keep as string if JSON parsing fails
                            pass

                    # Determine field name from element ID
                    field_name = self._extract_field_name(element.id)

                    # Handle nested fields (e.g., context.background)
                    self._set_nested_field(artifact_data, field_name, value)

                except Exception as e:
                    if element.required:
                        raise RuntimeError(
                            f"Failed to generate required element '{element.id}': {e}"
                        )
                    # Optional element failed, log and continue
                    print(f"Warning: Failed to generate optional element '{element.id}': {e}")

        # Write to output file (unless dry run)
        if not dry_run:
            output_file = output_path or Path(artifact_config.output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(artifact_data, f, indent=2)

            print(f"✓ Artifact written to: {output_file}")

        return artifact_data

    def _get_generator(self, generation_pattern: str, **kwargs):
        """
        Get or create generator instance (with caching).

        Args:
            generation_pattern: The generation pattern
            **kwargs: Arguments for generator constructor

        Returns:
            Generator instance
        """
        # Cache generators except AI generators (which may have per-element prompts)
        if generation_pattern == 'ai_augmented':
            from ..generators.ai_augmented import AIAugmentedGenerator
            return AIAugmentedGenerator(model=kwargs.get('model'), api_key=kwargs.get('api_key'))

        if generation_pattern not in self._generator_cache:
            self._generator_cache[generation_pattern] = get_generator(generation_pattern, **kwargs)

        return self._generator_cache[generation_pattern]

    def _extract_field_name(self, element_id: str) -> str:
        """
        Extract the JSON field name from element ID.

        Examples:
            "title_field" -> "title"
            "request_id_field" -> "request_id"
            "context_background" -> "context.background"
            "timeline_milestones" -> "timeline.milestones"
        """
        # Remove common suffixes
        for suffix in ['_field', '_content', '_block', '_element']:
            if element_id.endswith(suffix):
                element_id = element_id[:-len(suffix)]
                break

        # Handle nested fields (convert underscore to dot notation for known nested fields)
        nested_prefixes = ['context', 'timeline', 'metadata']
        for prefix in nested_prefixes:
            if element_id.startswith(f"{prefix}_"):
                return element_id.replace('_', '.', 1)

        return element_id

    def _set_nested_field(self, data: Dict[str, Any], field_path: str, value: Any) -> None:
        """
        Set a nested field in a dictionary using dot notation.

        Examples:
            field_path = "title" -> data["title"] = value
            field_path = "context.background" -> data["context"]["background"] = value
        """
        if '.' not in field_path:
            # Simple field
            data[field_path] = value
        else:
            # Nested field
            parts = field_path.split('.')
            current = data

            # Navigate/create nested structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Set final value
            current[parts[-1]] = value

    def preview(self, artifact_id: str, context: Dict[str, Any]) -> str:
        """
        Generate a preview of the artifact without writing to disk.

        Args:
            artifact_id: The artifact config ID
            context: User-provided context data

        Returns:
            JSON string of the assembled artifact
        """
        artifact = self.assemble(artifact_id, context, dry_run=True)
        return json.dumps(artifact, indent=2)
