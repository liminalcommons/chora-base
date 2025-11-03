"""
Config Loader - Loads and validates content and artifact configs

Part of the standalone inbox generator (Path C implementation).
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ContentElement:
    """Represents a single content element from a content config"""
    id: str
    generation_pattern: str  # literal, user_input, template_fill, ai_augmented
    example_output: Optional[str] = None
    template: Optional[str] = None
    prompt_template: Optional[str] = None
    required: bool = True


@dataclass
class ContentConfig:
    """Represents a content configuration"""
    id: str
    type: str
    version: str
    title: str
    elements: List[ContentElement]
    metadata: Dict[str, Any]


@dataclass
class ArtifactChild:
    """Represents a child reference in an artifact config"""
    id: str
    path: str
    required: bool = True
    order: int = 0


@dataclass
class ArtifactConfig:
    """Represents an artifact configuration"""
    id: str
    type: str
    version: str
    title: str
    output_file: str
    composition_strategy: str  # concat, merge
    children: List[ArtifactChild]
    metadata: Dict[str, Any]


class ConfigLoader:
    """
    Loads content and artifact configurations from JSON files.

    Features:
    - JSON schema validation
    - Dependency resolution
    - Config caching
    """

    def __init__(self, content_dir: Path, artifact_dir: Optional[Path] = None):
        """
        Initialize config loader.

        Args:
            content_dir: Directory containing content config JSON files
            artifact_dir: Directory containing artifact config JSON files (optional)
        """
        self.content_dir = Path(content_dir)
        self.artifact_dir = Path(artifact_dir) if artifact_dir else self.content_dir
        self._content_cache: Dict[str, ContentConfig] = {}
        self._artifact_cache: Dict[str, ArtifactConfig] = {}

    def load_content_config(self, config_id: str) -> ContentConfig:
        """
        Load a content configuration by ID.

        Args:
            config_id: The content config ID (without .json extension)

        Returns:
            ContentConfig object

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        # Check cache first
        if config_id in self._content_cache:
            return self._content_cache[config_id]

        # Find config file
        config_file = self.content_dir / f"{config_id}.json"
        if not config_file.exists():
            raise FileNotFoundError(f"Content config not found: {config_file}")

        # Load and parse JSON
        with open(config_file, 'r') as f:
            data = json.load(f)

        # Validate required fields
        if data.get('type') != 'content':
            raise ValueError(f"Invalid config type: {data.get('type')} (expected 'content')")

        if data.get('id') != config_id:
            raise ValueError(f"Config ID mismatch: {data.get('id')} != {config_id}")

        # Parse elements
        elements = []
        for elem_data in data.get('elements', []):
            element = ContentElement(
                id=elem_data['id'],
                generation_pattern=elem_data['generation_pattern'],
                example_output=elem_data.get('example_output'),
                template=elem_data.get('template'),
                prompt_template=elem_data.get('prompt_template'),
                required=elem_data.get('required', True)
            )
            elements.append(element)

        # Create ContentConfig
        config = ContentConfig(
            id=data['id'],
            type=data['type'],
            version=data.get('metadata', {}).get('version', '1.0'),
            title=data.get('metadata', {}).get('title', ''),
            elements=elements,
            metadata=data.get('metadata', {})
        )

        # Cache and return
        self._content_cache[config_id] = config
        return config

    def load_artifact_config(self, config_id: str) -> ArtifactConfig:
        """
        Load an artifact configuration by ID.

        Args:
            config_id: The artifact config ID (without .json extension)

        Returns:
            ArtifactConfig object

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        # Check cache first
        if config_id in self._artifact_cache:
            return self._artifact_cache[config_id]

        # Find config file
        config_file = self.artifact_dir / f"{config_id}.json"
        if not config_file.exists():
            raise FileNotFoundError(f"Artifact config not found: {config_file}")

        # Load and parse JSON
        with open(config_file, 'r') as f:
            data = json.load(f)

        # Validate required fields
        if data.get('type') != 'artifact':
            raise ValueError(f"Invalid config type: {data.get('type')} (expected 'artifact')")

        if data.get('id') != config_id:
            raise ValueError(f"Config ID mismatch: {data.get('id')} != {config_id}")

        # Parse children
        children = []
        for child_data in data.get('content', {}).get('children', []):
            child = ArtifactChild(
                id=child_data['id'],
                path=child_data['path'],
                required=child_data.get('required', True),
                order=child_data.get('order', 0)
            )
            children.append(child)

        # Sort children by order
        children.sort(key=lambda c: c.order)

        # Create ArtifactConfig
        config = ArtifactConfig(
            id=data['id'],
            type=data['type'],
            version=data.get('metadata', {}).get('version', '1.0'),
            title=data.get('metadata', {}).get('title', ''),
            output_file=data.get('metadata', {}).get('outputs', [{}])[0].get('file', ''),
            composition_strategy=data.get('metadata', {}).get('compositionStrategy', 'concat'),
            children=children,
            metadata=data.get('metadata', {})
        )

        # Cache and return
        self._artifact_cache[config_id] = config
        return config

    def load_all_content_for_artifact(self, artifact_id: str) -> List[ContentConfig]:
        """
        Load all content configs referenced by an artifact.

        Args:
            artifact_id: The artifact config ID

        Returns:
            List of ContentConfig objects in order
        """
        artifact = self.load_artifact_config(artifact_id)
        content_configs = []

        for child in artifact.children:
            # Extract config ID from path (assumes path like "configs/content/my-config.json")
            config_id = Path(child.path).stem

            try:
                content_config = self.load_content_config(config_id)
                content_configs.append(content_config)
            except FileNotFoundError as e:
                if child.required:
                    raise
                # Optional child missing, skip it
                print(f"Warning: Optional content config not found: {config_id}")

        return content_configs

    def validate_config_tree(self, artifact_id: str) -> bool:
        """
        Validate that all required content configs exist for an artifact.

        Args:
            artifact_id: The artifact config ID

        Returns:
            True if all required configs exist, False otherwise
        """
        try:
            self.load_all_content_for_artifact(artifact_id)
            return True
        except FileNotFoundError:
            return False
