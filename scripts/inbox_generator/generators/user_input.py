"""
User Input Generator - Extracts values from user context

Used for fields where the user provides the value directly (e.g., title, description)
"""

from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..core.config_loader import ContentElement


class UserInputGenerator(BaseGenerator):
    """
    Generates content by extracting values from user-provided context.

    Example:
        context = {"title": "Update documentation"}
        element.id = "title_field"
        -> Returns: "Update documentation"
    """

    def generate(
        self,
        element: ContentElement,
        context: Dict[str, Any],
        config_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Extract value from user context.

        The context key is derived from the element ID by removing common suffixes
        like '_field', '_content', '_block', etc.

        Args:
            element: Content element to generate
            context: User-provided context data
            config_metadata: Config metadata (unused)

        Returns:
            Value from context

        Raises:
            ValueError: If required context key is missing
        """
        # Try multiple possible context keys
        possible_keys = self._get_possible_keys(element.id)

        for key in possible_keys:
            if key in context:
                value = context[key]
                # Handle different types
                if isinstance(value, (list, dict)):
                    import json
                    return json.dumps(value, indent=2)
                return str(value)

        # No matching key found
        raise ValueError(
            f"User input not found for element '{element.id}'. "
            f"Tried keys: {possible_keys}"
        )

    def _get_possible_keys(self, element_id: str) -> list[str]:
        """
        Generate possible context keys from element ID.

        Example:
            "title_field" -> ["title_field", "title"]
            "context_background" -> ["context_background", "context.background", "background"]
        """
        keys = [element_id]

        # Remove common suffixes
        for suffix in ['_field', '_content', '_block', '_element']:
            if element_id.endswith(suffix):
                base = element_id[:-len(suffix)]
                keys.append(base)

        # Handle nested keys (e.g., "context_background" -> "context.background")
        if '_' in element_id:
            parts = element_id.split('_')
            # Try dot notation
            keys.append('.'.join(parts))
            # Try just the last part
            keys.append(parts[-1])

        return keys
